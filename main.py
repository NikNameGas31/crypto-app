from fastapi import FastAPI, Query, HTTPException
import sqlite3

app = FastAPI()
DB_PATH = 'prices.db'

def fetch_prices(ticker):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM prices WHERE ticker = ?', (ticker,))
    data = cursor.fetchall()
    conn.close()
    return data

@app.get("/prices")
def get_prices(ticker: str = Query(...)):
    try:
        return fetch_prices(ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/prices/latest")
def get_latest_price(ticker: str = Query(...)):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM prices WHERE ticker = ? ORDER BY timestamp DESC LIMIT 1', (ticker,))
        data = cursor.fetchone()
        conn.close()
        if data is None:
            raise HTTPException(status_code=404, detail="No data found")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/prices/date")
def get_price_by_date(ticker: str = Query(...), start_date: int = Query(...), end_date: int = Query(...)):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM prices WHERE ticker = ? AND timestamp BETWEEN ? AND ?', (ticker, start_date, end_date))
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))