import React, { useState } from "react";
import axiosAPI from "../api/axiosApi";

const ProfilePage = () => {
  const [state, setState] = useState({
    stock_resp: "",
    history_resp: "",
    stats_resp: "",
  });

  const handleStock = async () => {
    setState({...state, stock_resp: ""});
    const response = await axiosAPI.get("stock", {
      params: {
        q: document.getElementById('input-stock').value,
      }
    });
    setState({...state, stock_resp: JSON.stringify(response.data)});
  };

  const handleHistory = async () => {
    setState({...state, history_resp: ""});
    const response = await axiosAPI.get("history", {
      params: {
      }
    });
    setState({...state, history_resp: JSON.stringify(response.data)});
  };

  const handleStats = async () => {
    setState({...state, stats_resp: ""});
    const response = await axiosAPI.get("stats", {
      params: {
      }
    });
    setState({...state, stats_resp: JSON.stringify(response.data)});
  };

  return (
    <div>
      <h1>Profile page</h1>
      <p>Only logged in users should see this</p>
      <p>
        <button onClick={handleStock}> Get Stock </button>
        <input id="input-stock" type="text" size="10" />
        <br />
        <textarea rows="2" cols="180" value={state.stock_resp} readOnly />
      </p>
      <p>
        <button onClick={handleHistory}>Get History</button>
        <br />
        <textarea rows="10" cols="140" value={state.history_resp} readOnly />
      </p>
      <p>
        <button onClick={handleStats}>Get Stats</button>
        <br />
        <textarea rows="5" cols="100" value={state.stats_resp} readOnly />
      </p>
    </div>
  );
};

export default ProfilePage;
