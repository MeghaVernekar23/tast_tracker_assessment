// src/Login.js
import { useState } from 'react';


function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {

            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);
            const url = "http://localhost:8000/users/login";
            const response = await fetch(url, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
              },
              body: formData.toString(),
            });

            console.log("*****",response.status)
        
            if (!response.ok) {
              throw new Error(`Server responded with status ${response.status}`);
            }
        
            const data = await response.json();
            console.log('Login successful:', data);
            
          } catch (error) {
            console.error('Error during login:', error);
            alert(`Something went wrong: ${error.message}`);
          }


    };

    return (
        <div className="container mt-5 text-center">
            <h1 className="mb-4">Login Page</h1>
            <form  onSubmit={handleSubmit}>
                <div className="form-group">
                    <input
                        type="email"
                        placeholder="Enter your email"
                        className="form-control w-1000 mx-auto"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <input
                        type="password"
                        placeholder="Enter your password"
                        className="form-control w-1000 mx-auto"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>

                <button className="btn btn-success mt-3" type="submit">
                Submit
                </button>
            </form>
            <span id='successlogin'>

            </span>
    </div>
        
    );
}

export default Login;
