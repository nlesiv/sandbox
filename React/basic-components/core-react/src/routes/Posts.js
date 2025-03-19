import { useState } from 'react';
import '../App.css';
import Post from '../components/Post/Post'
import PostsList from '../components/PostsList/PostsList';
import MainHeader from "../components/MainHeader/MainHeader"
function Posts() {
  const [dialogState, setDialogState] = useState(false);

  function onDialogClose(state) {
    console.log("App.onDialogClose(state)", state);
    setDialogState(false)
  }
  return (
    <>
    <main>
      <PostsList dialog={dialogState} onDialogClose={onDialogClose}/>
     </main>
     </>
  );
}

export default Posts;
