// components/ChatWindow.js
import React, { useState } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

const ChatWindow = ({ messages, onSendMessage }) => {
  return (
    <div className="chat-window">
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <ChatMessage key={index} sender={msg.sender} text={msg.text} />
        ))}
      </div>
      <ChatInput onSendMessage={onSendMessage} />
    </div>
  );
};

export default ChatWindow;
