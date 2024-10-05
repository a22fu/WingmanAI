import React, { useState } from "react";

import {useDroppable} from '@dnd-kit/core';
import {
  SortableContext,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";


import PlayerCard from "./PlayerCard";


const containerStyle = {
  height: "10vw",
  width: "10vw",
  background: "#dadada",
  padding: 10,
  margin: 10,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  border: "1px solid black",
};
export default function PlayerBox(props) {
  const { id, items } = props;

  const { setNodeRef } = useDroppable({
    id
  });

  return (
    <SortableContext
      id={id}
      items={items}
      strategy={verticalListSortingStrategy}
    >
      <div ref={setNodeRef} style={containerStyle}>
        {items.map((id) => (
          <PlayerCard key={id} id={id} />
        ))}
      </div>
    </SortableContext>
  );
}

