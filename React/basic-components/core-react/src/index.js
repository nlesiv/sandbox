import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Posts from './routes/Posts';
import reportWebVitals from './reportWebVitals';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import NewPost from './components/NewPost/NewPost';
import RootLayout from './routes/RootLayout';
const router = createBrowserRouter([
  {
    route: '/',
    element: <RootLayout />,
    children: [
      {
        path: "/",
        element: <Posts />
      },
      {
        path: "/create-post",
        element: <NewPost />
      }
    ]
  },
  
 
]);
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    {/* <App /> */}
    <RouterProvider router={router}/>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
