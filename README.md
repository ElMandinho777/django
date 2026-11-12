# CentiStore - Arquitectura Full Stack Django REST + React

Proyecto integral que combina un Backend en **Django REST Framework (DRF)** y un Frontend desarrollado en **React con Vite**, integrando autenticación por JSON Web Tokens (JWT), consumo de APIs REST de terceros y un Web Service SOAP público.

Desarrollado con base en las **páginas 13 a 35** del manual de Desarrollo Full Stack con Django y ReactJS.

---

## 🚀 Requisitos Previos

- **Python:** 3.10 o superior
- **Node.js:** 18 o superior con `npm`
- **Git**

---

## 🛠️ Instalación y Puesta en Marcha

### 1. Clonar el repositorio
```bash
git clone https://github.com/ElMandinho777/django.git
cd django
```

---

### 2. Configurar y Ejecutar el Backend (Django)

```bash
cd backend

# Crear entorno virtual (si no existe)
python -m venv venv

# Activar el entorno virtual
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# En Linux/macOS:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Iniciar servidor de desarrollo
python manage.py runserver 127.0.0.1:8000
```

El backend estará disponible en:
- **API Swagger / Documentación:** `http://127.0.0.1:8000/swagger/`
- **Administrador de Django:** `http://127.0.0.1:8000/admin/`
- **Endpoint Web Service SOAP:** `http://127.0.0.1:8000/api/v1/soap/country/?code=MX`

---

### 3. Configurar y Ejecutar el Frontend (React + Vite)

En una nueva terminal:

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará accesible en `http://localhost:5173/`.

---

## 👤 Credenciales de Demostración

| Tipo | Correo Electrónico | Contraseña | Rol |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin@centistore.example` | `mH1J-n9MMUlx_aL70UbzgZBP!7a` | Administrador (Staff) |
| **Cliente** | `cliente@centistore.example` | `CDq5NilAMA5mSxL1RwioupwP!7a` | Cliente regular |

También es posible crear un nuevo usuario desde la vista de registro en `http://localhost:5173/register`.

---

## 📦 Estructura del Proyecto

```text
RDA-P2/
├── backend/
│   ├── centistore/          # Configuración principal, settings, urls, wsgi
│   ├── users/               # Modelos de usuario, serializers, vistas JWT, registro y SOAP
│   ├── products/            # Catálogo y lógica de productos
│   ├── requirements.txt     # Dependencias del Backend
│   ├── .gitignore           # Excluye venv, db.sqlite3, .env
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── api/             # Consumo de endpoints de Django (login, registro, auth/me)
│   │   ├── context/         # AuthContext (persistencia de sesión con JWT)
│   │   ├── hooks/           # Custom hooks: useAuth, useUser
│   │   ├── layouts/         # AdminLayout, ClientLayout, CommonLayout
│   │   ├── pages/           # Dashboard (con widget API terceros), Login, Register, Home
│   │   ├── routes/          # Enrutamiento con React Router v6
│   │   └── App.scss         # Estilos SASS y personalización de Semantic UI
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
└── README.md
```

---

## 🌐 Servicios Web Implementados

1. **Web Service Propio (DRF + SimpleJWT):**
   - `POST /api/v1/auth/token/`: Obtención de par de tokens (Access y Refresh).
   - `POST /api/v1/auth/register/`: Registro público de nuevos usuarios con contraseña hasheada.
   - `GET /api/v1/auth/me/`: Consulta protegida con Bearer Token de los datos del usuario logueado.
2. **API de Terceros (Frontend):**
   - Consumo de **DummyJSON Quotes API** (`https://dummyjson.com/quotes/random`) dentro del Dashboard protegido mediante `fetch()`.
3. **Web Service SOAP (Backend con Zeep):**
   - `GET /api/v1/soap/country/?code=MX`: Endpoint en Django que consume el servicio público SOAP WSDL `CountryInfoService` retornando datos normalizados en JSON.
