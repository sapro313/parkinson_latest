import { useEffect, useState } from "react";
import { Bar, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  LineElement,
  PointElement
} from "chart.js";

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  LineElement,
  PointElement
);

export default function Dashboard() {
  const [features, setFeatures] = useState([]);
  const [inputs, setInputs] = useState({});
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [page, setPage] = useState("dashboard");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/features")
      .then(res => res.json())
      .then(setFeatures);

    fetch("http://127.0.0.1:8000/history")
      .then(res => res.json())
      .then(setHistory);
  }, []);

  const handleChange = (key, value) => {
    const num = value === "" ? "" : Number(value);
    setInputs(prev => ({ ...prev, [key]: num }));
  };

  const predict = async () => {
    const res = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ inputs })
    });

    const data = await res.json();
    setResult(data);

    fetch("http://127.0.0.1:8000/history")
      .then(res => res.json())
      .then(setHistory);
  };

  // Theme colors from CSS variables
  const primary = getComputedStyle(document.documentElement).getPropertyValue('--primary').trim();
  const secondary = getComputedStyle(document.documentElement).getPropertyValue('--secondary').trim();
  const accent = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();

  // Bar Chart data
  const barData = {
    labels: ["Healthy", "Parkinson"],
    datasets: [
      {
        label: "Confidence",
        data: result ? [1 - result.confidence, result.confidence] : [0, 0],
        backgroundColor: [primary, accent],
        borderRadius: 6
      }
    ]
  };

  // Line Chart data
  const lineData = {
    labels: history.map(h => h.timestamp),
    datasets: [
      {
        label: "Confidence Trend",
        data: history.map(h => h.confidence),
        borderColor: secondary,
        backgroundColor: "rgba(59, 130, 246, 0.2)",
        tension: 0.3,
        fill: true,
        pointBackgroundColor: accent
      }
    ]
  };

  return (
    <div className="dashboard">

      <div className="sidebar">
        <h2>🧠 AI Panel</h2>

        <p
          onClick={() => setPage("dashboard")}
          style={{ color: page === "dashboard" ? accent : "white" }}
        >
          Dashboard
        </p>

        <p
          onClick={() => setPage("analytics")}
          style={{ color: page === "analytics" ? accent : "white" }}
        >
          Analytics
        </p>
      </div>

      <div className="main">

        {page === "dashboard" && (
          <>
            <h1>Parkinson AI Diagnostic</h1>

            <div className="card">
              <h3>Patient Inputs</h3>

              <div className="grid">
                {features.map(f => (
                  <div key={f} className="input-group">
                    <label>{f}</label>

                    <input
                      type="range"
                      min="0"
                      max="500"
                      step="0.1"
                      value={inputs[f] ?? 0}
                      onChange={e => handleChange(f, e.target.value)}
                    />

                    <input
                      type="number"
                      value={inputs[f] ?? ""}
                      onChange={e => handleChange(f, e.target.value)}
                    />

                    <span className="range-value">
                      Value: {inputs[f] ?? 0}
                    </span>
                  </div>
                ))}
              </div>

              <button onClick={predict}>Analyze</button>
            </div>

            {result && (
              <div className="card">
                <h3>Prediction</h3>
                <p>{result.result}</p>
                <p>{(result.confidence * 100).toFixed(2)}%</p>
              </div>
            )}

            {result && (
              <div className="card">
                <h3>Confidence Chart</h3>
                <Bar data={barData} />
              </div>
            )}
          </>
        )}

        {page === "analytics" && (
          <>
            <h1>Analytics Dashboard</h1>

            {history.length > 0 && (
              <div className="card">
                <h3>Prediction Trend</h3>
                <Line data={lineData} />
              </div>
            )}

            <div className="card">
              <h3>History</h3>
              <table style={{ width: "100%", marginTop: "10px" }}>
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>Result</th>
                    <th>Confidence</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((h, i) => (
                    <tr key={i}>
                      <td>{h.timestamp}</td>
                      <td>{h.result}</td>
                      <td>{(h.confidence * 100).toFixed(2)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}

      </div>
    </div>
  );
}