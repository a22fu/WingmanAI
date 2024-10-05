// App.js
import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow.jsx';
import buildTeam from './API/buildAPI.js';
import PlayerBox from './components/PlayerBox.jsx';
import PlayerCard from './components/PlayerCard.jsx';
import {
  DndContext,
  KeyboardSensor,
  PointerSensor,
  DragOverlay,

  useSensor,
  useSensors,
  closestCorners,
} from "@dnd-kit/core";
import { arrayMove, sortableKeyboardCoordinates } from "@dnd-kit/sortable";

import './App.css';



function App() {
  const [messages, setMessages] = useState([]);

  const handleSendMessage = async (message) => {
    console.log(message + "received")
    if (message.trim() !== '') {
      // Add user message to chat
      const newMessages = [...messages, { sender: 'user', text: message }];
      setMessages(newMessages);

      // Simulate AI response (you would replace this with an actual API call)
      const aiResponse = await buildTeam(message);
      setMessages([...newMessages, { sender: 'bot', text: aiResponse }]);

    }
  };



  return (
    <div className="App">
      <ChatWindow className= {chat-container} messages={messages} onSendMessage={handleSendMessage} />
    </div>
  );  
  }

export default App;

  
