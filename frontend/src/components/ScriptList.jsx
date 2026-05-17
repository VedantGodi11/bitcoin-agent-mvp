import { useState } from 'react';

const ScriptList = ({ scripts, onDelete, loading }) => {
  const [validationResults, setValidationResults] = useState({});

  const validateScript = async (scriptId, content) => {
    try {
      const response = await fetch('/api/scripts/validate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ content })
      });
      const result = await response.json();
      setValidationResults(prev => ({
        ...prev,
        [scriptId]: result
      }));
    } catch (error) {
      console.error('Validation error:', error);
    }
  };

  return (
    <div className="card">
      <h3>Your Scripts</h3>
      {scripts.length === 0 ? (
        <p>No scripts yet. Create your first script above!</p>
      ) : (
        scripts.map(script => (
          <div key={script.id} style={{
            border: '1px solid #ddd',
            borderRadius: '5px',
            padding: '10px',
            marginBottom: '10px'
          }}>
            <pre style={{
              backgroundColor: '#f5f5f5',
              padding: '10px',
              borderRadius: '3px',
              fontFamily: 'monospace',
              whiteSpace: 'pre-wrap',
              wordWrap: 'break-word'
            }}>
              {script.content}
            </pre>
            <div style={{ marginTop: '10px', display: 'flex', gap: '10px', alignItems: 'center' }}>
              <button
                onClick={() => validateScript(script.id, script.content)}
                disabled={loading}
                style={{ backgroundColor: '#28a745' }}
              >
                Validate
              </button>
              <button
                onClick={() => onDelete(script.id)}
                disabled={loading}
                style={{ backgroundColor: '#dc3545' }}
              >
                Delete
              </button>
              <small style={{ color: '#666' }}>
                Created: {new Date(script.created_at).toLocaleDateString()}
              </small>
            </div>
            {validationResults[script.id] && (
              <div style={{ marginTop: '10px' }}>
                <strong>Validation Result:</strong>
                <div style={{
                  color: validationResults[script.id].is_valid ? '#28a745' : '#dc3545',
                  marginTop: '5px'
                }}>
                  {validationResults[script.id].is_valid ? '✓ Valid' : '✗ Invalid'}
                </div>
                {validationResults[script.id].errors.length > 0 && (
                  <div style={{ color: '#dc3545', marginTop: '5px' }}>
                    <strong>Errors:</strong>
                    <ul>
                      {validationResults[script.id].errors.map((error, idx) => (
                        <li key={idx}>{error}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {validationResults[script.id].warnings.length > 0 && (
                  <div style={{ color: '#ffc107', marginTop: '5px' }}>
                    <strong>Warnings:</strong>
                    <ul>
                      {validationResults[script.id].warnings.map((warning, idx) => (
                        <li key={idx}>{warning}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        ))
      )}
    </div>
  );
};

export default ScriptList;