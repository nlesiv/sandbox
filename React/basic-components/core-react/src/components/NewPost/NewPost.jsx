import { useState } from 'react';
import classes from './NewPost.module.css';


function NewPost(props) {
  const [current, setValue ] = useState("")
  // stateData[0] // current value
  // stateDada[1] // state updating function

  function changeBodyHandler(event) {
    console.log('changeBodyHandler(event.target.value;)', event.target.value)
    setValue(event.target.value)
      
  }
  return (
    <form className={classes.form}>
      <p>
        <label htmlFor="body">Text</label>
        <textarea id="body" required rows={3} onChange={props.onBodyChange}/>
      </p>
      <p>{current}</p>
      <p>
        <label htmlFor="name">Your name</label>
        <input type="text" id="name" required onChange={props.onAuthorChange} />
      </p>
    </form>
  );
}

export default NewPost;