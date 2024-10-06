// components/ChatWindow.js
import React, { useState } from "react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
// App.js
import PlayerBox from "./PlayerBox.jsx";
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


const teamContext = {
  flexDirection: "row",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  border: "1px solid black",

  background: "white",
};

const ChatWindow = ({ messages, onSendMessage, items, hiddenIds }) => { 
  
  const containerStyle = {
    width: "10vw",
    height: "10vw",
    background: "#dadada",

    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    border: "1px solid black",
  };

  return (
    <div className="chat-window">
      
        <div className="player-container">
          <PlayerBox containerStyle = {containerStyle} id="container1" items={items.container1} hiddenIds={hiddenIds} />
          <PlayerBox containerStyle = {containerStyle} id="container2" items={items.container2} hiddenIds={hiddenIds} />
          <PlayerBox containerStyle = {containerStyle} id="container3" items={items.container3} hiddenIds={hiddenIds} />
          <PlayerBox containerStyle = {containerStyle} id="container4" items={items.container4} hiddenIds={hiddenIds} />
          <PlayerBox containerStyle = {containerStyle} id="container5" items={items.container5} hiddenIds={hiddenIds} />
        </div>

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
