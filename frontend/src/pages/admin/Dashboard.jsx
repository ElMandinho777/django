import React, { useState, useEffect } from "react";
import { Button, Loader, Dimmer } from "semantic-ui-react";
import { useAuth } from "../../hooks/useAuth";

export function Dashboard() {
  const { logout, auth } = useAuth();
  const user = auth?.me || {};

  // Widget de API de Terceros (Frase célebre / motivadora)
  const [quote, setQuote] = useState(null);
  const [loadingQuote, setLoadingQuote] = useState(true);

  const fetchThirdPartyApi = async () => {
    setLoadingQuote(true);
    try {
      // Consumo de API de terceros pública y gratuita (DummyJSON Quotes)
      const res = await fetch("https://dummyjson.com/quotes/random");
      const data = await res.json();
      setQuote(data);
    } catch (err) {
      console.error("Error al consumir API de terceros:", err);
      setQuote({
        quote: "El éxito es la suma de pequeños esfuerzos repetidos cada día.",
        author: "Robert Collier",
      });
    } finally {
      setLoadingQuote(false);
    }
  };

  useEffect(() => {
    fetchThirdPartyApi();
  }, []);

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>CentiStore Dashboard</h1>
        <div className="user-badge">
          <div className="user-info">
            <div className="user-email">{user.email || user.username}</div>
            <div className="user-status">Sesión activa (JWT)</div>
          </div>
          <Button color="red" size="small" onClick={logout}>
            Cerrar Sesión
          </Button>
        </div>
      </header>

      <main className="dashboard-content">
        {/* Panel 1: Datos del usuario autenticado (AuthContext + Web Service Propio) */}
        <section className="card-panel">
          <h3>
            👤 Datos del Usuario Autenticado
          </h3>
          <p>Información devuelta por el servicio protegido <code>/api/v1/auth/me/</code>:</p>
          <div className="info-row">
            <span>ID:</span>
            <strong>{user.id || 1}</strong>
          </div>
          <div className="info-row">
            <span>Usuario:</span>
            <strong>{user.username}</strong>
          </div>
          <div className="info-row">
            <span>Correo:</span>
            <strong>{user.email}</strong>
          </div>
          <div className="info-row">
            <span>Teléfono:</span>
            <strong>{user.telefono || "No registrado"}</strong>
          </div>
          <div className="info-row">
            <span>Rol Staff:</span>
            <strong>{user.is_staff ? "Administrador" : "Cliente"}</strong>
          </div>
          <div className="info-row">
            <span>Cuenta Activa:</span>
            <strong style={{ color: user.is_active ? "green" : "red" }}>
              {user.is_active ? "Sí (Verificado)" : "No"}
            </strong>
          </div>
        </section>

        {/* Panel 2: Widget de API de Terceros (Parte 2: Requisitos) */}
        <section className="card-panel widget-panel">
          <h3>
            🌐 Widget: API de Terceros (Frase Inspiracional)
          </h3>
          <p>Datos obtenidos en tiempo real mediante <code>fetch()</code> a la API externa:</p>

          {loadingQuote ? (
            <div style={{ height: "100px", position: "relative" }}>
              <Dimmer active inverted>
                <Loader inverted>Cargando API externa...</Loader>
              </Dimmer>
            </div>
          ) : (
            <div className="quote-box">
              <blockquote>"{quote?.quote}"</blockquote>
              <cite>— {quote?.author}</cite>
            </div>
          )}

          <Button
            size="tiny"
            basic
            color="teal"
            onClick={fetchThirdPartyApi}
            disabled={loadingQuote}
          >
            🔄 Actualizar Frase
          </Button>

          <div>
            <span className="api-badge">API Externa: DummyJSON Quotes API (REST/JSON)</span>
          </div>
        </section>

        {/* Panel 3: Resumen de Servicios */}
        <section className="card-panel" style={{ borderTopColor: "#21ba45", gridColumn: "1 / -1" }}>
          <h3>
            ⚙️ Arquitectura Full Stack y Web Services Integrados
          </h3>
          <p>Este sistema implementa la arquitectura completa solicitada para el RA2:</p>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "15px", marginTop: "15px" }}>
            <div style={{ background: "#f9fafb", padding: "12px 16px", borderRadius: "8px" }}>
              <strong>1. Frontend en React (Vite)</strong>
              <p style={{ margin: "5px 0 0", fontSize: "13px" }}>React Router v6, Formik, Yup, Semantic UI, SASS y persistencia de sesión con AuthContext.</p>
            </div>
            <div style={{ background: "#f9fafb", padding: "12px 16px", borderRadius: "8px" }}>
              <strong>2. Web Service Propio (DRF + JWT)</strong>
              <p style={{ margin: "5px 0 0", fontSize: "13px" }}>Autenticación JWT con SimpleJWT, endpoints de login, registro público y consulta protegida <code>/auth/me/</code>.</p>
            </div>
            <div style={{ background: "#f9fafb", padding: "12px 16px", borderRadius: "8px" }}>
              <strong>3. Web Service SOAP (Django + Zeep)</strong>
              <p style={{ margin: "5px 0 0", fontSize: "13px" }}>Consumo de servicio SOAP público CountryInfoService mediante <code>/api/v1/soap/country/</code>.</p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
