import React, { useState, useRef, useEffect } from 'react';
import { executeCommand } from '../services/api';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function ChatBox() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  // Scroll to bottom when new message added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendCommand = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMsg]);

    try {
      const result = await executeCommand(input);
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: JSON.stringify(result, null, 2) }
      ]);
    } catch (err) {
      toast.error('Error executing command');
    }

    setInput('');
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '90vh',
      maxWidth: '3700px',
      margin: '0 auto',
      border: '1px solid #ddd',
      borderRadius: '10px',
      overflow: 'hidden',
      backgroundColor: '#f7f7f8',
      boxShadow: '0 0 10px rgba(0,0,0,0.1)'
    }}>
      {/* Chat messages */}
      <div style={{
        flex: 1,
        padding: '20px',
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column'
      }}>
        {messages.map((msg, i) => (
          <div key={i} style={{
            alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
            margin: '5px 0',
            maxWidth: '75%'
          }}>
            <div style={{
              backgroundColor: msg.sender === 'user' ? '#3b82f6' : '#e5e7eb',
              color: msg.sender === 'user' ? '#fff' : '#000',
              padding: '12px 18px',
              borderRadius: '20px',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word',
              fontSize: '14px',
              lineHeight: '1.5'
            }}>
              {msg.text}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div style={{
        display: 'flex',
        padding: '15px',
        borderTop: '1px solid #ddd',
        backgroundColor: '#fff'
      }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendCommand()}
          placeholder="Type a command or message..."
          style={{
            flex: 1,
            padding: '20px 15px',
            borderRadius: '20px',
            border: '1px solid #ccc',
            fontSize: '14px',
            outline: 'none'
          }}
        />
        <button
          onClick={sendCommand}
          style={{
            marginLeft: '10px',
            padding: '20px 30px',
            borderRadius: '20px',
            backgroundColor: '#3b82f6',
            color: '#fff',
            border: 'none',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          Send
        </button>
      </div>

      <ToastContainer position="bottom-right" />
    </div>
  );
}

export default ChatBox;
