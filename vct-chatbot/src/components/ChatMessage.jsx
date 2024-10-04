// components/ChatMessage.js
import React from 'react';

const ChatMessage = ({ sender, text }) => {
  const className = sender === 'user' ? 'user-message' : 'bot-message';
  return <div className={className}>{text}</div>;
};

export default ChatMessage;
