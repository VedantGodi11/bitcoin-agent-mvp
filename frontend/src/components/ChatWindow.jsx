import { useEffect, useRef } from 'react';

const ChatWindow = ({ messages, loading }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div style={{
      height: '400px',
      border: '1px solid #ddd',
      borderRadius: '5px',
      padding: '10px',
      marginBottom: '20px',
      overflowY: 'auto',
      backgroundColor: '#f9f9f9'
    }}>
      {messages.length === 0 ? (
        <div style={{ textAlign: 'center', color: '#666', padding: '20px' }}>
          Start a conversation with the Bitcoin Smart Contract Agent!
        </div>
      ) : (
        messages.map((message, index) => (
          <div
            key={index}
            style={{
              marginBottom: '15px',
              textAlign: message.role === 'user' ? 'right' : 'left'
            }}
          >
            <div
              style={{
                display: 'inline-block',
                maxWidth: '70%',
                padding: '10px',
                borderRadius: '10px',
                backgroundColor: message.role === 'user' ? '#f7931a' : '#e9ecef',
                color: message.role === 'user' ? 'white' : 'black'
              }}
            >
              <strong>{message.role === 'user' ? 'You' : 'Agent'}:</strong> {message.content}
            </div>
          </div>
        ))
      )}

      {loading && (
        <div style={{ textAlign: 'left', marginBottom: '15px' }}>
          <div style={{
            display: 'inline-block',
            padding: '10px',
            borderRadius: '10px',
            backgroundColor: '#e9ecef',
            color: '#666'
          }}>
            <strong>Agent:</strong> Thinking...
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatWindow;