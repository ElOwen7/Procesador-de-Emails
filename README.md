# Procesador-de-Emails
Idealmente esta la herramienta busca automatizar el procesamiento de correos de postulantes a vacantes. Extraer sus CVs desde correos automáticamente, sin tener que entrar uno por uno a Gmail.

La aplicación en Streamlit se conecta a tu cuenta de Gmail, filtra correos por asunto y fecha, y extrae información útil de cada correo:

# 🔍 Filtrado:
- Solo procesa correos cuyo *asunto* contenga una palabra clave o codigo de vacante (como "VACANTE").

- Solo toma correos a partir de la fecha especificada, sino se ingresa una tomara los ultimos 7 días.

# 📤 Extracción de datos por correo:
- Asunto del correo (que contiene un código de vacante).

- Fecha de envío.

- Texto del cuerpo del correo.

- Correo del remitente.

- Adjunto, si contiene un archivo .pdf, .doc o .docx (se descarga localmente).


# 💻 ¿Qué puede hacer el usuario desde la interfaz?
- 1) Ingresar una palabra clave del asunto y una fecha mínima.

- 2) Procesar los correos con un botón.

- 3) Ver los resultados en una tabla.

- 4) Descargar un ZIP que incluye el CSV + todos los archivos adjuntos.

## ¿Como iniciar Sesion?
* 1- Ingresa tu direccion de correo electronico de GMAIL ejemplo(tucorreo@gmail.com)
* 2- Ingresa tu contraseña de Aplicaciones. 
 * * ¿No sabes como generearla? 
     * 1) Asegurate de tener la verificacion en 2 pasos en tu cuenta.
     * 2) Ingresa al siguiente enlace https://myaccount.google.com/apppasswords?rapt=AEjHL4OPNOmZIkj6KHhMRtMBHVOfwXP6Y_ZGAusSVDKGbMygT6kOaw-AfyGRlPACabLrrRKVzMKetZ7u-U7JoQVVXRCrYVhzt0j36KMhUuUs7vjPjTMpzqU
     * 3) Inicia sesion con tu cuenta.
     * 4) Escribe un nombre de app, y se generara tu contraseña de aplicacion, copiala y guardala en un lugar seguro.
     * 5) Vuelve a https://procesador-de-emails-v1-otp.streamlit.app/ e inicia sesión con tu correo y la contraseña que acabas de generar.
     
     


