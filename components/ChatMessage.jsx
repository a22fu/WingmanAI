// components/ChatMessage.js
import React from 'react';

const ChatMessage = ({ sender, text }) => {
  const className = sender === 'user' ? 'user-message' : 'bot-message';
  console.log(text)
  return <div className={className} style={{ whiteSpace: 'pre-wrap' }}>{text}</div>;
};

export default ChatMessage;
