# Despliegue en Render

No necesitas definir de antemano qué productos habrá ni crear tablas a mano. Al iniciar, la aplicación crea las tablas `products` y `admin` a partir de [models.py](models.py); después agregas los productos desde el panel de administración.

La SQLite local sirve para desarrollo, pero Render puede borrar sus archivos al reiniciar o desplegar. Para persistir los productos:

1. Crea una base PostgreSQL en Render. El nombre de la base puede ser `onixz`; Render genera usuario y contraseña. No agregues filas ni productos manualmente.
2. En las variables de entorno del servicio web, agrega `DATABASE_URL` y pega el valor **Internal Database URL** que Render muestra para esa base. No inventes ni publiques esa URL.
3. Agrega `SECRET_KEY` con un valor aleatorio privado. Puedes generarlo localmente con `python -c "import secrets; print(secrets.token_hex(32))"` y pegar el resultado en Render.
4. Para persistir imágenes, conecta un disco al servicio web con punto de montaje `/var/data` y configura `UPLOAD_FOLDER` con el valor `/var/data/products`.
5. Vuelve a desplegar. Al arrancar con esa base vacía, la app crea las tablas y el administrador inicial (`admin` / `onixz`); cambia esa contraseña desde el panel.

La app acepta las URLs `postgres://` y `postgresql://` de Render. No guardes URLs ni claves en Git. Cambiar a una base nueva no copia los productos de SQLite, y `db.create_all()` no migra ni recupera los datos anteriores.