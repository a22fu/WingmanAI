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
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={(e) => handleEnter(e)}
        placeholder="Type your message..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
};

export default ChatInput;
