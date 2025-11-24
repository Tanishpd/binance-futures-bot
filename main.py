#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot - Command Line Interface
"""

import sys
import logging
from bot import BasicBot
import config

# Setup console logging in addition to file logging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(config.LOG_FORMAT))
logging.getLogger().addHandler(console_handler)

logger = logging.getLogger(__name__)


def validate_symbol(symbol):
    """Validate trading symbol format."""
    if not symbol or not isinstance(symbol, str):
        return False
    return symbol.isupper() and len(symbol) >= 6
    

def validate_side(side):
    """Validate order side."""
    return side.upper() in ['BUY', 'SELL']


def validate_positive_number(value, name):
    """Validate that a value is a positive number."""
    try:
        num = float(value)
        if num <= 0:
            print(f"Error: {name} must be greater than 0")
            return None
        return num
    except ValueError:
        print(f"Error: {name} must be a valid number")
        return None


def print_header():
    """Print application header."""
    print("\n" + "="*60)
    print("  BINANCE FUTURES TESTNET TRADING BOT")
    print("="*60 + "\n")


def print_menu():
    """Print main menu options."""
    print("\n--- MAIN MENU ---")
    print("1. View Account Information")
    print("2. Check Current Price")
    print("3. Place Market Order")
    print("4. Place Limit Order")
    print("5. Place Stop-Limit Order")
    print("6. Check Order Status")
    print("7. Cancel Order")
    print("8. Exit")
    print("-" * 40)


def get_user_input(prompt, validator=None):
    """Get and validate user input."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("Error: Input cannot be empty")
            continue
        if validator and not validator(value):
            print("Error: Invalid input format")
            continue
        return value


def display_order_details(order):
    """Display order details in a formatted way."""
    print("\n" + "="*60)
    print("  ORDER DETAILS")
    print("="*60)
    print(f"Order ID:       {order.get('orderId', 'N/A')}")
    print(f"Symbol:         {order.get('symbol', 'N/A')}")
    print(f"Side:           {order.get('side', 'N/A')}")
    print(f"Type:           {order.get('type', 'N/A')}")
    print(f"Quantity:       {order.get('origQty', 'N/A')}")
    print(f"Price:          {order.get('price', 'N/A')}")
    print(f"Status:         {order.get('status', 'N/A')}")
    print(f"Time in Force:  {order.get('timeInForce', 'N/A')}")
    if 'stopPrice' in order and order['stopPrice'] != '0':
        print(f"Stop Price:     {order.get('stopPrice', 'N/A')}")
    print("="*60 + "\n")


def view_account_info(bot):
    """View account information."""
    try:
        print("\nFetching account information...")
        account = bot.get_account_info()
        
        print("\n" + "="*60)
        print("  ACCOUNT INFORMATION")
        print("="*60)
        print(f"Total Wallet Balance: {account.get('totalWalletBalance', 'N/A')} USDT")
        print(f"Available Balance:    {account.get('availableBalance', 'N/A')} USDT")
        print(f"Total Unrealized PNL: {account.get('totalUnrealizedProfit', 'N/A')} USDT")
        
        print("\n--- Positions ---")
        positions = [p for p in account.get('positions', []) if float(p.get('positionAmt', 0)) != 0]
        if positions:
            for pos in positions:
                print(f"Symbol: {pos['symbol']}, Amount: {pos['positionAmt']}, Entry Price: {pos['entryPrice']}")
        else:
            print("No open positions")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\nError: Failed to fetch account information - {str(e)}")
        logger.error(f"Error in view_account_info: {str(e)}")


def check_current_price(bot):
    """Check current price of a symbol."""
    try:
        symbol = get_user_input("Enter symbol (e.g., BTCUSDT): ", validate_symbol).upper()
        
        print(f"\nFetching current price for {symbol}...")
        price = bot.get_current_price(symbol)
        
        print(f"\n{'='*60}")
        print(f"  Current Price of {symbol}: {price} USDT")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\nError: Failed to fetch price - {str(e)}")
        logger.error(f"Error in check_current_price: {str(e)}")


def place_market_order(bot):
    """Place a market order."""
    try:
        print("\n--- MARKET ORDER ---")
        symbol = get_user_input("Enter symbol (e.g., BTCUSDT): ", validate_symbol).upper()
        side = get_user_input("Enter side (BUY/SELL): ", validate_side).upper()
        
        quantity = None
        while quantity is None:
            qty_input = input("Enter quantity: ").strip()
            quantity = validate_positive_number(qty_input, "Quantity")
        
        # Show current price
        current_price = bot.get_current_price(symbol)
        print(f"\nCurrent price: {current_price} USDT")
        print(f"Estimated cost: {current_price * quantity} USDT")
        
        confirm = input("\nConfirm order? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Order cancelled")
            return
        
        print("\nPlacing market order...")
        order = bot.place_market_order(symbol, side, quantity)
        display_order_details(order)
        print("✓ Market order executed successfully!")
        
    except Exception as e:
        print(f"\nError: Failed to place market order - {str(e)}")
        logger.error(f"Error in place_market_order: {str(e)}")


def place_limit_order(bot):
    """Place a limit order."""
    try:
        print("\n--- LIMIT ORDER ---")
        symbol = get_user_input("Enter symbol (e.g., BTCUSDT): ", validate_symbol).upper()
        side = get_user_input("Enter side (BUY/SELL): ", validate_side).upper()
        
        quantity = None
        while quantity is None:
            qty_input = input("Enter quantity: ").strip()
            quantity = validate_positive_number(qty_input, "Quantity")
        
        price = None
        while price is None:
            price_input = input("Enter limit price: ").strip()
            price = validate_positive_number(price_input, "Price")
        
        # Show current price
        current_price = bot.get_current_price(symbol)
        print(f"\nCurrent price: {current_price} USDT")
        print(f"Your limit price: {price} USDT")
        print(f"Total order value: {price * quantity} USDT")
        
        confirm = input("\nConfirm order? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Order cancelled")
            return
        
        print("\nPlacing limit order...")
        order = bot.place_limit_order(symbol, side, quantity, price)
        display_order_details(order)
        print("✓ Limit order placed successfully!")
        
    except Exception as e:
        print(f"\nError: Failed to place limit order - {str(e)}")
        logger.error(f"Error in place_limit_order: {str(e)}")


