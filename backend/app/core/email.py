import smtplib
import ssl
from email.mime.text import MIMEText
from email.header import Header
from app.core.config import settings


def send_verify_code_email(to_email: str, code: str) -> bool:
    """发送验证码邮件（QQ邮箱SMTP）"""
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print("SMTP 未配置，跳过发送")
        return False

    subject = "西华师范数智瞭望系统 - 注册验证码"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 500px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
            <h2 style="color: #3a86ff;">欢迎使用数智瞭望系统</h2>
            <p>您的注册验证码为：</p>
            <div style="background: #f5f5f5; padding: 15px; border-radius: 6px; text-align: center; margin: 20px 0;">
                <span style="font-size: 28px; font-weight: bold; color: #3a86ff; letter-spacing: 8px;">{code}</span>
            </div>
            <p style="color: #666; font-size: 12px;">验证码 5 分钟内有效，请勿泄露给他人。</p>
            <p style="color: #999; font-size: 12px; margin-top: 20px;">如非本人操作，请忽略此邮件。</p>
        </div>
    </body>
    </html>
    """

    msg = MIMEText(body, "html", "utf-8")
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = Header(subject, "utf-8")

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context, timeout=10) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM, [to_email], msg.as_string())
        return True
    except Exception as e:
        print(f"发送邮件失败: {e}")
        return False
