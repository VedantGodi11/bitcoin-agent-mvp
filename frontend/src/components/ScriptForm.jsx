import { useState } from 'react';

const ScriptForm = ({ onSubmit, loading }) => {
  const [content, setContent] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (content.trim() && !loading) {
      onSubmit(content.trim());
      setContent('');
    }
  };

  return (
    <div className="card">
      <h3>Create New Script</h3>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Enter your Bitcoin script here..."
            rows={4}
            required
            disabled={loading}
          />
        </div>
        <button type="submit" disabled={loading || !content.trim()}>
          {loading ? 'Creating...' : 'Create Script'}
        </button>
      </form>
    </div>
  );
};

export default ScriptForm;