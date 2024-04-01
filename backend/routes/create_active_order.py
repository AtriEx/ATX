"""Creates buy and sell orders"""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import HTTPException
from pydantic import BaseModel
from starlette.status import HTTP_400_BAD_REQUEST

from database import supabase_middleman


class ErrorResponse(BaseModel):
    error_code: int
    error_message: str
    details: str = None  # Optional field


def create_active_buy_sell_order(data: dict) -> str:
    """Create a buy or sell order for a stock."""
    buy_or_sell = data["buy_or_sell"]
    price = data["price"]
    expirey = data["expirey"]
    quantity = data["quantity"]
    stock_id = data["stockId"]
    user_id = data["userId"]

    expirey = expirey.replace(
        "Z", "+00:00"
    )  # Replace Z with +00:00 to make it ISO 8601 compliant
    expirey = datetime.fromisoformat(expirey)  # Convert expirey to datetime object

    if price < 1:
        raise_http_exception(
            status_code=HTTP_400_BAD_REQUEST,
            error_code=400,
            error_message="Price must be greater than 0",
        )
    if quantity < 1:
        raise_http_exception(
            status_code=HTTP_400_BAD_REQUEST,
            error_code=400,
            error_message="Quantity must be greater than 0",
        )
    if expirey < datetime.now(timezone.utc):
        raise_http_exception(
            status_code=HTTP_400_BAD_REQUEST,
            error_code=400,
            error_message="Expirey date cannot be in the past",
        )

    if not supabase_middleman.fetch_stock_price(stock_id):
        raise_http_exception(
            status_code=HTTP_400_BAD_REQUEST,
            error_code=400,
            error_message="Stock not found",
        )

    # validate user_id is a valid uuid and it exists
    try:
        UUID(hex=user_id)  # throws value error if not a valid uuid
        # user_profile = supabase_middleman.fetch_profile(user_id)
        user_profile = supabase_middleman.get_user_profile(user_id)
        if not user_profile:
            raise_http_exception(
                status_code=HTTP_400_BAD_REQUEST,
                error_code=400,
                error_message="User not found",
            )
    except ValueError:
        raise_http_exception(
            status_code=HTTP_400_BAD_REQUEST,
            error_code=400,
            error_message="user_id is not in valid UUID format",
        )

    # validate that if order is a buy order, user has enough balance,
    # or if order is a sell order, user has enough quantity
    if buy_or_sell:  # Buy order
        user_profile = supabase_middleman.get_user_profile(user_id)
        if not user_profile:
            raise_http_exception(
                status_code=HTTP_400_BAD_REQUEST,
                error_code=400,
                error_message="User not found",
            )
        if user_profile["balance"] < price * quantity:
            raise_http_exception(
                status_code=HTTP_400_BAD_REQUEST,
                error_code=400,
                error_message="Insufficient balance",
            )
    else:  # Sell order
        # portfolio = supabase_middleman.fetch_portfolio(user_id, stock_id)
        portfolio = supabase_middleman.get_user_portfolio(user_id)[stock_id]
        if not portfolio:
            raise_http_exception(
                status_code=HTTP_400_BAD_REQUEST,
                error_code=400,
                error_message="Portfolio not found",
            )
        if portfolio["quantity"] < 1:
            raise_http_exception(
                status_code=HTTP_400_BAD_REQUEST,
                error_code=400,
                error_message="User does not own stock",
            )
        if portfolio["quantity"] < quantity:
            raise_http_exception(
                status_code=HTTP_400_BAD_REQUEST,
                error_code=400,
                error_message="Insufficient quantity",
            )

    time_posted = datetime.now().isoformat()
    # create_active_order.create_active_order(
    #     time_posted, buy_or_sell, price, expirey, quantity, stock_id, user_id
    # )

    generated_order_id = str(uuid4())

    if buy_or_sell:
        supabase_middleman.update_user_balance(user_id, price * quantity * -1)
        # supabase_middleman.escrow_funds(user_id, price, quantity)
    else:
        supabase_middleman.update_user_portfolio(user_id, stock_id, quantity * -1)
        # supabase_middleman.escrow_stock(user_id, stock_id, quantity)

    expirey = str(expirey)
    # Generate an entry for each quantity and insert those entries into the table
    for i in range(quantity):
        entry = {
            "time_posted": time_posted,
            "buy_or_sell": buy_or_sell,
            "price": price,
            "expirey": expirey,
            "quantity": 1,
            "stockId": stock_id,
            "userId": user_id,
            "orderId": generated_order_id,
            "has_been_processed": False,
        }
        # Insert the entry into the active_buy_sell table
        supabase_middleman.insert_entry("active_buy_sell", entry)
    return "Active order created"


def raise_http_exception(status_code, error_code, error_message, details=None):
    error_response = ErrorResponse(
        error_code=error_code, error_message=error_message, details=details
    )
    raise HTTPException(
        status_code=status_code, detail=error_response.model_dump_json()
    )
