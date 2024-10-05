// components/ChatWindow.js
import React from 'react';
import ChatInput from './ChatInput';
import PlayerBox from './PlayerBox';
export default function SearchWindow({items, hiddenIds}) {
  const onSearch = async (search) => {
    console.log(search + "received");
    
  };

  return (
    <div className='search-window'> 
      <ChatInput
        onSendMessage={onSearch}
      >
      </ChatInput>
      <PlayerBox id="container6" items={items.container6} hiddenIds= {hiddenIds}></PlayerBox>
    </div>
  );
}