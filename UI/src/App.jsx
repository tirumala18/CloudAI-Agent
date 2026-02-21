import React from 'react';
import ChatBox from './components/ChatBox';

function App() {
  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      padding: '2rem 4rem',
      margin: '0 auto',
      boxSizing: 'border-box'
    }}>
      <div style={{
        marginBottom: '1rem',
        textAlign: 'center'
      }}>
        <h1 style={{
          fontSize: '2.5rem',
          fontWeight: '700',
          background: 'linear-gradient(to right, #6366f1, #ec4899, #f59e0b)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          letterSpacing: '-1px'
        }}>CloudAI Agent</h1>
        <p style={{
          color: 'var(--text-secondary)',
          marginTop: '0.25rem',
          fontSize: '1rem',
          fontWeight: '500'
        }}>Your intelligent multi-cloud assistant</p>
      </div>

      <ChatBox />
    </div>
  );
}

export default App;
