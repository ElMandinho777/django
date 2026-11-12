import React from "react";
import { Link } from "react-router-dom";
import { Button } from "semantic-ui-react";

export function Home() {
  return (
    <div style={{ textAlign: "center", padding: "80px 20px" }}>
      <h1>CentiStore Frontend</h1>
      <p>Aplicación web full stack con React y Django REST Framework</p>
      <div style={{ marginTop: "30px" }}>
        <Link to="/login">
          <Button primary size="large">Iniciar Sesión</Button>
        </Link>
        <Link to="/register" style={{ marginLeft: "15px" }}>
          <Button secondary size="large">Registrarse</Button>
        </Link>
      </div>
    </div>
  );
}
