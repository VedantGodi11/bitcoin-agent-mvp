import { useState } from 'react';

const MessageInput = ({ onSendMessage, loading }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !loading) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px' }}>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message to the Bitcoin agent..."
        style={{ flex: 1 }}
        disabled={loading}
      />
      <button type="submit" disabled={loading || !message.trim()}>
        Send
      </button>
    </form>
  );
};

export default MessageInput;