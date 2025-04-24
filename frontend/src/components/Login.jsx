// src/Login.js
import { useState } from 'react';
import { apiRequest } from '../utils/Apirequest';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';


function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [signupData, setSignupData] = useState({
    user_name: '',
    user_email: '',
    user_phone_no: '',
    user_address: '',
    user_password: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const data = await apiRequest({
        url: 'http://localhost:8000/users/login',
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
      });

      console.log('Login successful:', data);
      alert("Login successful!");

    
      navigate('/dashboard');

    } catch (error) {
      console.error('Error during login:', error);
      alert(`Something went wrong: ${error.message}`);
    }
  };

  const handleSignupChange = (e) => {
    setSignupData({ ...signupData, [e.target.name]: e.target.value });
  };

  const handleSignupSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiRequest({
        url: 'http://localhost:8000/users/signup',
        method: 'POST',
        body: {
          user_name: signupData.user_name,
          user_email: signupData.user_email,
          user_phone_no: signupData.user_phone_no,
          user_address: signupData.user_address,
          user_password: signupData.user_password,
        },
      });

      alert("Signup successful!");

    } catch (error) {
      alert(`Signup failed: ${error.message}`);
    }
  };

  const clearSignupForm = () => {
    setSignupData({
      user_name: '',
      user_email: '',
      user_phone_no: '',
      user_address: '',
      user_password: ''
    });
  };
  

  return (
    <div className="d-flex justify-content-center align-items-center" style={{ height: '100vh', width: '100vw' }}>
      <div className="card p-4 shadow" style={{ minWidth: '500px' }}>
        <h1 className="text-center mb-4">Login Page</h1>
        <form onSubmit={handleSubmit}>
          <div className="form-group mb-3">
            <input
              type="email"
              placeholder="Enter your email"
              className="form-control w-100 mx-auto"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="form-group mt-3">
            <input
              type="password"
              placeholder="Enter your password"
              className="form-control w-100 mx-auto"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button className="btn btn-success mt-4 w-100" type="submit">
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
      </div>

      <div className="modal fade" id="signupModal" tabIndex="-1" aria-labelledby="signupModalLabel" aria-hidden="true">
        <div className="modal-dialog modal-dialog-centered">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id="signupModalLabel">Signup</h5>
             
            </div>
            <form onSubmit={handleSignupSubmit}>
              <div className="modal-body">
                <input
                  type="text"
                  name="user_name"
                  className="form-control mb-2"
                  placeholder="Username"
                  value={signupData.user_name}
                  onChange={handleSignupChange}
                />
                <input
                  type="email"
                  name="user_email"
                  className="form-control mb-2"
                  placeholder="Email"
                  value={signupData.user_email}
                  onChange={handleSignupChange}
                />
                <input
                  type="text"
                  name="user_phone_no"
                  className="form-control mb-2"
                  placeholder="Phone"
                  value={signupData.user_phone_no}
                  onChange={handleSignupChange}
                />
                <input
                  type="text"
                  name="user_address"
                  className="form-control mb-2"
                  placeholder="Place"
                  value={signupData.user_address}
                  onChange={handleSignupChange}
                />
                <input
                  type="password"
                  name="user_password"
                  className="form-control"
                  placeholder="Password"
                  value={signupData.user_password}
                  onChange={handleSignupChange}
                />
              </div>
              <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" data-bs-dismiss="modal" onClick={clearSignupForm }>
                    Close
                  </button>
                  <button type="submit" className="btn btn-primary">
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
