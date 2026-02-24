import React, { useState, useRef, useEffect } from 'react';
import { executeCommand } from '../services/api';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function ChatBox() {
  const [input, setInput] = useState('');

  // For local testing, we are just using the keys in docker-compose.yml
  const ACCOUNTS = [
    { id: 'default', name: 'Local Test Account (Access Keys)' }
  ];

  const [selectedAccount, setSelectedAccount] = useState('default');
  const [messages, setMessages] = useState(() => {
    // Try to retrieve existing messages from localStorage
    const saved = localStorage.getItem('cloud_agent_messages');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        return [];
      }
    }
    return [
      { sender: 'bot', text: 'Hello! I am your AI Cloud Operations Agent. How can I help you manage your AWS resources today?' }
    ];
  });
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Scroll to bottom when new message added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Save messages to local storage whenever they change
  useEffect(() => {
    localStorage.setItem('cloud_agent_messages', JSON.stringify(messages));
  }, [messages]);

  const sendCommand = async () => {
    if (!input.trim() || isLoading) return;

    const query = input.trim();
    const userMsg = { sender: 'user', text: query };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const result = await executeCommand(query, selectedAccount);

      // Attempt to prettify JSON responses
      let displayResult = result;
      if (result && typeof result.response === 'string') {
        displayResult = result.response;
      } else if (typeof result === 'object' && result !== null) {
        displayResult = JSON.stringify(result, null, 2);
      }

      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: displayResult }
      ]);
    } catch (err) {
      toast.error('Error executing command or unable to reach backend.');
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: '❌ An error occurred while communicating with the cloud agent backend. Please check the logs.' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearHistory = () => {
    if (window.confirm('Are you sure you want to clear your chat history?')) {
      const initial = [{ sender: 'bot', text: 'Chat history cleared. How can I help you?' }];
      setMessages(initial);
      localStorage.setItem('cloud_agent_messages', JSON.stringify(initial));
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      width: '100%',
      flex: 1,
      background: 'var(--glass-bg)',
      backdropFilter: 'blur(20px)',
      WebkitBackdropFilter: 'blur(20px)',
      border: '1px solid var(--glass-border)',
      borderRadius: '24px',
      overflow: 'hidden',
      boxShadow: '0 10px 40px rgba(0, 0, 0, 0.08)'
    }}>
      {/* Header Controls */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '16px 24px 0 24px',
      }}>
        {/* Account Selector */}
        <select
          value={selectedAccount}
          onChange={(e) => setSelectedAccount(e.target.value)}
          style={{
            padding: '6px 12px',
            borderRadius: '16px',
            background: 'rgba(255,255,255,0.5)',
            border: '1px solid rgba(0,0,0,0.1)',
            color: 'var(--text-primary)',
            fontSize: '0.85rem',
            outline: 'none',
            cursor: 'pointer',
            boxShadow: '0 2px 4px rgba(0,0,0,0.02)'
          }}
        >
          {ACCOUNTS.map(acc => (
            <option key={acc.id} value={acc.id}>{acc.name}</option>
          ))}
        </select>
        <button
          onClick={clearHistory}
          style={{
            background: 'transparent',
            border: 'none',
            color: 'var(--text-secondary)',
            fontSize: '0.8rem',
            cursor: 'pointer',
          }}
          onMouseOver={(e) => {
            e.target.style.color = '#ef4444';
          }}
          onMouseOut={(e) => {
            e.target.style.color = 'var(--text-secondary)';
          }}
        >
          Clear Chat
        </button>
      </div>

      {/* Chat messages */}
      <div style={{
        flex: 1,
        padding: '24px',
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
      }}>
        {messages.map((msg, i) => (
          <div key={i} className="animate-msg" style={{
            alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
            maxWidth: '80%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: msg.sender === 'user' ? 'flex-end' : 'flex-start'
          }}>
            <span style={{
              fontSize: '0.75rem',
              color: 'var(--text-secondary)',
              marginBottom: '6px',
              marginLeft: '4px',
              fontWeight: '500'
            }}>
              {msg.sender === 'user' ? 'You' : 'Agent'}
            </span>
            <div style={{
              background: msg.sender === 'user' ? 'linear-gradient(135deg, #a78bfa 0%, #f472b6 100%)' : 'var(--bot-msg-bg)',
              color: msg.sender === 'user' ? '#ffffff' : 'var(--text-primary)',
              padding: '16px 20px',
              borderRadius: msg.sender === 'user' ? '20px 20px 4px 20px' : '20px 20px 20px 4px',
              border: 'none',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word',
              fontSize: '1rem',
              lineHeight: '1.6',
              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.02)'
            }}>
              {msg.text}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="animate-msg" style={{
            alignSelf: 'flex-start',
            maxWidth: '80%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-start'
          }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: '6px', marginLeft: '4px', fontWeight: '500' }}>Agent</span>
            <div style={{
              backgroundColor: 'var(--bot-msg-bg)',
              color: 'var(--text-secondary)',
              padding: '14px 20px',
              borderRadius: '20px 20px 20px 4px',
              border: '1px solid var(--glass-border)',
              display: 'flex',
              gap: '6px',
              alignItems: 'center'
            }}>
              <span className="dot-pulse">Processing...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div style={{
        padding: '24px',
      }}>
        <div style={{
          display: 'flex',
          background: 'rgba(255,255,255,0.7)',
          borderRadius: '24px',
          padding: '8px 8px 8px 16px',
          border: '1px solid rgba(0,0,0,0.05)',
          alignItems: 'center',
          boxShadow: '0 2px 10px rgba(0,0,0,0.02)'
        }}
          onFocus={(e) => { e.currentTarget.style.borderColor = 'rgba(99, 102, 241, 0.3)'; e.currentTarget.style.boxShadow = '0 0 0 4px rgba(99,102,241,0.1)'; }}
          onBlur={(e) => { e.currentTarget.style.borderColor = 'rgba(0,0,0,0.05)'; e.currentTarget.style.boxShadow = 'inset 0 2px 4px rgba(0,0,0,0.02)'; }}
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendCommand()}
            placeholder="Type a command or describe what to do..."
            style={{
              flex: 1,
              background: 'transparent',
              border: 'none',
              color: 'var(--text-primary)',
              fontSize: '1rem',
              outline: 'none',
              fontFamily: 'inherit'
            }}
            disabled={isLoading}
          />
          <button
            onClick={sendCommand}
            disabled={isLoading || !input.trim()}
            style={{
              marginLeft: '12px',
              padding: '8px 16px',
              borderRadius: '20px',
              background: 'rgba(0,0,0,0.05)',
              color: 'var(--text-secondary)',
              border: 'none',
              cursor: input.trim() && !isLoading ? 'pointer' : 'not-allowed',
              fontWeight: '500',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            {isLoading ? 'Wait...' : 'Send'}
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
      </div>

      <ToastContainer position="bottom-right" theme="dark" />
    </div>
  );
}

export default ChatBox;
