// App.js
import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);

  const handleSendMessage = (message) => {
    if (message.trim() !== '') {
      // Add user message to chat
      const newMessages = [...messages, { sender: 'user', text: message }];
      setMessages(newMessages);

      // Simulate AI response (you would replace this with an actual API call)
      getAIResponse(message, newMessages);
    }
  };

  const getAIResponse = (userMessage, currentMessages) => {
    setTimeout(() => {
      const aiResponse = 'AI Response: ' + userMessage;
      setMessages([...currentMessages, { sender: 'bot', text: aiResponse }]);
    }, 1000);
  };

  return (
    <div className="App">
      <ChatWindow messages={messages} onSendMessage={handleSendMessage} />
    </div>
  );
}

export default App;
