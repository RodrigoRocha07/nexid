import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def solicitacao_registro( id, usuario):
    remetente = "impulsemaxnexid@gmail.com"
    senha = "gfwaphrqllwjjjpw"
    assunto = "Solicitação de registro"
    mensagem = f"Usuario {usuario} de id: {id}, solictou registro na plataforma NexID, por favor, verifique a autenticidade do mesmo."
    destinatario = "impulsemaxnexid@gmail.com"
    # Criando a mensagem
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto

    msg.attach(MIMEText(mensagem, "plain"))

    try:
        # Conectando ao servidor SMTP do Gmail
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, msg.as_string())
        servidor.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        
def ativacao_em_analise(usuario, destinatario):
    remetente = "impulsemaxnexid@gmail.com"
    senha = "gfwaphrqllwjjjpw"
    assunto = "Solicitação de registro"
    mensagem = retorna_msg_ativacao_em_analise(usuario)
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto

    msg.attach(MIMEText(mensagem, "html"))

    try:
        # Conectando ao servidor SMTP do Gmail
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, msg.as_string())
        servidor.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


def confirmacao_registro(usuario, destinatario):
    remetente = "impulsemaxnexid@gmail.com"
    senha = "gfwaphrqllwjjjpw"
    assunto = "Solicitação de registro"
    mensagem = retorna_msg_confirmacao_registro(usuario)
    # Criando a mensagem
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto

    msg.attach(MIMEText(mensagem, "html"))

    try:
        # Conectando ao servidor SMTP do Gmail
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, msg.as_string())
        servidor.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


def retorna_msg_ativacao_em_analise(usuario):
    mensagem =  f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ativação em Análise</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                padding: 10px 0;
            }}
            .header img {{
                width: 100px;
            }}
            .content {{
                margin: 20px 0;
            }}
            .content p {{
                font-size: 16px;
                line-height: 1.5;
            }}
            .footer {{
                text-align: center;
                padding: 10px 0;
                font-size: 12px;
                color: #777777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="content">
                <h1>Ativação em Análise</h1>
                <p>Olá {usuario},</p>
                <p>Seu registro está sendo processado, em breve você receberá um e-mail de confirmação.</p>
                <p>Atenciosamente,<br>Equipe NexID</p>
            </div>
            <div class="footer">
                <p>&copy; 2025 NexID. Todos os direitos reservados.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return mensagem

def retorna_msg_confirmacao_registro(usuario):
    mensagem =  f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Confirmação de Registro</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                padding: 10px 0;
            }}
            .header img {{
                width: 100px;
            }}
            .content {{
                margin: 20px 0;
            }}
            .content p {{
                font-size: 16px;
                line-height: 1.5;
            }}
            .footer {{
                text-align: center;
                padding: 10px 0;
                font-size: 12px;
                color: #777777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="content">
                <h1>Confirmação de Registro</h1>
                <p>Olá {usuario},</p>
                <p>Seu registro foi aprovado, seja bem vindo a plataforma NexID.</p>
                <p>Atenciosamente,<br>Equipe NexID</p>
            </div>
            <div class="footer">
                <p>&copy; 2025 NexID. Todos os direitos reservados.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return mensagem