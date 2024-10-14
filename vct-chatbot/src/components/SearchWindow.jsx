// components/ChatWindow.js
import {useState} from 'react';
import PlayerBox from './PlayerBox';
export default function SearchWindow({items, hiddenIds}) {
  const [search, setSearch] = useState('');
  const containerStyle = {
    width: "20vw",
  
    display: 'grid',
    gridTemplateColumns: `repeat(${4}, 1fr)`,  // 5 columns
    gridGap: '10px',                          // Spacing between grid items
    padding: '10px',

    gridAutoRows: 'auto',                     // Ensures rows take only as much height as needed
    alignItems: 'start',                      // Align items at the start of each row
  };
  
  return (
    <div className='search-window'> 
      <div className="chat-input player-search">
      <input
        style={{marginTop:"20px"}}
        type="text"
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search for player..."
      />
        </div>
        <div className='grid-wrap'>
          <PlayerBox containerStyle = {containerStyle} 
          id="container6" 
          items={items.container6} 
          hiddenIds= {hiddenIds}
          search = {search}>
          </PlayerBox>
          </div>
    </div>
  );
}



