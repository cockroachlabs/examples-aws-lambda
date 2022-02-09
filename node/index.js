const { Pool } = require('pg')

let client
let pool

const initTable = async (client) => {
  console.log('Initializing table...')
  const tableInitialized = await client.query('CREATE TABLE IF NOT EXISTS accounts (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), balance INT8)')
  console.log(tableInitialized)
}

const insertAccounts = async (client) => {
  console.log('Inserting new rows into the accounts table...')
  const balanceValue = [Math.floor(Math.random() * 1000)]
  const accountsInserted = await client.query('INSERT INTO accounts (id, balance) VALUES (DEFAULT, $1)', balanceValue)
  console.log(accountsInserted)
}

exports.handler = async (event, context) => {
  if (!pool) {
    const connectionString = process.env.DATABASE_URL
    pool = new Pool({
      connectionString,
      max: 1,
      min: 0
    })
  }
  if (!client) { client = await pool.connect() }

  await initTable(client)
  await insertAccounts(client)
}
