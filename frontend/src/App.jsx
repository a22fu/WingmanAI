import React, { useState } from "react";
import ChatWindow from "./components/ChatWindow.jsx";
import {buildTeam }from "./API/buildAPI.js";
import { changeTeam } from "./API/buildAPI.js";
import PlayerCard from "./components/PlayerCard.jsx";
import vctlogo from "./resources/vct_logo.png"
import wingman from "./resources/Wingman.png"
import { alpha, styled } from '@mui/material/styles';
import { red } from '@mui/material/colors';
import Switch from '@mui/material/Switch';
import FormControlLabel from '@mui/material/FormControlLabel';
import {
  DragOverlay,
  DndContext,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  closestCorners,
} from "@dnd-kit/core";

import "./App.css";
import SearchWindow from "./components/SearchWindow.jsx";
import playerdata from "./players/playerdata.jsx";


const RedSwitch = styled(Switch)(({ theme }) => ({
  '& .MuiSwitch-switchBase.Mui-checked': {
    color: red[600],
    '&:hover': {
      backgroundColor: alpha(red[600], theme.palette.action.hoverOpacity),
    },
  },
  '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
    backgroundColor: red[600],
  },
}));

function App() {
  const [items, setItems] = useState({
    container1: [],
    container2: [],
    container3: [],
    container4: [],
    container5: [],
    container6: playerdata,
  });
  const [messages, setMessages] = useState([]);
  const [activeId, setActiveId] = useState();
  const [isAnalysisMode, setIsAnalysisMode] = useState(false);

  // Handle switch change
  const handleSwitchChange = (event) => {
    setIsAnalysisMode(event.target.checked);
    console.log('Switch Value:', event.target.checked); // Log the value
  };

  const handleSendMessage = async (message) => {
    console.log(message + " received");
    if (message.trim() !== "") {
      const newMessages = [...messages, { sender: "user", text: message }];
      setMessages(newMessages);
      const loadingResponse = [...newMessages, {sender: "bot", text: "..."}];
      setMessages(loadingResponse)

      try{
        const aiResponse = await buildTeam(message, items, setItems);
        setMessages([...newMessages, { sender: "bot", text: aiResponse }]);
      }

      catch(error){
        console.warn(error)
        setMessages([...newMessages, { sender: "bot", text: "There was an error with your last prompt. Please try again." }]);

      }

    }
  };

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor)
  );

  return (
    <div className="App">
      <div className="top">
        <div className="left">
        <img src= {wingman} alt="val-logo" ></img>
          <h>Wingman</h>
        </div>
      <div className="right">
        <h>Analysis Mode</h>
            <FormControlLabel
            value="end"
            control={<RedSwitch/>}
            labelPlacement="start"
            className="switch"
            onChange={handleSwitchChange} 
          />
        </div>
      </div>
      <div className="main">
        <DndContext
          sensors={sensors}
          collisionDetection={closestCorners}
          onDragStart={handleDragStart}
          onDragEnd={handleDragEnd}
        >
          <SearchWindow items = {items} hiddenIds={[]}/>
          <ChatWindow messages={messages} onSendMessage={handleSendMessage} items={items} hiddenIds={[activeId]} // Pass activeId here
          />
          <DragOverlay>
            {(activeId) ? <PlayerCard id={activeId} playerId={activeId} /> : null}
          </DragOverlay>
        </DndContext>
      </div>
    </div>
  );

  function findContainer(id) {
    if (id in items) {
      return id;
    }

    return Object.keys(items).find((key) => items[key].includes(id));
  }

  function handleDragStart(event) {
    const { active } = event;
    const { id } = active;
    setActiveId(id);
  }

  function handleDragEnd(event) {
    const { active, over } = event;
    if (!over) return;

    const { id: activeId } = active;
    const { id: overId } = over;
    const activeContainer = findContainer(activeId);
    const overContainer = findContainer(overId);
    
    if (!activeContainer || !overContainer) {
      return;
    }

    // Swap positions in the containers
    if (activeContainer !== overContainer) {
      setItems((prevItems) => {
        var activeItem = activeId;
        var overItem = overId;
        if(activeId.includes("container")){
          activeItem = prevItems[activeContainer][0];
        }
        if(overId.includes("container")){
          overItem = prevItems[overContainer][0];
        }

        if(overItem){ // swap if exists or place if doesnt exist

          if(overContainer === "container6"){ // remove a player
            console.log(prevItems)
            if(isAnalysisMode){
              var old_team = prevItems.container1.concat(prevItems.container2).concat(prevItems.container3).concat(prevItems.container4).concat(prevItems.container5)

              const newMessages = [...messages];
              changeTeam(old_team, activeItem, "", setMessages, newMessages);
            }

            return {
              ...prevItems,
              [activeContainer]: [], // Place the overItem in the active container
              [overContainer]: [...prevItems[overContainer], activeItem], // Place the activeItem in the over container
            };
          }else if(activeContainer === "container6"){ // Swap from search.
            console.log(activeItem)
            console.log(overItem)
            console.log(prevItems)
            if(isAnalysisMode){
              var old_team = prevItems.container1.concat(prevItems.container2).concat(prevItems.container3).concat(prevItems.container4).concat(prevItems.container5)


              const newMessages = [...messages];
              changeTeam(old_team, activeItem, overItem, setMessages, newMessages);
            }
            return {
              ...prevItems,
              [activeContainer]: prevItems[activeContainer].map(item =>
                item === activeItem ? overItem : item 
              ),
              [overContainer]: [activeItem], 
            };
          }else{
            
        return {
          ...prevItems,
          [activeContainer]: [overItem], // Place the overItem in the active container
          [overContainer]: [activeItem], // Place the activeItem in the over container
        };
      
    }
      }else{
        if(activeContainer === "container6"){
          if(isAnalysisMode){
            var old_team = prevItems.container1.concat(prevItems.container2).concat(prevItems.container3).concat(prevItems.container4).concat(prevItems.container5)


            const newMessages = [...messages];
            changeTeam(old_team, "", activeItem, setMessages, newMessages);
          }
          return {
            ...prevItems,
            [activeContainer]: prevItems[activeContainer].filter(item =>
              item !== activeItem  // Replace activeItem with overItem
            ),
            [overContainer]: [activeItem], // Append activeItem to overContainer
          };
        }else{
        return {
          ...prevItems,
          [activeContainer]: [], // Place the overItem in the active container
          [overContainer]: [activeItem], // Place the activeItem in the over container
        };
      }
    }    
  }
    );
    }

    setActiveId(null); // Reset active item
  }
}

export default App;
