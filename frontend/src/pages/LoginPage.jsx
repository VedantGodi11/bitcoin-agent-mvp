import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import LoginForm from '../components/LoginForm.jsx';
import { useAuth } from '../hooks/useAuth.jsx';

const LoginPage = () => {
  const [isRegister, setIsRegister] = useState(false);
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      navigate('/chat');
    }
  }, [user, navigate]);

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto' }}>
      <h1>Welcome to Bitcoin Smart Contract Agent</h1>
      <p>Chat with AI to generate, validate, and manage Bitcoin scripts.</p>

      <LoginForm isRegister={isRegister} />

      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <button
          onClick={() => setIsRegister(!isRegister)}
          style={{
            background: 'none',
            border: 'none',
            color: '#f7931a',
            cursor: 'pointer',
            textDecoration: 'underline'
          }}
        >
          {isRegister ? 'Already have an account? Login' : 'Need an account? Register'}
        </button>
      </div>
    </div>
  );
};

export default LoginPage;