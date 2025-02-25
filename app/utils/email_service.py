import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

def send_password_reset_email(to_email: str, reset_link: str):
    
    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("PASSWORD")
    
    subject = "Redefinição de Senha"
    body = f"Olá,\n\nClique no link abaixo para redefinir sua senha:\n{reset_link}\n\nEste link expira em 1 hora."
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
