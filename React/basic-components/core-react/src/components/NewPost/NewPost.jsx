import { useState } from 'react';
import classes from './NewPost.module.css';


function NewPost(props) {
  const [body, setBody] = useState("")
  const [author, setAuthor] = useState("")
  const [current, setValue ] = useState("")
  // stateData[0] // current value
  // stateDada[1] // state updating function

  function changeBodyHandler(event) {
    console.log('changeBodyHandler(event.target.value;)', event.target.value)
    setValue(event.target.value)
      
  }

  function onSubmit(event) {
    console.log('PostsList.onSubmit(event.target.value;)', event.target.value)
    event.preventDefault();
    const data = {
      body: body,
      author: author
    }
    console.log(data)
    props.onSubmit(data)
  }

  function changeBodyHandler(event) {
    console.log('PostsList.changeBodyHandler(event.target.value;)', event.target.value)
    setBody(event.target.value)
}

function changeAuthorHandler(event) {
    console.log('PostsList.changeAuthorHandler(event.target.value;)', event.target.value)
    setAuthor(event.target.value)
}
  return (
    <form className={classes.form} onSubmit={onSubmit}>
      <p>
        <label htmlFor="body">Text</label>
        <textarea id="body" required rows={3} onChange={changeBodyHandler}/>
      </p>
      <p>{current}</p>
      <p>
        <label htmlFor="name">Your name</label>
        <input type="text" id="name" required onChange={changeAuthorHandler} />
      </p>

      <p className={classes.actions}>
      <button type='button' onClick={props.onCancel}>Cancel</button>
      <button type='submit'>Submit</button>
      </p>
    </form>
  );
}

export default NewPost;