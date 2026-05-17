import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth.jsx';

const Header = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header style={{
      backgroundColor: '#f7931a',
      color: 'white',
      padding: '1rem',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}>
      <h1 style={{ margin: 0 }}>
        <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>
          Bitcoin Smart Contract Agent
        </Link>
      </h1>

      {user ? (
        <nav>
          <Link to="/chat" style={{ color: 'white', margin: '0 10px', textDecoration: 'none' }}>
            Chat
          </Link>
          <Link to="/scripts" style={{ color: 'white', margin: '0 10px', textDecoration: 'none' }}>
            Scripts
          </Link>
          <button
            onClick={handleLogout}
            style={{
              background: 'none',
              border: '1px solid white',
              color: 'white',
              padding: '5px 10px',
              cursor: 'pointer',
              marginLeft: '10px'
            }}
          >
            Logout
          </button>
        </nav>
      ) : (
        <nav>
          <Link to="/login" style={{ color: 'white', textDecoration: 'none' }}>
            Login
          </Link>
        </nav>
      )}
    </header>
  );
};

export default Header;