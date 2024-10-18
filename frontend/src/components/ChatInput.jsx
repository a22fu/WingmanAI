// components/ChatInput.js
import React, { useState } from 'react';
import vallogo from "../resources/vallogo.png" 
import sendimg from "../resources/send-svgrepo-com.svg"
const ChatInput = ({ onSendMessage }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    onSendMessage(inputValue);
    setInputValue(''); // Clear the input field after sending
  };
  
  const handleEnter = (e) => {
    if(e.key === 'Enter'){
      handleSend()
    }
  };

  return (
    <div className="chat-input">
      <div className="input-container">
        <div className="valorant-icon">
          <img src= {vallogo}alt="val-logo" ></img>
        </div>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={(e) => handleEnter(e)}
          placeholder="Ask a VCT question..."
          className="message-input"
        />
        <button onClick={handleSend} className="send-button">
          <img width="37px" height="37px" src={sendimg} alt="Enter"/>
        </button>
        </div>

    </div>
  );
};

export default ChatInput;
