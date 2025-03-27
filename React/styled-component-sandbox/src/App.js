import logo from './logo.svg';
import './App.css';
import Card from './components/Card';
import GlobalStyles from './global-styles';
import styled, {ThemeProvider} from 'styled-components'
import {useState} from 'react';
import Spinner from './components/Spinner'; 
import Form from "./components/Form"
import List from "./components/List"
const BaseTheme = {
  color: '#222',
  background: '#fff',
}

const DarkTheme = {
  color: '',
  background: '#222',
}

const Container = styled.div`
  padding: 2rem;
  color:${(props) => {
    return props.theme.color
  }};

  background:${(props) => {
    return props.theme.background
  }};
  
`
function App() {
  const [baseTheme, setTheme] = useState(true)

  const toggleTheme = () => {
    console.log("toggleTheme", this)
    setTheme(!baseTheme)
  }
  return (
    <ThemeProvider theme={baseTheme === true ? BaseTheme : DarkTheme} className="App">
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
      {/* <GlobalStyles /> */}
      <Container>
        <h2>Hello World</h2>
        <Card></Card>
        <button className='btn' onClick={toggleTheme}>Toggle me</button>
      </Container>

      {/* <Spinner></Spinner> */}

    <Form></Form>

    <List></List>

      
    </ThemeProvider>
  );
}

export default App;
