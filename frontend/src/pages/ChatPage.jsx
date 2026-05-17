import { useState, useEffect } from 'react';
import ChatWindow from '../components/ChatWindow.jsx';
import MessageInput from '../components/MessageInput.jsx';
import api from '../services/api.js';

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    // Create a new session when component mounts
    createNewSession();
  }, []);

  const createNewSession = async () => {
    try {
      const response = await api.post('/api/sessions');
      setSessionId(response.data.id);
    } catch (error) {
      console.error('Error creating session:', error);
    }
  };

  const handleSendMessage = async (message) => {
    if (!sessionId) return;

    setLoading(true);
    try {
      const response = await api.post('/api/agent/chat', {
        session_id: sessionId,
        message
      });

      // Add user message and agent response to chat
      setMessages(prev => [
        ...prev,
        { role: 'user', content: message },
        { role: 'agent', content: response.data.response }
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [
        ...prev,
        { role: 'user', content: message },
        { role: 'agent', content: 'Sorry, I encountered an error. Please try again.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Chat with Bitcoin Agent</h2>
      <p>Ask me about Bitcoin scripts, validation, or generation!</p>

      <ChatWindow messages={messages} loading={loading} />
      <MessageInput onSendMessage={handleSendMessage} loading={loading} />
    </div>
  );
};

export default ChatPage;