import classes from "./Modal.module.css";
import { useState } from "react";

function Modal(props) {

  return (
    <>
      <div className={classes.backdrop} onClick={props.onClose}/>
      <dialog open className={classes.modal}>
      {props.children}
      </dialog>
    </>
  )
}

export default Modal;