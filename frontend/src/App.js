import { useState } from "react";
import Login from "./Login";
import Dashboard from "./Dashboard";

function App() {
  const [auth, setAuth] = useState(false);

  return auth ? <Dashboard /> : <Login setAuth={setAuth} />;
}

export default App;