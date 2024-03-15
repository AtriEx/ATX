from database import supabase_middleman


    
def networth_calculator(user_id: str) -> int:
    """
    Gets the user's networth from profile, portfolio, and active_buy_sell

    Args:
        user_id (int): The id of the user whose net worth is requested

    Returns: Net worth of user
    """
    profile_balance = (supabase.table("profiles")
        .select("balance")
        .match({"userId": user_id})
        .execute()
        .data
        .pop()["balance"])

    user_portfolio = (supabase.table("portfolio")
        .select("quantity,stockId")
        .match({"userId": user_id})
        .execute()
        .data)
    portfolio_balance = 0
    for stock in user_portfolio:
        portfolio_balance += stock["quantity"] * supabase_middleman.fetch_stock_price(stock["stockId"])

    active_buy_sell_entries = (supabase.table("active_buy_sell")
        .select("price,quantity,stockId,buy_or_sell,userId")
        .match({"userId": user_id})
        .execute()
        .data)
    active_order_balance = 0
    for entry in active_buy_sell_entries:
        if entry["buy_or_sell"]:
            active_order_balance += entry["price"] * entry["quantity"]
        else:
            active_order_balance += supabase_middleman.fetch_stock_price(entry["stockId"]) * entry["quantity"]

    return active_order_balance + portfolio_balance + profile_balance
   
