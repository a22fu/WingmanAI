import * as React from "react";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from '@dnd-kit/utilities';
import data from '../players/imgdict.json'

export function Item(props) {
  const { id, isSmall } = props;

  const style = {
    width: isSmall ? "4.6vw" : "9vw",
    height: isSmall ? "4.6vw" : "9vw",
  };
  var image = data[id]
  if (!image){
    image = "https://www.vlr.gg/img/base/ph/sil.png"
  }
  return (
    <div style={style} className="player-card">
      <img src={image} alt="Item" className="player-image" />
      <div className="player-text">{id}</div> {/* Display the id as text */}
    </div>
  );
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
