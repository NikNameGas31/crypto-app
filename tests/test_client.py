import asyncio
import pytest
from aiohttp import ClientSession
from client import fetch_price

@pytest.mark.asyncio
async def test_fetch_price():
    async with ClientSession() as session:
        data = await fetch_price(session, 'btc_usd')
        assert 'result' in data
        assert 'index_price' in data['result']