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
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '12px'
        }}>
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="url(#blue-pink-gradient)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <defs>
              <linearGradient id="blue-pink-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#6366f1" />
                <stop offset="50%" stopColor="#ec4899" />
                <stop offset="100%" stopColor="#f59e0b" />
              </linearGradient>
            </defs>
            <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"></path>
          </svg>
          <h1 style={{
            fontSize: '3.5rem',
            fontWeight: '800',
            background: 'linear-gradient(to right, #6366f1, #ec4899, #f59e0b)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            letterSpacing: '-2px',
            margin: 0
          }}>CloudAI Agent</h1>
        </div>
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
