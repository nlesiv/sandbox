import { useState} from 'react'
import styles from './PostsList.module.css'
import Post from '../Post/Post';
import NewPost from "../NewPost/NewPost";
import Modal from '../Modal/Modal';

function PostsList(props) {
    // const chosenName = Math.random() > .5 ? "Superman" : "Batman"
    const [body, setBody] = useState("")
    const [author, setAuthor] = useState("")
    const [modalOpen, setModalState] = useState(true)

    function changeBodyHandler(event) {
        console.log('PostsList.changeBodyHandler(event.target.value;)', event.target.value)
        setBody(event.target.value)
    }

    function changeAuthorHandler(event) {
        console.log('PostsList.changeAuthorHandler(event.target.value;)', event.target.value)
        setAuthor(event.target.value)
    }

    function toggleModal(event) {
        setModalState(false)
    }

    return (
        <>
        {modalOpen &&
        ( <Modal onClose={toggleModal}>
            <NewPost onBodyChange={changeBodyHandler} onAuthorChange={changeAuthorHandler} />
        </Modal> )}
        <ul className={styles.posts}>
             <Post author={author} body={body}></Post>
             <Post author="Batman" body="React is awesomer"></Post>
        </ul>
        </>
    );
}

export default PostsList;