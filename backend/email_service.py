"""
Email Service - Basit email gönderimi
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
FROM_EMAIL = os.environ.get('FROM_EMAIL', 'noreply@universitymathai.com')

def send_email(to_email, subject, body, html_body=None):
    """
    Email gönder
    
    Args:
        to_email: Alıcı email adresi
        subject: Email konusu
        body: Email metni
        html_body: HTML formatında email içeriği (opsiyonel)
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        return False, "SMTP credentials not configured"
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        
        msg.attach(MIMEText(body, 'plain'))
        
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        
        return True, "Email sent successfully"
    except Exception as e:
        return False, str(e)

def send_welcome_email(user_email, user_name):
    """Hoşgeldin emaili gönder"""
    subject = "University Match AI'a Hoşgeldiniz!"
    body = f"""
    Merhaba {user_name},
    
    University Match AI'a hoşgeldiniz!
    
    Şimdi üniversite eşleştirme sistemimizi kullanarak sizin için en uygun programları keşfedebilirsiniz.
    
    İyi eğitimler!
    University Match AI Team
    """
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h1 style="color: #4F46E5;">University Match AI'a Hoşgeldiniz!</h1>
        <p>Merhaba <strong>{user_name}</strong>,</p>
        <p>University Match AI'a hoşgeldiniz!</p>
        <p>Şimdi üniversite eşleştirme sistemimizi kullanarak sizin için en uygun programları keşfedebilirsiniz.</p>
        <p>İyi eğitimler!</p>
        <p style="color: #666;">University Match AI Team</p>
    </body>
    </html>
    """
    return send_email(user_email, subject, body, html_body)

def send_upgrade_confirmation(user_email, user_name, tier):
    """Tier yükseltme onayı emaili gönder"""
    subject = f"University Match AI - {tier.title()} Tier'a Yükseltildiniz!"
    body = f"""
    Merhaba {user_name},
    
    Hesabınız başarıyla {tier.title()} tier'a yükseltildi!
    
    Artık tüm premium özelliklerden yararlanabilirsiniz.
    
    Teşekkürler,
    University Match AI Team
    """
    return send_email(user_email, subject, body)
