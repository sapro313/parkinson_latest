import { useState } from "react";

export default function Login({ setAuth }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    const res = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    if (data.status === "success") setAuth(true);
    else alert("Invalid credentials");
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>🧠 Parkinson AI</h2>
        <p className="subtitle">Doctor Login</p>

        <div className="input-box">
          <label>Username</label>
          <input
            type="text"
            placeholder="Enter username"
            onChange={e => setUsername(e.target.value)}
          />
        </div>

        <div className="input-box">
          <label>Password</label>
          <input
            type="password"
            placeholder="Enter password"
            onChange={e => setPassword(e.target.value)}
          />
        </div>

        <button onClick={login}>Login</button>
      </div>
    </div>
  );
}