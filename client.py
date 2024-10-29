import aiohttp
import asyncio
import time
import sqlite3

DB_PATH = 'prices.db'

async def fetch_price(session, ticker):
    url = f'https://www.deribit.com/api/v2/public/get_index_price?index_name={ticker}'
    async with session.get(url) as response:
        return await response.json()

async def save_price(ticker, price):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            price REAL,
            timestamp INTEGER
        )
    ''')
    cursor.execute('INSERT INTO prices (ticker, price, timestamp) VALUES (?, ?, ?)', (ticker, price, int(time.time())))
    conn.commit()
    conn.close()

async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            for ticker in ['btc_usd', 'eth_usd']:
                data = await fetch_price(session, ticker)
                price = data['result']['index_price']
                await save_price(ticker, price)
            await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())