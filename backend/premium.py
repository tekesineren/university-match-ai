"""
Premium özellikler ve kullanıcı yönetimi
Rate limiting, tier kontrolü, API key yönetimi
"""

import json
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

# Basit JSON dosyası ile kullanıcı veritabanı (production'da gerçek DB kullan)
USERS_FILE = 'users.json'
API_KEYS_FILE = 'api_keys.json'

# Tier limitleri
TIER_LIMITS = {
    'free': {
        'requests_per_day': 5,
        'cv_analyses_per_month': 1,
        'api_access': False,
        'priority_support': False
    },
    'premium': {
        'requests_per_day': 100,
        'cv_analyses_per_month': -1,  # -1 = sınırsız
        'api_access': False,
        'priority_support': True
    },
    'pro': {
        'requests_per_day': -1,  # -1 = sınırsız
        'cv_analyses_per_month': -1,
        'api_access': True,
        'priority_support': True
    }
}

def load_users():
    """Kullanıcı veritabanını yükle"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Kullanıcı veritabanını kaydet"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def load_api_keys():
    """API key'leri yükle"""
    if os.path.exists(API_KEYS_FILE):
        with open(API_KEYS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_api_keys(api_keys):
    """API key'leri kaydet"""
    with open(API_KEYS_FILE, 'w', encoding='utf-8') as f:
        json.dump(api_keys, f, indent=2, ensure_ascii=False)

def get_user_id():
    """Request'ten kullanıcı ID'sini al (API key veya session'dan)"""
    # Önce API key kontrolü
    api_key = request.headers.get('X-API-Key') or request.headers.get('Authorization', '').replace('Bearer ', '')
    if api_key:
        api_keys = load_api_keys()
        if api_key in api_keys:
            return api_keys[api_key]['user_id']
    
    # Session veya user_id header'dan
    user_id = request.headers.get('X-User-ID') or request.json.get('user_id') if request.is_json else None
    
    # Yoksa IP adresini kullan (basit tracking için)
    if not user_id:
        user_id = request.remote_addr
    
    return user_id

def get_user_tier(user_id):
    """Kullanıcının tier'ını al"""
    users = load_users()
    if user_id in users:
        return users[user_id].get('tier', 'free')
    return 'free'

def update_user_usage(user_id, endpoint='match'):
    """Kullanıcı kullanımını güncelle"""
    users = load_users()
    
    if user_id not in users:
        users[user_id] = {
            'tier': 'free',
            'created_at': datetime.now().isoformat(),
            'usage': {
                'requests_today': 0,
                'last_request_date': None,
                'cv_analyses_this_month': 0,
                'last_cv_analysis_month': None
            }
        }
    
    user = users[user_id]
    usage = user['usage']
    today = datetime.now().date().isoformat()
    current_month = datetime.now().strftime('%Y-%m')
    
    # Günlük request sayısını güncelle
    if usage['last_request_date'] != today:
        usage['requests_today'] = 0
        usage['last_request_date'] = today
    
    usage['requests_today'] += 1
    
    # CV analizi sayısını güncelle
    if endpoint == 'parse-cv':
        if usage['last_cv_analysis_month'] != current_month:
            usage['cv_analyses_this_month'] = 0
            usage['last_cv_analysis_month'] = current_month
        usage['cv_analyses_this_month'] += 1
    
    save_users(users)

def check_rate_limit(user_id, endpoint='match'):
    """Rate limit kontrolü"""
    tier = get_user_tier(user_id)
    limits = TIER_LIMITS[tier]
    users = load_users()
    
    if user_id not in users:
        return True, None  # İlk kullanım, limit yok
    
    user = users[user_id]
    usage = user['usage']
    today = datetime.now().date().isoformat()
    current_month = datetime.now().strftime('%Y-%m')
    
    # Günlük request limiti
    if limits['requests_per_day'] != -1:
        if usage['last_request_date'] == today:
            if usage['requests_today'] >= limits['requests_per_day']:
                return False, f"Günlük limit aşıldı ({limits['requests_per_day']} request/gün). Premium'a geçerek sınırsız erişim kazanın!"
        else:
            usage['requests_today'] = 0
            usage['last_request_date'] = today
    
    # Aylık CV analizi limiti
    if endpoint == 'parse-cv' and limits['cv_analyses_per_month'] != -1:
        if usage['last_cv_analysis_month'] == current_month:
            if usage['cv_analyses_this_month'] >= limits['cv_analyses_per_month']:
                return False, f"Aylık CV analizi limiti aşıldı ({limits['cv_analyses_per_month']} analiz/ay). Premium'a geçerek sınırsız analiz yapın!"
        else:
            usage['cv_analyses_this_month'] = 0
            usage['last_cv_analysis_month'] = current_month
    
    return True, None

def require_tier(min_tier='free'):
    """Tier gereksinimi decorator"""
    tier_order = {'free': 0, 'premium': 1, 'pro': 2}
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_user_id()
            tier = get_user_tier(user_id)
            
            if tier_order[tier] < tier_order[min_tier]:
                return jsonify({
                    "success": False,
                    "error": f"Bu özellik için {min_tier} tier gereklidir. Şu anki tier: {tier}",
                    "upgrade_required": True,
                    "current_tier": tier,
                    "required_tier": min_tier
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def rate_limit(f):
    """Rate limiting decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_user_id()
        endpoint = request.endpoint or 'match'
        
        # Rate limit kontrolü
        allowed, error_msg = check_rate_limit(user_id, endpoint)
        if not allowed:
            return jsonify({
                "success": False,
                "error": error_msg,
                "rate_limit_exceeded": True,
                "upgrade_url": "/pricing"
            }), 429
        
        # Kullanımı güncelle
        update_user_usage(user_id, endpoint)
        
        return f(*args, **kwargs)
    return decorated_function

def upgrade_user(user_id, tier, stripe_customer_id=None, subscription_id=None):
    """Kullanıcı tier'ını yükselt"""
    users = load_users()
    
    if user_id not in users:
        users[user_id] = {
            'tier': tier,
            'created_at': datetime.now().isoformat(),
            'stripe_customer_id': stripe_customer_id,
            'subscription_id': subscription_id,
            'upgraded_at': datetime.now().isoformat(),
            'usage': {
                'requests_today': 0,
                'last_request_date': None,
                'cv_analyses_this_month': 0,
                'last_cv_analysis_month': None
            }
        }
    else:
        users[user_id]['tier'] = tier
        users[user_id]['upgraded_at'] = datetime.now().isoformat()
        if stripe_customer_id:
            users[user_id]['stripe_customer_id'] = stripe_customer_id
        if subscription_id:
            users[user_id]['subscription_id'] = subscription_id
    
    save_users(users)

def create_api_key(user_id, key_name='default'):
    """API key oluştur (Pro tier için)"""
    import secrets
    api_key = f"maa_{secrets.token_urlsafe(32)}"
    
    api_keys = load_api_keys()
    api_keys[api_key] = {
        'user_id': user_id,
        'key_name': key_name,
        'created_at': datetime.now().isoformat(),
        'last_used': None,
        'usage_count': 0
    }
    
    save_api_keys(api_keys)
    return api_key

def get_user_stats(user_id):
    """Kullanıcı istatistiklerini al"""
    users = load_users()
    if user_id not in users:
        return None
    
    user = users[user_id]
    tier = user.get('tier', 'free')
    limits = TIER_LIMITS[tier]
    usage = user.get('usage', {})
    
    return {
        'tier': tier,
        'limits': limits,
        'usage': {
            'requests_today': usage.get('requests_today', 0),
            'requests_remaining_today': limits['requests_per_day'] - usage.get('requests_today', 0) if limits['requests_per_day'] != -1 else -1,
            'cv_analyses_this_month': usage.get('cv_analyses_this_month', 0),
            'cv_analyses_remaining': limits['cv_analyses_per_month'] - usage.get('cv_analyses_this_month', 0) if limits['cv_analyses_per_month'] != -1 else -1
        },
        'created_at': user.get('created_at'),
        'upgraded_at': user.get('upgraded_at')
    }










