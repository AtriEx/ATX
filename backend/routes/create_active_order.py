"""Creates buy and sell orders"""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from database import supabase_middleman


def create_active_buy_sell_order(data: dict) -> str:
    """Create a buy or sell order for a stock."""
    buy_or_sell = data["buy_or_sell"]
    price = data["price"]
    expiry = data["expirey"]
    quantity = data["quantity"]
    stock_id = data["stockId"]
    user_id = data["userId"]

    expiry = expiry.replace(
        "Z", "+00:00"
    )  # Replace Z with +00:00 to make it ISO 8601 compliant
    expiry = datetime.fromisoformat(expiry)  # Convert expiry to datetime object
    errors = []
    if price < 1:
        errors.append("Price must be greater than 0")
    if quantity < 1:
        errors.append("Quantity must be greater than 0")
    if expiry < datetime.now(timezone.utc):
        errors.append("Expiry date cannot be in the past")
    if not supabase_middleman.fetch_stock_price(stock_id):
        errors.append("Stock not found")
    if errors:
        return ", ".join(errors)

    # validate user_id is a valid uuid and it exists
    try:
        UUID(hex=user_id)  # throws value error if not a valid uuid
        user_profile = supabase_middleman.get_user_profile(user_id)
        if not user_profile:
            errors.append("User not found")
    except ValueError:
        errors.append("user_id is not in valid UUID format")

    if errors:
        return ", ".join(errors)

    # validate that if order is a buy order, user has enough balance,
    # or if order is a sell order, user has enough quantity
    if buy_or_sell:  # Buy order
        user_profile = supabase_middleman.get_user_profile(user_id)
        if not user_profile:
            errors.append("User not found")
        if user_profile["balance"] < price * quantity:
            errors.append("Insufficient balance")
    else:  # Sell order
        # portfolio = supabase_middleman.fetch_portfolio(user_id, stock_id)
        portfolio = supabase_middleman.get_user_portfolio(user_id)[stock_id]
        if not portfolio:
            errors.append("Stock not found in users portfolio")
        if portfolio["quantity"] < 1:
            errors.append("User does not own stock")
        if portfolio["quantity"] < quantity:
            errors.append("Insufficient quantity")

    if errors:
        return ", ".join(errors)

    time_posted = datetime.now().isoformat()

    generated_order_id = str(uuid4())

    if buy_or_sell:
        supabase_middleman.update_user_balance(user_id, price * quantity * -1)
        # supabase_middleman.escrow_funds(user_id, price, quantity)
    else:
        supabase_middleman.update_user_portfolio(user_id, stock_id, quantity * -1)
        # supabase_middleman.escrow_stock(user_id, stock_id, quantity)

    expiry = str(expiry)
    entries = []
    # Generate an entry for each quantity and insert those entries into the table
    entries = [
        {
            "time_posted": time_posted,
            "buy_or_sell": buy_or_sell,
            "price": price,
            "expirey": expiry,
            "quantity": quantity,
            "stockId": stock_id,
            "userId": user_id,
            "orderId": generated_order_id,
            "has_been_processed": False,
        }
        for _ in range(quantity)
    ]
    # Insert the entry into the active_buy_sell table
    supabase_middleman.insert_entry("active_buy_sell", entries)
    return "Active order created"
