// components/ChatInput.js
import React, { useState } from 'react';

const ChatInput = ({ onSendMessage }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    onSendMessage(inputValue);
    setInputValue(''); // Clear the input field after sending
  };
  
  const handleEnter = (e) => {
    if(e.key == 'Enter'){
      handleSend()
    }
  };

  return (
    <div className="chat-input">
      <div className="input-container">
  <input
    type="text"
    value={inputValue}
    onChange={(e) => setInputValue(e.target.value)}
    onKeyDown={(e) => handleEnter(e)}
    placeholder="Ask a VCT question..."
    className="message-input"
  />
  <button onClick={handleSend} className="send-button">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="feather feather-upload"
    >
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
      <polyline points="17 8 12 3 7 8"></polyline>
      <line x1="12" y1="3" x2="12" y2="15"></line>
    </svg>
  </button>
</div>

    </div>
  );
};

export default ChatInput;
