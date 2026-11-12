import React from "react";
import { Button, Form } from "semantic-ui-react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";
import { Link, useNavigate } from "react-router-dom";
import { registerApi } from "../../api/user";

export function Register() {
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: {
      username: "",
      email: "",
      password: "",
      password_confirm: "",
    },
    validationSchema: Yup.object({
      username: Yup.string()
        .required("El username es obligatorio")
        .matches(/^\S*$/, "El username no debe contener espacios"),
      email: Yup.string()
        .email("Correo electrónico no válido")
        .required("El correo electrónico es obligatorio"),
      password: Yup.string()
        .required("La contraseña es obligatoria")
        .min(8, "La contraseña debe tener al menos 8 caracteres"),
      password_confirm: Yup.string()
        .required("La confirmación de contraseña es obligatoria")
        .oneOf([Yup.ref("password"), null], "Las contraseñas no coinciden"),
    }),
    onSubmit: async (formValues) => {
      try {
        const { password_confirm, ...data } = formValues;
        await registerApi(data);
        toast.success("Usuario registrado exitosamente. Ahora puedes iniciar sesión.");
        navigate("/login");
      } catch (error) {
        toast.error(error.message);
      }
    },
  });

  return (
    <div className="register-admin">
      <div className="register-admin__content">
        <h1>Crear Cuenta</h1>
        <Form className="register-form-admin" onSubmit={formik.handleSubmit}>
          <div className="field">
            <label>Nombre de Usuario</label>
            <Form.Input
              name="username"
              placeholder="juan_perez"
              value={formik.values.username}
              onChange={(e) => {
                const val = e.target.value.replace(/\s+/g, "");
                formik.setFieldValue("username", val);
              }}
              onBlur={formik.handleBlur}
              error={formik.touched.username && formik.errors.username}
            />
          </div>
          <div className="field">
            <label>Correo Electrónico</label>
            <Form.Input
              name="email"
              placeholder="correo@ejemplo.com"
              value={formik.values.email}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.email && formik.errors.email}
            />
          </div>
          <div className="field">
            <label>Contraseña</label>
            <Form.Input
              name="password"
              type="password"
              placeholder="Al menos 8 caracteres"
              value={formik.values.password}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.password && formik.errors.password}
            />
          </div>
          <div className="field">
            <label>Confirmar Contraseña</label>
            <Form.Input
              name="password_confirm"
              type="password"
              placeholder="Repite tu contraseña"
              value={formik.values.password_confirm}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.password_confirm && formik.errors.password_confirm}
            />
          </div>
          <Button type="submit" content="Registrar Usuario" primary fluid loading={formik.isSubmitting} />
        </Form>
        <div className="auth-links">
          ¿Ya tienes cuenta? <Link to="/login">Inicia sesión</Link>
        </div>
      </div>
    </div>
  );
}
