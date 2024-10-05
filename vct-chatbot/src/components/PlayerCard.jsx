import * as React from "react";

import { useSortable } from "@dnd-kit/sortable";


import {CSS} from '@dnd-kit/utilities';

// Within your component that receives `transform` from `useDraggable`:


export function Item(props) {
  const { id } = props;

  const style = {
    width: "9vw",
    height: "9vw",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    border: "1px solid black",

    background: "white"
  };

  return <div style={style}>{id}</div>;
}

export default function PlayerCard(props) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition
  } = useSortable({ id: props.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition
  };

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      <Item id={props.id} />
    </div>
  );
}