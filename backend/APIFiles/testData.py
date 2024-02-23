from datetime import datetime, timedelta


#creates a test buy order table entry and returns it
def testEntry1() -> dict:
    testEntry = {"userId": "d8a7ae82-1704-41bf-96a3-9347a5c022c8",
                    "buy_or_sell": True,
                    "stockId": 2,
                    "price": 15,
                    "quantity": 1,
                    "time_posted": datetime.now().isoformat(),
                    "expirey": (datetime.now() + timedelta(hours=1)).isoformat()  # This is a test value; users will input an expiry date
                    }
    return testEntry

#creates a test sell order table entry and returns it
def testEntry2() -> dict:
    testEntry = {"userId": "572a902e-de7a-4739-adfe-f4af32a3f18b",
                    "buy_or_sell": False,
                    "stockId": 2,
                    "price": 15,
                    "quantity": 1,
                    "time_posted": datetime.now().isoformat(),
                    "expirey": (datetime.now() + timedelta(hours=1)).isoformat()  # This is a test value; users will input an expiry date
                    }
    return testEntry