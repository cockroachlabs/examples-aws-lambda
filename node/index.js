const { Pool } = require('pg')

let pool

const initTable = async (p) => {
  const client = await p.connect()
  console.log('Initializing table...')
  try {
    const tableInitialized = await client.query(
      `CREATE TABLE IF NOT EXISTS accounts (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          balance INT8
        )`
    )
    console.log(tableInitialized)
  } catch (err) {
    console.log(err.stack)
  } finally {
    client.release()
  }
}

const insertAccounts = async (p) => {
  const client = await p.connect()
  console.log('Inserting new rows into the accounts table...')
  const balanceValue = [Math.floor(Math.random() * 1000)]
  try {
    const accountsInserted = await client.query(
      'INSERT INTO accounts (id, balance) VALUES (DEFAULT, $1)',
      balanceValue
    )
    console.log(accountsInserted)
  } catch (err) {
    console.log(err.stack)
  } finally {
    client.release()
  }
}

exports.handler = async (context) => {
  if (!pool) {
    const connectionString = process.env.DATABASE_URL
    pool = new Pool({
      connectionString,
      max: 1,
      maxLifetimeSeconds = 1800
    })
  }

  await initTable(pool)
  await insertAccounts(pool)
}
