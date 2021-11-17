import os
import sys
import logging
import uuid
import random
from math import floor
import psycopg2
from psycopg2.extras import register_uuid
from psycopg2.errors import OperationalError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def create_accounts(conn, num):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS accounts (id UUID PRIMARY KEY, balance INT8)")
        while num > 0:
            account_id = uuid.uuid4()
            account_balance = floor(random.random()*1_000_000)
            cur.execute("UPSERT INTO accounts (id, balance) VALUES (%s, %s)", [
                        account_id, account_balance])
            logger.info(
                f"Created new account with id {account_id} and balance {account_balance}.")
            num -= 1
        logger.debug(f"create_accounts(): status message: {cur.statusmessage}")
    conn.commit()


def lambda_handler(event, context):

    register_uuid()

    try:
        conn = psycopg2.connect(os.path.expandvars(os.environ['DATABASE_URL']))
    except OperationalError as err:
        logger.error("Could not connect to CockroachDB.")
        logger.error(err)
        sys.exit()

    logger.info("Hey! You successfully connected to your CockroachDB cluster.")

    create_accounts(conn, 5)

    logger.info("Database initialized.")

    return
