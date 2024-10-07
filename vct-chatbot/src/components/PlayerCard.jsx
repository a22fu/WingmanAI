import * as React from "react";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from '@dnd-kit/utilities';
import data from '../players/imgdict.json'

export function Item(props) {
  const { id, isSmall } = props;

  const style = {
    width: isSmall ? "4.6vw" : "9vw",
    height: isSmall ? "4.6vw" : "9vw",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    border: "1px solid black",
    background: "white",
    position: "relative", // Set position to relative for absolute positioning of text
    overflow: "hidden", // Ensures no overflow from the container
    transition: "width 0.3s ease, height 0.3s ease", // Apply transition here
  };

  const imgStyle = {
    width: "100%", // Make the image fit the container
    height: "100%",
    objectFit: "cover", // Ensures the image scales properly and maintains aspect ratio
  };

  const textStyle = {
    position: "absolute", // Position text absolutely over the image
    color: "white", // Text color
    backgroundColor: "rgba(0, 0, 0, 0.5)", // Semi-transparent background for better visibility
    padding: "5px", // Padding around text
    bottom: "10px", // Position from bottom
    left: "50%", // Center the text horizontally
    transform: "translateX(-50%)", // Centering adjustment
    borderRadius: "5px", // Rounded corners for the background
    textAlign: "center", // Center the text
    width: "90%", // Optional: control the text width
  };
  var image = data[id]
  if (!image){
    image = "https://www.vlr.gg/img/base/ph/sil.png"
  }
  return (
    <div style={style}>
      <img src={image} alt="Item" style={imgStyle} />
      <div style={textStyle}>{id}</div> {/* Display the id as text */}
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
