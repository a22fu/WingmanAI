import React from "react";
import player_img from '../resources/blank_player.png'
import {useDroppable} from '@dnd-kit/core';
import {
  rectSortingStrategy,
  SortableContext,
} from "@dnd-kit/sortable";


import PlayerCard from "./PlayerCard";



export default function PlayerBox(props) {
  const { id, items,hiddenIds, containerStyle, search} = props;
  
  const { setNodeRef } = useDroppable({
    id
  });
  items.sort()

  let map
  if (search != null){
    map = items.filter((item) => {
      return search.toLowerCase() === '' ? item : item.toLowerCase().includes(search.toLowerCase());
    }).map((item) =>
      (hiddenIds.includes(item)) ? null : ( // Hide the dragged item from its original container
        <PlayerCard key={item} id={item} playerId={item} container = {id}/>
      )
    )
  }else{
    map = items.map((item) =>
      (hiddenIds.includes(item)) ? null : ( // Hide the dragged item from its original container
        <PlayerCard key={item} id={item} playerId={item} container = {id}/>
      )
    )
  }

  return (
    <SortableContext
      id={id}
      items={items}
      strategy={rectSortingStrategy}
      hiddenIds = {hiddenIds}
      >
      <div ref={setNodeRef} style={containerStyle}>
      {map.length === 0 && id !== 'container6'? <img src={player_img} alt="player" width="80%"/> : map}
      </div>
    </SortableContext>
  );
}

