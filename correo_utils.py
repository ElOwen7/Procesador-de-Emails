import imaplib
import email
import os
from email.header import decode_header
from email.utils import parseaddr
from dotenv import load_dotenv
from datetime import datetime
import re


""" 
# Solo para ejecucion local, no en Streamlit
def cargar_configuracion():
    load_dotenv()
    user = os.getenv("USER_MAIL")
    password = os.getenv("PASSWORD_APP")
    return user, password

def conectar_gmail(user, password):
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(user, password)
    imap.select('inbox')
    return imap
"""

def conectar_gmail(user, password):
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(user, password)
    imap.select('inbox')
    return imap


def obtener_correos(imap, filtro_asunto, fecha_desde, carpeta_adjuntos="Adjuntos"):
    result, data = imap.search(None, 'ALL')
    email_ids = data[0].split()
    datos = []

    for email_id in email_ids:
        result, data = imap.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        dato = procesar_mensaje(msg, filtro_asunto, fecha_desde, carpeta_adjuntos)
        if dato:
            datos.append(dato)

    return datos

def procesar_mensaje(msg, filtro_asunto, fecha_desde, carpeta_adjuntos):
    from_email = parseaddr(msg.get("From"))[1]
    subject_raw = decode_header(msg.get("Subject", ""))[0][0]
    subject = subject_raw.decode(errors="ignore") if isinstance(subject_raw, bytes) else subject_raw

    try:
        parsed_date = email.utils.parsedate_to_datetime(msg['Date']).replace(tzinfo=None)
    except:
        parsed_date = None

    if filtro_asunto.lower() not in subject.lower() or (parsed_date and parsed_date.date() < fecha_desde):
        return None

    body = ""
    attachment_path = None
    attachment_name = None

    for part in msg.walk():
        ctype = part.get_content_type()
        if ctype == "text/plain":
            try:
                body = part.get_payload(decode=True).decode(errors='ignore')
            except:
                continue

        if part.get_content_disposition() == 'attachment':
            attachment_path, attachment_name = guardar_adjunto(part, carpeta_adjuntos)

    return {
        "Cod_Vacante": subject,
        "date": parsed_date,
        "body": body.strip(),
        "from_email": from_email,
        "attachment_name": attachment_name,
        "attachment_path": attachment_path
    }

def guardar_adjunto(part, carpeta_adjuntos):
    filename_raw = decode_header(part.get_filename())[0][0]
    filename = filename_raw.decode(errors='ignore') if isinstance(filename_raw, bytes) else filename_raw

    if filename.lower().endswith(('.pdf', '.doc', '.docx')):
        if not os.path.exists(carpeta_adjuntos):
            os.makedirs(carpeta_adjuntos)
        filepath = os.path.join(carpeta_adjuntos, filename)
        with open(filepath, "wb") as f:
            f.write(part.get_payload(decode=True))
        return filepath, filename
    return None, None
