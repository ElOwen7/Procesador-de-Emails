import imaplib
import email
import os
import pandas as pd
import polars as pl
from dotenv import load_dotenv
from email.header import decode_header
from email.utils import parseaddr
from datetime import datetime, timedelta
import streamlit as st
from io import BytesIO

# -----------------------------------
load_dotenv()
USER_MAIL = os.getenv("USER_MAIL")
PASSWORD = os.getenv("PASSWORD_APP")

CARPETA_ADJUNTOS = 'Adjuntos'
if not os.path.exists(CARPETA_ADJUNTOS):
    os.makedirs(CARPETA_ADJUNTOS)

st.set_page_config(page_title="Procesador de Correos", layout="wide")
st.title("📥 Procesador de Correos de Vacantes")

# Inputs del usuario
filtro_asunto = st.text_input("🔍 Filtro de asunto", value="VACANTE")
fecha_desde = st.date_input("📅 Fecha desde", value=datetime.now() - timedelta(days=7))

# Procesar correos
if st.button("🔄 Procesar correos"):
    st.info("Conectando con Gmail y procesando correos...")

    datos = []

    with imaplib.IMAP4_SSL('imap.gmail.com') as imap:
        imap.login(USER_MAIL, PASSWORD)
        imap.select('inbox')

        result, data = imap.search(None, 'ALL')
        email_ids = data[0].split()

        progress = st.progress(0)
        total = len(email_ids)

        for idx, email_id in enumerate(email_ids):
            result, data = imap.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            remitente = msg.get('From')
            nombre_remitente, email_remitente = parseaddr(remitente)

            subject = decode_header(msg['Subject'])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode(errors='ignore')

            date_str = msg['Date']
            try:
                parsed_date = email.utils.parsedate_to_datetime(date_str)
                parsed_date = parsed_date.replace(tzinfo=None) if parsed_date else None
            except Exception:
                parsed_date = None

            if filtro_asunto.lower() not in subject.lower():
                continue
            if parsed_date is None or parsed_date.date() < fecha_desde:
                continue

            body = ""
            archivo_adjunto = None

            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    try:
                        body = part.get_payload(decode=True).decode(errors='ignore')
                    except Exception:
                        continue

                if part.get_content_disposition() == 'attachment':
                    try:
                        filename = part.get_filename()
                        if filename:
                            decoded_filename = decode_header(filename)[0][0]
                            if isinstance(decoded_filename, bytes):
                                decoded_filename = decoded_filename.decode(errors='ignore')

                            if decoded_filename.lower().endswith(('.pdf', '.doc', '.docx')):
                                filepath = os.path.join(CARPETA_ADJUNTOS, decoded_filename)
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                archivo_adjunto = filepath
                    except Exception:
                        continue

            datos.append({
                "Cod_Vacante": subject,
                "date": parsed_date,
                "body": body.strip(),
                "from_email": email_remitente,
                "attachment_name": os.path.basename(archivo_adjunto) if archivo_adjunto else None,
                "attachment_path": archivo_adjunto
            })

            progress.progress((idx + 1) / total)

    if datos:
        df = pd.DataFrame(datos)
        st.session_state["df_correo"] = df  # Guarda el DataFrame
        st.success("✅ Correos procesados correctamente.")
    else:
        st.warning("⚠️ No se encontraron correos que coincidan con el filtro.")

# Mostrar resultados si existen
if "df_correo" in st.session_state:
    df = st.session_state["df_correo"]
    st.subheader("📋 Resultados")
    st.dataframe(df.drop(columns=["attachment_path"]), use_container_width=True)

    # Descargar CSV (sin ruta, solo nombre del archivo)
    df_csv = df.drop(columns=["attachment_path"])
    csv = df_csv.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Descargar CSV", data=csv, file_name="correos_filtrados.csv", mime="text/csv")

    # Descargar adjuntos individuales
    st.subheader("📎 Archivos Adjuntos")
    for i, row in df.iterrows():
        if row["attachment_path"] and os.path.exists(row["attachment_path"]):
            with open(row["attachment_path"], "rb") as f:
                bytes_data = f.read()
            st.download_button(
                label=f"📄 Descargar {row['attachment_name']}",
                data=BytesIO(bytes_data),
                file_name=row["attachment_name"],
                mime="application/octet-stream",
                key=f"adjunto_{i}"
            )
