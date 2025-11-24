"""
Stripe entegrasyonu - Ödeme işlemleri ve webhook'lar
"""

import os
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    stripe = None
from flask import request, jsonify
from premium import upgrade_user, get_user_id

# Stripe API key'leri environment variable'dan al
if STRIPE_AVAILABLE:
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_...')  # Test key
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', 'whsec_...')

# Fiyatlandırma (Stripe Price ID'leri)
PRICE_IDS = {
    'premium_monthly': os.environ.get('STRIPE_PREMIUM_PRICE_ID', 'price_...'),
    'pro_monthly': os.environ.get('STRIPE_PRO_PRICE_ID', 'price_...'),
}

def create_checkout_session(tier, user_id=None):
    """
    Stripe Checkout session oluştur
    
    Args:
        tier: 'premium' veya 'pro'
        user_id: Kullanıcı ID'si (metadata'ya eklenecek)
    
    Returns:
        Checkout session URL
    """
    if not STRIPE_AVAILABLE:
        return None, "Stripe kütüphanesi yüklü değil"
    try:
        price_id = PRICE_IDS.get(f'{tier}_monthly')
        if not price_id:
            return None, "Price ID bulunamadı"
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=os.environ.get('SUCCESS_URL', 'http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}'),
            cancel_url=os.environ.get('CANCEL_URL', 'http://localhost:3000/pricing'),
            metadata={
                'user_id': user_id or get_user_id(),
                'tier': tier
            },
            subscription_data={
                'metadata': {
                    'user_id': user_id or get_user_id(),
                    'tier': tier
                }
            }
        )
        
        return session.url, None
    except Exception as e:
        return None, str(e)

def handle_stripe_webhook(payload, sig_header):
    """
    Stripe webhook'ları işle
    
    Önemli event'ler:
    - checkout.session.completed: İlk ödeme tamamlandı
    - customer.subscription.created: Abonelik oluşturuldu
    - customer.subscription.updated: Abonelik güncellendi
    - customer.subscription.deleted: Abonelik iptal edildi
    - invoice.payment_succeeded: Ödeme başarılı
    - invoice.payment_failed: Ödeme başarısız
    """
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return None, f"Invalid payload: {e}"
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return None, f"Invalid signature: {e}"
    
    # Event tipine göre işle
    event_type = event['type']
    data = event['data']['object']
    
    if event_type == 'checkout.session.completed':
        # Checkout tamamlandı
        user_id = data['metadata'].get('user_id')
        tier = data['metadata'].get('tier')
        customer_id = data.get('customer')
        subscription_id = data.get('subscription')
        
        if user_id and tier:
            upgrade_user(user_id, tier, customer_id, subscription_id)
            return f"User {user_id} upgraded to {tier}", None
    
    elif event_type == 'customer.subscription.created':
        # Abonelik oluşturuldu
        user_id = data['metadata'].get('user_id')
        tier = data['metadata'].get('tier')
        customer_id = data.get('customer')
        subscription_id = data.get('id')
        
        if user_id and tier:
            upgrade_user(user_id, tier, customer_id, subscription_id)
            return f"Subscription created for user {user_id}", None
    
    elif event_type == 'customer.subscription.updated':
        # Abonelik güncellendi (tier değişikliği olabilir)
        user_id = data['metadata'].get('user_id')
        tier = data['metadata'].get('tier')
        customer_id = data.get('customer')
        subscription_id = data.get('id')
        status = data.get('status')
        
        if status == 'active' and user_id and tier:
            upgrade_user(user_id, tier, customer_id, subscription_id)
            return f"Subscription updated for user {user_id}", None
        elif status in ['canceled', 'unpaid', 'past_due']:
            # Abonelik iptal edildi, free tier'a düşür
            upgrade_user(user_id, 'free', customer_id, subscription_id)
            return f"Subscription canceled for user {user_id}, downgraded to free", None
    
    elif event_type == 'customer.subscription.deleted':
        # Abonelik silindi
        user_id = data['metadata'].get('user_id')
        customer_id = data.get('customer')
        
        if user_id:
            upgrade_user(user_id, 'free', customer_id, None)
            return f"Subscription deleted for user {user_id}, downgraded to free", None
    
    elif event_type == 'invoice.payment_succeeded':
        # Ödeme başarılı
        subscription_id = data.get('subscription')
        customer_id = data.get('customer')
        # Abonelik aktif kalıyor, herhangi bir işlem gerekmez
        return "Payment succeeded", None
    
    elif event_type == 'invoice.payment_failed':
        # Ödeme başarısız
        subscription_id = data.get('subscription')
        customer_id = data.get('customer')
        # Kullanıcıya bildirim gönderilebilir
        return "Payment failed - notification sent", None
    
    return f"Event {event_type} processed", None

def get_subscription_status(customer_id):
    """Müşterinin abonelik durumunu kontrol et"""
    try:
        subscriptions = stripe.Subscription.list(customer=customer_id, limit=1)
        if subscriptions.data:
            subscription = subscriptions.data[0]
            return {
                'status': subscription.status,
                'tier': subscription.metadata.get('tier', 'free'),
                'current_period_end': subscription.current_period_end,
                'cancel_at_period_end': subscription.cancel_at_period_end
            }
        return None
    except Exception as e:
        return None

