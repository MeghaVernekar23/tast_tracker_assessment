// src/Login.js
import { useState } from "react";
import { apiRequest } from "../utils/Apirequest";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { AlertMessage } from "../utils/Alert";
import { InputFormModal } from "../utils/FormModal";
import { Modal } from "bootstrap";

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [signupData, setSignupData] = useState({
    user_name: "",
    user_email: "",
    user_phone_no: "",
    user_address: "",
    user_password: "",
  });

  const [alert, setAlert] = useState({
    show: false,
    message: "",
    type: "success",
  });

  const showAlert = (message, type = "success") => {
    setAlert({
      show: true,
      message: message,
      type: type,
    });

    setTimeout(() => {
      setAlert({
        show: false,
        message: "",
        type: "success",
      });
    }, 2000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const data = await apiRequest({
        url: "http://localhost:8000/users/login",
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      console.log("Login successful:", data);

      const user_email = await apiRequest({
        url: "http://localhost:8000/users/me",
        method: "GET",
        headers: {
          Authorization: `Bearer ${data.access_token}`,
        },
      });

      localStorage.setItem("current_user", JSON.stringify(user_email));
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("token_type", data.token_type);
      showAlert("Login Successful !!", "success");

      navigate("/dashboard");
    } catch (error) {
      console.error("Error during login:", error);
      showAlert(
        "Error occured while login. Please check user email and password"
      );
    }
  };

  const handleSignupChange = (e) => {
    setSignupData({ ...signupData, [e.target.name]: e.target.value });
  };

  const handleSignupSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiRequest({
        url: "http://localhost:8000/users/signup",
        method: "POST",
        body: {
          user_name: signupData.user_name,
          user_email: signupData.user_email,
          user_phone_no: signupData.user_phone_no,
          user_address: signupData.user_address,
          user_password: signupData.user_password,
        },
      });

      clearSignupForm();
      closeModal("signupModal");
      showAlert("User Created Successfully!");
    } catch {
      showAlert("User email already exist. Login instead!");
    }
  };

  const closeModal = (modalId) => {
    const modalElement = document.getElementById(modalId);
    const modalInstance = Modal.getOrCreateInstance(modalElement);
    modalInstance.hide();

    const modalBackdrop = document.querySelector(".modal-backdrop");
    if (modalBackdrop) {
      modalBackdrop.remove();
    }
  };

  const clearSignupForm = () => {
    setSignupData({
      user_name: "",
      user_email: "",
      user_phone_no: "",
      user_address: "",
      user_password: "",
    });
  };

  return (
    <div
      className="d-flex justify-content-center align-items-center"
      style={{ height: "100vh", width: "100vw" }}
    >
      <div className="card p-4 shadow" style={{ minWidth: "500px" }}>
        <h1 className="text-center mb-4">Login Page</h1>
        <form onSubmit={handleSubmit}>
          <div className="form-group mb-3">
            <input
              type="email"
              placeholder="Enter your email"
              className="form-control w-100 mx-auto"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group mt-3">
            <input
              type="password"
              placeholder="Enter your password"
              className="form-control w-100 mx-auto"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button className="btn btn-outline-success mt-4 w-100" type="submit">
            Login
          </button>
        </form>

        <button
          type="button"
          className="btn btn-outline-primary mt-3 w-100"
          data-bs-toggle="modal"
          data-bs-target="#signupModal"
        >
          Signup
        </button>
        <AlertMessage
          show={alert.show}
          type={alert.type}
          message={alert.message}
        />
      </div>

      <InputFormModal
        modalId="signupModal"
        title={"Sign up"}
        fields={[
          {
            name: "user_name",
            type: "text",
            placeholder: "User Name",
            required: true,
          },
          {
            name: "user_email",
            type: "email",
            placeholder: "Email",
            required: true,
          },
          {
            name: "user_phone_no",
            type: "text",
            placeholder: "Phone",
            pattern: "^\\+?[0-9]{10,13}$",
            required: true,
          },
          {
            name: "user_address",
            type: "text",
            placeholder: "Place",
            required: true,
          },
          {
            name: "user_password",
            type: "password",
            placeholder: "Password",
            required: true,
          },
        ]}
        formData={signupData}
        onChange={handleSignupChange}
        onSubmit={handleSignupSubmit}
        clearForm={clearSignupForm}
        alert={alert}
        showAlert={showAlert}
      />
    </div>
  );
}

export default Login;
