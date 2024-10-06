import React, { useState } from "react";

import {useDroppable} from '@dnd-kit/core';
import {
  rectSortingStrategy,
  SortableContext,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";


import PlayerCard from "./PlayerCard";



export default function PlayerBox(props) {
  const { id, items,hiddenIds, containerStyle, search} = props;
  
  const { setNodeRef } = useDroppable({
    id
  });
  var map;
  console.log(items)
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
      
      {map}
      </div>
    </SortableContext>
  );
}

