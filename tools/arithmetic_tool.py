import os
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper 
from langchain.tools import tool
from dotenv import load_dotenv
load_dotenv()

@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The product of a and b.
    """
    return a * b

@tool
def add(a: int, b: int) -> int:
    """
    Add two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The sum of a and b.
    """
    return a + b

@tool 
def currency_convertor(from_curr: str, to_curr: str, value: float) -> float:
    """
    Convert a monetary amount from one currency to another using the AlphaVantage exchange rate API.

    Args:
        from_curr (str): The ISO currency code of the source currency.
        to_curr (str): The ISO currency code of the target currency.
        value (float): The monetary amount to convert.

    Returns:
        float: The converted amount in the target currency.
    """
    os.environ["ALPHAVANTAGE_API_KEY"] = os.getenv("ALPHAVANTAGE_API_KEY") 
    alpha_vantage = AlphaVantageAPIWrapper() 
    response = alpha_vantage._get_exchange_rate(from_curr, to_curr) 
    exchange_rate = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
    return value * float(exchange_rate)