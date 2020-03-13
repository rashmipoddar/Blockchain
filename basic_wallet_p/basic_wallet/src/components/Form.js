import React, { useState } from 'react';
import axios from 'axios';

const Form = () => {

  const [userId, setUserId] = useState('');
  const [balance, setBalance] = useState(0);
  const [blocks, setBlocks] = useState([]);

  const handleChange = (event) => {
    setUserId(event.target.value)
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    axios.get('http://0.0.0.0:5000/chain')
    .then(response => {
      console.log(response);
      // console.log(response.data.chain);
      let chainBlocks = response.data.chain;
      chainBlocks.forEach(block => {
        // console.log('Inside the first for each');
        block.transactions.forEach(transaction => {
          if (transaction.sender === `${userId}`) {
            setBalance(prevBalance => prevBalance - transaction.amount)
            setBlocks(b => b.concat(transaction));
          } else if (transaction.recipient === `${userId}`) {
            setBalance(prevBalance => prevBalance + transaction.amount)
            setBlocks(b => b.concat(transaction));
          }
        })
      });
    })
    .catch(error => {
      console.log(error);
    })
  }

  const handleRefresh = (event) => {
    event.preventDefault();
    setBalance(0);
    setBlocks([]);
    axios.get('http://0.0.0.0:5000/chain')
    .then(response => {
      console.log(response);
      // console.log(response.data.chain);
      let chainBlocks = response.data.chain;
      chainBlocks.forEach(block => {
        // console.log('Inside the first for each');
        block.transactions.forEach(transaction => {
          if (transaction.sender === `${userId}`) {
            setBalance(prevBalance => prevBalance - transaction.amount)
            setBlocks(b => b.concat(transaction));
          } else if (transaction.recipient === `${userId}`) {
            setBalance(prevBalance => prevBalance + transaction.amount)
            setBlocks(b => b.concat(transaction));
          }
        })
      });
    })
    .catch(error => {
      console.log(error);
    })
  }

  // console.log('Block:', blocks);

  return (
    <>
      <form onSubmit={handleSubmit}>
        <input
          name='id'
          placeholder='Enter your ID'
          value={userId}
          onChange={handleChange}
        />
      </form>
      <button onClick={handleRefresh}>Refresh</button>
      <h1>Balance: {balance}</h1>
      <h1>All transactions by the entered user:</h1>
      {blocks.length > 0 ? (
        blocks.map((block, index) => (
          <div key={index}>
            <h1>Sender: {block.sender}</h1>
            <h1>Recipient: {block.recipient}</h1>
            <h1>Amount: {block.amount}</h1>
          </div>
        ))
      ) : null}

    </>
  )

}

export default Form;