import React, { useState } from "react";

import {useDroppable} from '@dnd-kit/core';
import {
  SortableContext,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";


import PlayerCard from "./PlayerCard";


const containerStyle = {
  background: "#dadada",
  padding: 10,
  margin: 10,
  flex: 1
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

