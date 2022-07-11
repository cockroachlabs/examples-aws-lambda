import os
import logging
import random
from math import floor
from psycopg2.pool import SimpleConnectionPool

logger = logging.getLogger()
logger.setLevel(logging.INFO)

pool = None


def create_accounts(p, n):
    conn = p.getconn()
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS accounts (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), balance INT8)")
        conn.commit()
        while n > 0:
            account_balance = floor(random.random()*1_000_000)
            cur.execute("UPSERT INTO accounts (id, balance) VALUES (DEFAULT, %s)", [
                        account_balance])
            logger.info(
                f"Created new account with balance {account_balance}.")
            n -= 1
        logger.debug(f"create_accounts(): status message: {cur.statusmessage}")
        conn.commit()


def lambda_handler(event, context):
    global pool
    if not pool:
        pool = SimpleConnectionPool(0, 1, dsn=os.environ['DATABASE_URL'], application_name="$ docs_lambda_python")

    create_accounts(pool, 5)

    logger.info("Database initialized.")

    return
