import React, { useState } from "react";
import ChatWindow from "./components/ChatWindow.jsx";
import buildTeam from "./API/buildAPI.js";
import PlayerCard from "./components/PlayerCard.jsx";
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
function App() {
  const [items, setItems] = useState({
    container1: ["1"],
    container2: ["2"],
    container3: ["3"],
    container4: ["4"],
    container5: ["5"],
    container6: playerdata,
  });

  const [activeId, setActiveId] = useState();
  const defaultAnnouncements = {
    onDragStart(id) {
      console.log(`Picked up draggable item ${id}.`);
    },
    onDragOver(id, overId) {
      if (overId) {
        console.log(`Draggable item ${id} was moved over droppable area ${overId}.`);
        return;
      }
      console.log(`Draggable item ${id} is no longer over a droppable area.`);
    },
    onDragEnd(id, overId) {
      if (overId) {
        console.log(`Draggable item ${id} was dropped over droppable area ${overId}`);
        return;
      }
      console.log(`Draggable item ${id} was dropped.`);
    },
    onDragCancel(id) {
      console.log(`Dragging was cancelled. Draggable item ${id} was dropped.`);
    },
  };
  
  const [messages, setMessages] = useState([]);

  const handleSendMessage = async (message) => {
    console.log(message + " received");
    if (message.trim() !== "") {
      const newMessages = [...messages, { sender: "user", text: message }];
      setMessages(newMessages);

      const aiResponse = await buildTeam(message);
      setMessages([...newMessages, { sender: "bot", text: aiResponse }]);
    }
  };

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor)
  );

  return (
    <div className="App">
      <DndContext
        announcements={defaultAnnouncements}
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
    console.log(event);
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

        if(overItem){ // swap or place if doesnt exist

          if(overContainer === "container6"){
            return {
              ...prevItems,
              [activeContainer]: [], // Place the overItem in the active container
              [overContainer]: [...prevItems[overContainer], activeItem], // Place the activeItem in the over container
            };
          }else if(activeContainer === "container6"){
            return {
              ...prevItems,
              [activeContainer]: prevItems[activeContainer].map(item =>
                item === activeItem ? overItem : item // Replace activeItem with overItem
              ),
              [overContainer]: [activeItem], // Append activeItem to overContainer
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
          console.log("asda")
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
