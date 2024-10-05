// components/ChatWindow.js
import React, { useState } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
// App.js
import PlayerBox from './PlayerBox.jsx';
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

export default function SearchWindow() {
  const onSearch = async (search) => {
    console.log(search + "received");
    
  };

  return (
    <div className='search-window'> 
      <ChatInput
        onSendMessage={onSearch}
      >

      </ChatInput>
    </div>
  );
}