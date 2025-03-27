import { useState, useEffect, use} from 'react'
import styles from './PostsList.module.css'
import Post from '../Post/Post';
import NewPost from "../NewPost/NewPost";
import Modal from '../Modal/Modal';

function PostsList(props) {
    // const chosenName = Math.random() > .5 ? "Superman" : "Batman"

    const [posts, setPosts] = useState([])

    function addPost(data) {
        console.log("PostsList.addPost", data)

        // fetch("", {
        //     method: "POST",
        //     body: 
        //         JSON.stringify(data),
        //     headers: {
        //         'Content-Type': 'application/json'
        //     }
        // })
        // setPosts([data, ...posts])
        setPosts((existingData) => {
            return [data, ...posts]
        })
        props.onDialogClose()
    }

    useEffect(() => {
        // async function fetchPosts() {
        //     const response = await fetch("");
        //     const data = await response.json()
        //     setPosts(data.posts)
        // }

        // fetchPosts();
    }, [])
    return (
        <>
        {props.dialog &&
        ( <Modal onClose={props.onDialogClose}>
            <NewPost onCancel={props.onDialogClose} onSubmit={addPost} />
        </Modal> )}
        {posts.length > 0 &&  <ul className={styles.posts}>
             {/* <Post author={author} body={body}></Post> */}
             {posts.map((item, indx) => {
                return <Post key={indx} author={item.author} body={item.body}></Post>
             })}
        </ul> || <div>No Posts to view</div> }
       
        </>
    );
}

export default PostsList;