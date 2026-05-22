import { useState, useEffect, createContext, useContext } from 'react';
import api from '../services/api.js';

const AuthContext = createContext();

const parseJwt = (token) => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => `%${`00${c.charCodeAt(0).toString(16)}`.slice(-2)}`)
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const payload = parseJwt(token);
      if (payload?.sub) {
        setUser({ username: payload.sub });
      } else {
        localStorage.removeItem('token');
      }
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    const trimmedUsername = username.trim();
    try {
      const response = await api.post('/api/auth/login', {
        username: trimmedUsername,
        password
      });

      const { access_token, user_id } = response.data;
      localStorage.setItem('token', access_token);
      setUser({ id: user_id, username: trimmedUsername });
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  };

  const register = async (username, email, password) => {
    const trimmedUsername = username.trim();
    const trimmedEmail = email.trim();
    try {
      const response = await api.post('/api/auth/register', {
        username: trimmedUsername,
        email: trimmedEmail,
        password
      });

      const { access_token, user_id } = response.data;
      localStorage.setItem('token', access_token);
      setUser({ id: user_id, username: trimmedUsername });
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Registration failed');
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};