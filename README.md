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


💻 ¿Qué puede hacer el usuario desde la interfaz?
- 1) Ingresar una palabra clave del asunto y una fecha mínima.

- 2) Procesar los correos con un botón.

- 3) Ver los resultados en una tabla.

- 4) Descargar un ZIP que incluye el CSV + todos los archivos adjuntos.

