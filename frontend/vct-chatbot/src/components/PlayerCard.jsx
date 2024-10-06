import * as React from "react";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from '@dnd-kit/utilities';

export function Item(props) {
  const { id, isSmall } = props;

  const style = {
    width: isSmall ? "3.23vw" : "9vw",
    height: isSmall ? "3.23vw" : "9vw",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    border: "1px solid black",
    background: "white",
    transition: "width 0.3s ease, height 0.3s ease", // Apply transition here
    
  };

  return <div style={style}>{id}</div>;
}

export default function PlayerCard(props) {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id: props.id });
  const isSmall = props.container === "container6";

  const style = {
    
    transform: CSS.Transform.toString(transform),
    transition  // Apply transition to dragging animation
  };

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      <Item id={props.id} isSmall={isSmall} />
    </div>
  );
}
