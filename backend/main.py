# from routers import items, users
from datetime import datetime, timedelta
from fastapi import FastAPI
from supabase import create_client, Client
from APIFiles import supabaseMiddleman
from APIFiles import createActiveOrder
from APIFiles import quickBuy
from dotenv import load_dotenv
import os


app = FastAPI()



@app.get('/buyOrder')
async def testEntry():
    await createActiveOrder.createBuyOrder()
    return "Test entry inserted"


@app.get('/qb')
async def buyFlow():
    await quickBuy.buyMethod()
    return "Quick buy executed"
