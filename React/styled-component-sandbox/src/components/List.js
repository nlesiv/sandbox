import React from 'react'
import styled, {css} from 'styled-components'

const fruits = ['orange', 'apple', 'banana', 'peach'];

const Item = styled.li`
    list-style-type: none;
    ${
        (props) => {
            return props.odd ? css`
            color:white;
            background: red;
            font-size: 1.5rem;
            padding: 1.5rem;
            `
            : css`
            color:black;
            background: white;
            font-size: 1.5rem;
            padding: 1.5rem;
            `
        }
    }
`

const List = () => {
    return (
        <ul>
            {fruits.map((item, index) => {
                return <Item key={index} odd={(index + 1) % 2 !== 0}>{item}</Item>
            })}
        </ul>
    )
}

export default List;