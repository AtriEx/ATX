"""Helper functions to create test orders"""

from database import supabase_middleman
from util import test_data


def create_buy_order():
    """
    Inserst a test buy entry into active_buy_sell table.

    Returns: None
    """
    test_entry = test_data.test_entry_1()
    supabase_middleman.insert_entry("active_buy_sell", test_entry)


def create_sell_order():
    """
    Inserts a test sell entry into active_buy_sell table.

    Returns: None
    """
    test_entry = test_data.test_entry_2()
    supabase_middleman.insert_entry("active_buy_sell", test_entry)
