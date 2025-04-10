from mcp.server.fastmcp import FastMCP
import imaplib
import email
from email.header import decode_header
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mcp = FastMCP("Meuservidormcp")

def fetch_emails(remetente, senha, quantidade=10, remetente_filtro=None, palavras=None, data_inicio=None, data_fim=None):
    """ Conecta ao Gmail via IMAP e busca emails com filtros """
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(remetente, senha)
        mail.select("inbox")

        criteria = []
        if remetente_filtro:
            criteria.append(f'FROM "{remetente_filtro}"')
        if palavras:
            criteria.append(f'BODY "{palavras}"')
        if data_inicio and data_fim:
            criteria.append(f'SINCE {data_inicio.strftime("%d-%b-%Y")} BEFORE {data_fim.strftime("%d-%b-%Y")}')

        search_criteria = " ".join(criteria) if criteria else "ALL"
        status, messages = mail.search(None, search_criteria)
        email_ids = messages[0].split()

        emails = []
        for email_id in email_ids[-quantidade:]:  
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')
            emails.append(subject)

        mail.logout()
        return emails
    except Exception as e:
        print(f"Erro ao buscar emails: {e}")
        return []

def send_email(remetente, senha, destinatario, assunto, corpo):
    """ Envia um email usando SMTP """
    try:

        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto
        msg.attach(MIMEText(corpo, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  
            server.login(remetente, senha)  
            server.send_message(msg)  

        print("Email enviado com sucesso!")
        return {"status": "success", "message": "Email enviado com sucesso!"}
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return {"status": "error", "message": str(e)}
    
@mcp.tool("fetch_emails_tool")
async def fetch_emails_tool(remetente: str, senha: str, quantidade: int = 10, remetente_filtro: str = None, palavras: str = None, data_inicio: str = None, data_fim: str = None):
    """ Tool para buscar emails via IMAP com filtros """
    data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d") if data_inicio else None
    data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d") if data_fim else None

    emails = fetch_emails(remetente, senha, quantidade, remetente_filtro, palavras, data_inicio_dt, data_fim_dt)
    return {"emails": emails}

@mcp.tool("send_email_tool")
async def send_email_tool(remetente: str, senha: str, destinatario: str, assunto: str, corpo: str):
    """ Tool para enviar email via SMTP """
    result = send_email(remetente, senha, destinatario, assunto, corpo)
    return result

if __name__ == "__main__":
    mcp.run()
