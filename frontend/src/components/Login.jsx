// src/Login.js
import { useState } from "react";
import { apiRequest } from "../utils/Apirequest";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";

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
  const [loginAlert, setLoginAlert] = useState({
    show: false,
    message: "",
    type: "success",
  });
  const [signupAlert, setSignupAlert] = useState({
    show: false,
    message: "",
    type: "success",
  });

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

      setLoginAlert({
        show: true,
        message: "Login Successful !!",
        type: "success",
      });

      navigate("/dashboard");
    } catch (error) {
      console.error("Error during login:", error);
      setLoginAlert({
        show: true,
        message:
          "Error occured while login. Please check user email and password",
        type: "danger",
      });
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

      setSignupAlert({
        show: true,
        message: "User Created Successfully!",
        type: "success",
      });
    } catch (error) {
      alert(`Signup failed: ${error.message}`);
      setSignupAlert({
        show: true,
        message: "User email already exist. Login instead!",
        type: "danger",
      });
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
        {loginAlert.show && (
          <div className={`alert alert-${loginAlert.type} mt-3`} role="alert">
            {loginAlert.message}
          </div>
        )}
      </div>

      <div
        className="modal fade"
        id="signupModal"
        tabIndex="-1"
        aria-labelledby="signupModalLabel"
        aria-hidden="true"
      >
        <div className="modal-dialog modal-dialog-centered">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id="signupModalLabel">
                Signup
              </h5>
            </div>
            <form onSubmit={handleSignupSubmit}>
              <div className="modal-body">
                {signupAlert.show && (
                  <div
                    className={`alert alert-${signupAlert.type}`}
                    role="alert"
                  >
                    {signupAlert.message}
                  </div>
                )}
                <input
                  type="text"
                  name="user_name"
                  className="form-control mb-2"
                  placeholder="Username"
                  value={signupData.user_name}
                  onChange={handleSignupChange}
                  required
                />
                <input
                  type="email"
                  name="user_email"
                  className="form-control mb-2"
                  placeholder="Email"
                  value={signupData.user_email}
                  onChange={handleSignupChange}
                  required
                />
                <input
                  type="text"
                  name="user_phone_no"
                  className="form-control mb-2"
                  placeholder="Phone"
                  value={signupData.user_phone_no}
                  onChange={handleSignupChange}
                  pattern="^\+?[0-9]*$"
                  required
                />
                <input
                  type="text"
                  name="user_address"
                  className="form-control mb-2"
                  placeholder="Place"
                  value={signupData.user_address}
                  onChange={handleSignupChange}
                  required
                />
                <input
                  type="password"
                  name="user_password"
                  className="form-control"
                  placeholder="Password"
                  value={signupData.user_password}
                  onChange={handleSignupChange}
                  required
                />
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-outline-dark"
                  data-bs-dismiss="modal"
                  onClick={clearSignupForm}
                >
                  Close
                </button>
                <button type="submit" className="btn btn-outline-primary">
                  Create Account
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
