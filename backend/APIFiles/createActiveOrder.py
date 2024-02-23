import os
from fastapi import FastAPI
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta
from APIFiles import testData
from APIFiles import supabaseMiddleman
app=FastAPI()
load_dotenv()



#
async def createBuyOrder():
    # Insert a test entry into the active_buy_sell table
    testEntry = testData.testEntry1()
    supabaseMiddleman.insertEntry('active_buy_sell', testEntry)
    return 

async def createSellOrder():
    # Insert a test entry into the active_buy_sell table
    testEntry = testData.testEntry2()
    supabaseMiddleman.insertEntry('active_buy_sell', testEntry)
    return