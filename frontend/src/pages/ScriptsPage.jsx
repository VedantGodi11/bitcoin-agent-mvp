import { useState, useEffect } from 'react';
import ScriptForm from '../components/ScriptForm.jsx';
import ScriptList from '../components/ScriptList.jsx';
import api from '../services/api.js';

const ScriptsPage = () => {
  const [scripts, setScripts] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadScripts();
  }, []);

  const loadScripts = async () => {
    try {
      const response = await api.get('/api/scripts');
      setScripts(response.data);
    } catch (error) {
      console.error('Error loading scripts:', error);
    }
  };

  const handleCreateScript = async (content) => {
    setLoading(true);
    try {
      await api.post('/api/scripts', { content });
      await loadScripts(); // Reload scripts
    } catch (error) {
      console.error('Error creating script:', error);
      alert('Error creating script. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteScript = async (scriptId) => {
    if (!confirm('Are you sure you want to delete this script?')) return;

    setLoading(true);
    try {
      await api.delete(`/api/scripts/${scriptId}`);
      await loadScripts(); // Reload scripts
    } catch (error) {
      console.error('Error deleting script:', error);
      alert('Error deleting script. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Bitcoin Scripts</h2>
      <p>Manage your Bitcoin smart contract scripts.</p>

      <ScriptForm onSubmit={handleCreateScript} loading={loading} />
      <ScriptList
        scripts={scripts}
        onDelete={handleDeleteScript}
        loading={loading}
      />
    </div>
  );
};

export default ScriptsPage;