def place_stop_limit_order(bot):
    """Place a stop-limit order."""
    try:
        print("\n--- STOP-LIMIT ORDER ---")
        symbol = get_user_input("Enter symbol (e.g., BTCUSDT): ", validate_symbol).upper()
        side = get_user_input("Enter side (BUY/SELL): ", validate_side).upper()
        
        quantity = None
        while quantity is None:
            qty_input = input("Enter quantity: ").strip()
            quantity = validate_positive_number(qty_input, "Quantity")
        
        stop_price = None
        while stop_price is None:
            stop_input = input("Enter stop price (trigger price): ").strip()
            stop_price = validate_positive_number(stop_input, "Stop price")
        
        price = None
        while price is None:
            price_input = input("Enter limit price: ").strip()
            price = validate_positive_number(price_input, "Limit price")
        
        # Show current price
        current_price = bot.get_current_price(symbol)
        print(f"\nCurrent price: {current_price} USDT")
        print(f"Stop price: {stop_price} USDT (trigger)")
        print(f"Limit price: {price} USDT")
        print(f"Total order value: {price * quantity} USDT")
        
        confirm = input("\nConfirm order? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Order cancelled")
            return
        
        print("\nPlacing stop-limit order...")
        order = bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
        display_order_details(order)
        print("✓ Stop-limit order placed successfully!")
        
    except Exception as e:
        print(f"\nError: Failed to place stop-limit order - {str(e)}")
        logger.error(f"Error in place_stop_limit_order: {str(e)}")


def check_order_status(bot):
    """Check the status of an order."""
    try:
        print("\n--- CHECK ORDER STATUS ---")
        symbol = get_user_input("Enter symbol (e.g., BTCUSDT): ", validate_symbol).upper()
        order_id = get_user_input("Enter order ID: ")
        
        try:
            order_id = int(order_id)
        except ValueError:
            print("Error: Order ID must be a number")
            return
        
        print(f"\nFetching order status...")
        order = bot.get_order_status(symbol, order_id)
        display_order_details(order)
        
    except Exception as e:
        print(f"\nError: Failed to fetch order status - {str(e)}")
        logger.error(f"Error in check_order_status: {str(e)}")


def cancel_order(bot):
    """Cancel an order."""
    try:
        print("\n--- CANCEL ORDER ---")
        symbol = get_user_input("Enter symbol (e.g., BTCUSDT): ", validate_symbol).upper()
        order_id = get_user_input("Enter order ID: ")
        
        try:
            order_id = int(order_id)
        except ValueError:
            print("Error: Order ID must be a number")
            return
        
        confirm = input(f"\nConfirm cancellation of order {order_id}? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Cancellation aborted")
            return
        
        print(f"\nCancelling order...")
        result = bot.cancel_order(symbol, order_id)
        
        print(f"\n{'='*60}")
        print(f"  ORDER CANCELLED")
        print(f"{'='*60}")
        print(f"Order ID: {result.get('orderId', 'N/A')}")
        print(f"Symbol:   {result.get('symbol', 'N/A')}")
        print(f"Status:   {result.get('status', 'N/A')}")
        print(f"{'='*60}\n")
        print("✓ Order cancelled successfully!")
        
    except Exception as e:
        print(f"\nError: Failed to cancel order - {str(e)}")
        logger.error(f"Error in cancel_order: {str(e)}")


def main():
    """Main application entry point."""
    print_header()
    
    # Check for API credentials
    if not config.BINANCE_API_KEY or not config.BINANCE_API_SECRET:
        print("ERROR: API credentials not found!")
        print("\nPlease follow these steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your Binance Testnet API credentials to .env")
        print("3. Run the bot again\n")
        sys.exit(1)
    
    # Initialize bot
    try:
        print("Initializing bot...")
        bot = BasicBot(
            api_key=config.BINANCE_API_KEY,
            api_secret=config.BINANCE_API_SECRET,
            testnet=True
        )
        print("✓ Bot initialized successfully!\n")
        logger.info("Trading bot started successfully")
    except Exception as e:
        print(f"Error: Failed to initialize bot - {str(e)}")
        logger.error(f"Failed to initialize bot: {str(e)}")
        sys.exit(1)
    
    # Main loop
    while True:
        try:
            print_menu()
            choice = input("Enter your choice (1-8): ").strip()
            
            if choice == '1':
                view_account_info(bot)
            elif choice == '2':
                check_current_price(bot)
            elif choice == '3':
                place_market_order(bot)
            elif choice == '4':
                place_limit_order(bot)
            elif choice == '5':
                place_stop_limit_order(bot)
            elif choice == '6':
                check_order_status(bot)
            elif choice == '7':
                cancel_order(bot)
            elif choice == '8':
                print("\nThank you for using the trading bot. Goodbye!")
                logger.info("Trading bot shut down by user")
                sys.exit(0)
            else:
                print("\nError: Invalid choice. Please enter a number between 1 and 8.")
        
        except KeyboardInterrupt:
            print("\n\nBot interrupted by user. Shutting down...")
            logger.info("Trading bot interrupted by user")
            sys.exit(0)
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")
            logger.error(f"Unexpected error in main loop: {str(e)}")


if __name__ == "__main__":
    main()
