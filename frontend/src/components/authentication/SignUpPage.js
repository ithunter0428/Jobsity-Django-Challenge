import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import axiosAPI from "../api/axiosApi";

const SignUpPage = () => {
  const history = useHistory();
  const [state, setState] = useState({
    username: "",
    email: "",
    password: "",
  });

  const handleChangeUsername = (e) => {
      setState({...state, username: e.target.value});
  }

  const handleChangeEmail = (e) => {
      setState({...state, email: e.target.value});
  }
    
  const handleChangePassword = (e) => {
    setState({...state, password: e.target.value});
  }

  const handleClick = async () => {
    const response = await axiosAPI.post("user/create/", {
      username: state.username,
      email: state.email,
      password: state.password,
    });
    if (response.status == 201) {
      alert("New User Created");
      history.push("/");
    } else {
      alert(response.statusText);
    }
  };

  return (
    <div>
      <h1>Sign Up page</h1>
      <p>
        username: <input type="text" value={state.username} onChange={handleChangeUsername} />
      </p>
      <p>
        email: <input type="email" value={state.email} onChange={handleChangeEmail} />
      </p>
      <p>
        password: <input type="text" value={state.password} onChange={handleChangePassword} />
      </p>
      <button onClick={handleClick}>sign up</button>
    </div>
  );
};

export default SignUpPage;
