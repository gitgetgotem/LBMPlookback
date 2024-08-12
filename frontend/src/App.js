import React, { useState } from 'react';
import Dropdowns from './components/Dropdowns';
import './App.css';

const App = () => {
  const [result, setResult] = useState(null);

  const handleUpdate = async (zone, curve, utility) => {
    const response = await fetch('http://127.0.0.1:5000/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ zone, curve, utility }),
    });

    if (!response.ok) {
        console.error("Error:", response.statusText);
        return;
    }

    const data = await response.json();
    setResult(data);
  };

  const getOrderedKeys = (data) => {
    const keys = Object.keys(data[0]);
    const orderedKeys = ['Time_Stamp', ...keys.filter(key => key !== 'Time_Stamp')];
    return orderedKeys;
  };

  return (
    <div className="container">
      <div className="dropdown-container">
        <h1>LBMP Lookback</h1>
        <Dropdowns onUpdate={handleUpdate} />
      </div>
      {result && (
        <div className="table-container">
          <h3>Result:</h3>
          <table>
            <thead>
              <tr>
                {getOrderedKeys(result).map((key) => (
                  <th key={key}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {result.map((row, index) => (
                <tr key={index}>
                  {getOrderedKeys(result).map((key) => (
                    <td key={key}>{row[key]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default App;
