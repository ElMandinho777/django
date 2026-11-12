import React from "react";
import { Link } from "react-router-dom";
import { Button } from "semantic-ui-react";

export function Error404() {
  return (
    <div style={{ textAlign: "center", padding: "100px 20px" }}>
      <h1>Error 404</h1>
      <p>Página no encontrada</p>
      <Link to="/login">
        <Button primary>Volver al Login</Button>
      </Link>
    </div>
  );
}
