"""API handler for calculating the net worth of a user"""

from database import supabase_middleman


def net_worth_calculator(user_id: str) -> int:
    """
    Gets the user's networth from profile, portfolio, and active_buy_sell

    Args:
        user_id (int): The id of the user whose net worth is requested

    Returns: Net worth of user
    """

    # Get the user's balance
    profile_balance = supabase_middleman.get_user_profile(user_id)["balance"]

    # Get the user's portfolio
    user_portfolio = supabase_middleman.get_user_portfolio(user_id)
    portfolio_balance = 0

    # Calculate the value of the user's portfolio
    for stock in user_portfolio:
        quantity = stock["quantity"]
        stock_price = supabase_middleman.fetch_stock_price(stock["stockId"])
        portfolio_balance += quantity * stock_price

    # Get the user's active buy/sell orders
    active_buy_sell_entries = supabase_middleman.get_user_active_orders(user_id)
    # Calculate the value of the user's active buy/sell orders
    active_order_balance = 0
    for entry in active_buy_sell_entries:
        if entry["buy_or_sell"]:
            active_order_balance += entry["price"] * entry["quantity"] # buy order
        else:
            active_order_balance += (supabase_middleman.fetch_stock_price(entry["stockId"]) * 
                                    entry["quantity"])  # sell order

            
    return active_order_balance + portfolio_balance + profile_balance
