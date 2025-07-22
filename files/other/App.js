/* global chrome */

import React, { useEffect, useState } from "react";
function App() {

  const [siteMinutes, setSiteMinutes] = useState({});
  const [goals, setGoals] = useState({});
  useEffect(() => {
    fetch("http://localhost:5000/api/analytics/today")
      .then(res => res.json())
      .then(data => {
        setSiteMinutes(data.site_minutes);
        setGoals(data.goals);
      });
  }, []);

  // Example: Send browsing data to Python API
  const uploadUsage = () => {
    chrome.storage.local.get({usage: []}, res => {
      fetch("http://localhost:5000/api/upload_usage", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(res.usage),
      });
      chrome.storage.local.set({usage: []});
    });
  };

  return (
    <div className="App">
       <h2>Today's Usage</h2>
      <ul>
        {Object.entries(siteMinutes).map(([site, mins]) => (
          <li key={site}>{site}: {mins.toFixed(1)} min</li>
        ))}
      </ul>
      <h3>Goals</h3>
      <ul>
        {Object.entries(goals).map(([goal, val]) => (
          <li key={goal}>{goal}: {val}</li>
        ))}
      </ul>
      <button onClick={uploadUsage}>Sync Usage</button>
      </div>
  );
}

export default App;
