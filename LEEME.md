# Práctica 2: tienda online con Django

Proyecto implementado hasta la parte 5 del PDF: productos, categorías, API REST y administrador.

## Iniciar en esta computadora

1. Abre esta carpeta en Visual Studio Code.
2. Ejecuta `iniciar.cmd` (doble clic desde el Explorador de archivos).
3. Introduce el usuario de MySQL (Enter para root) y su contraseña. La contraseña no se muestra mientras escribes.
4. El asistente crea `django_api` si no existe, ejecuta las migraciones y solicita crear tu administrador.
5. Mantén la ventana abierta y visita:
   - API: http://127.0.0.1:8000/api/v1/
   - Productos: http://127.0.0.1:8000/api/v1/products/
   - Categorías: http://127.0.0.1:8000/api/v1/categories/
   - Administración: http://127.0.0.1:8000/admin/
6. Para detener el servidor, presiona Ctrl+C.

Crea primero una categoría y luego un producto asociado. Puedes hacerlo desde el administrador o desde los formularios de la API.

## Estado real de la entrega

- Entorno virtual creado y dependencias instaladas.
- Aplicaciones organizadas en BASE_APPS, THIRD_APPS y OWN_APPS.
- Modelos y serializadores de la parte 5 implementados.
- Ambos modelos registrados en el administrador.
- Rutas CRUD y migración inicial incluidas.
- Comprobación de Django sin problemas; tres pruebas automatizadas aprobadas con SQLite temporal (CRUD, categoría inexistente y administrador).
- Pendientes de tu contraseña: creación/conexión de la base MySQL, migraciones sobre MySQL, usuario administrador e inicio del servidor. No se ha verificado aún la ejecución sobre MySQL.

## Configuración

`config.local.json` se genera al conectar exitosamente. Contiene la contraseña local en texto y está excluido de Git: no lo entregues ni compartas. Puedes editarlo para corregir tus datos.

El PDF crea `django_api` pero después usa `hackathon`: aquí se utiliza `django_api` de forma consistente. También se corrige `py manage migrate` a `python manage.py migrate`. Se conserva la comprobación de compatibilidad de Django con MySQL; no se modifican las bibliotecas instaladas.

El entorno usa el Python 3.12 disponible en el runtime local de Codex, porque esta terminal no encontró `python` ni `py` en PATH. No fue necesario reinstalar Python. Si mueves el proyecto, recrea el entorno con tu propia instalación.

## Comandos manuales (PowerShell en esta carpeta)

```powershell
.\venv\Scripts\python.exe configurar.py
```

En otra computadora con Python:

```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe configurar.py
```

Repetir las pruebas sin tocar MySQL:

```powershell
$env:DJANGO_USE_SQLITE='1'
.\venv\Scripts\python.exe manage.py test
Remove-Item Env:DJANGO_USE_SQLITE
```

## Archivos principales

- `tienda_online/settings.py`: aplicaciones y conexión MySQL.
- `tienda_online/urls.py`: administración y prefijo api/v1/.
- `products/models.py`: Category y Product.
- `products/serializers.py`: conversión a JSON.
- `products/views.py`: operaciones CRUD.
- `products/urls.py`: router de la API.
- `products/admin.py`: registro de modelos.
- `products/migrations/0001_initial.py`: estructura de tablas.

Proyecto de práctica local: DEBUG está habilitado y la API permite las operaciones del tutorial sin autenticación. El servidor se enlaza únicamente a 127.0.0.1.

Referencias: https://www.django-rest-framework.org/ y https://docs.djangoproject.com/en/5.2/
