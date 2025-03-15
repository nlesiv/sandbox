import React from 'react';
import styled from 'styled-components'

const Card = () => {
    return (
        <StyledCard>
            <img
            src=''
            alt='product'
            />

            <footer>
                <h4>product name</h4>
                <p>$15</p>
            </footer>

        </StyledCard>
    )
}

const StyledCard = styled.article`
    width: 90vw;
    max-width: 300px;
    background: var(--white);
    border-radius: 0.25rem;
    img {
        widht: 100%;
        border-top-left-radius: 0.25rem;
        border-top-right-radius: 0.25rem;
    }

    footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
    }
`

export default Card;