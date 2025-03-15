import { Link } from "react-router-dom";

const Landing = () => {
  return (
    <div className="landing-container">
      <h1>Welcome to Kennel Manager</h1>
      <p>Manage your kennel operations efficiently.</p>
      <Link to="/login">
        <button>Login</button>
      </Link>
      <Link to="/register">
        <button>Register</button>
      </Link>
    </div>
  );
};

export default Landing;
