import styles from './Post.module.css'

function Post(props) {
    // const chosenName = Math.random() > .5 ? "Superman" : "Batman"
    return (
        <div className={styles.post}>
            <p className={styles.author}>{props.author}</p>
            <p className={styles.text}>{props.body}</p>
        </div>
    )
}

export default Post;