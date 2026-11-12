# CentiStore API

Adaptacion del proyecto de productos y categorias de la Unidad 1 para la practica del manual Desarrollo Full Stack con Django y ReactJS, paginas 5 a 12.
Tema: tienda de videojuegos y accesorios. Se conserva products, su filtro, servicios y pruebas; se agrega users.

## Instalacion
```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```
Escribe una clave Django aleatoria en .env antes de ejecutar. Puedes generarla con `python -c "import secrets; print(secrets.token_urlsafe(50))"`.
```powershell
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py createsuperuser
.\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8002 --insecure
```
Abre http://127.0.0.1:8002/swagger/ . --insecure solo sirve archivos estaticos en desarrollo local; no publicar con runserver.

## Orden del manual
1. Proyecto centistore y entorno virtual reutilizando products.
2. DRF y drf-yasg registrados en settings; Swagger y ReDoc en urls.
3. App users y AUTH_USER_MODEL antes de migrar la base nueva.
4. Usuario AbstractUser, email unico como USERNAME_FIELD y telefono adicional.
5. Admin con formularios seguros para crear y editar usuarios.
6. UserSerializer y CRUD administrativo /api/v1/users/.
7. Creacion segura con set_password y actualizacion sin sustituir el hash si no se envia password.
8. Datos personales en /api/v1/auth/me/.
9. SimpleJWT: /api/v1/auth/token/ y /api/v1/auth/token/refresh/.

## Seguridad
El campo password es write_only. Las respuestas y el esquema de lectura no lo contienen.
PUT y PATCH cambian la contrasena solo cuando se envia una nueva valida.
CRUD de usuarios exclusivo para staff; /auth/me/ requiere autenticacion.
JWT access: 30 minutos. Refresh: 1 dia. Swagger Authorize: `Bearer TOKEN_ACCESS`.
Telefono: 10 a 14 digitos y + opcional. Correo unico normalizado a minusculas.
No se publican base de datos, entorno, .env ni credenciales de demostracion.

## Base de datos
Se usa una base SQLite nueva como en el manual, porque cambiar AUTH_USER_MODEL sobre la base antigua requiere una migracion adicional. No se borro ni modifico la base MySQL del proyecto original. Se reutilizo su codigo y pruebas; los registros de demostracion son nuevos.

## Pruebas
```powershell
.\venv\Scripts\python.exe manage.py test
```
Las pruebas incluyen un administrador que modifica otro usuario, con contrasenas diferentes, y comprueban que PATCH y PUT sin password conservan exactamente el hash y el acceso original. Tambien comprueban que no hay password en crear, listar, consultar, editar ni datos personales; roles; expiracion JWT; telefono; login con email; cambio explicito y rechazo de password vacio.
