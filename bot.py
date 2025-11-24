from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import logging
import config

# Setup logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)


class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        """
        Initialize the trading bot with API credentials.
        
        Args:
            api_key (str): Binance API key
            api_secret (str): Binance API secret
            testnet (bool): Use testnet if True, production if False
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        try:
            self.client = Client(api_key, api_secret, testnet=testnet)
            if testnet:
                self.client.API_URL = config.TESTNET_BASE_URL
            logger.info(f"BasicBot initialized with testnet={testnet}")
        except Exception as e:
            logger.error(f"Failed to initialize client: {str(e)}")
            raise
    
    def get_account_info(self):
        """
        Get account information including balances.
        
        Returns:
            dict: Account information
        """
        try:
            logger.info("Fetching account information")
            account = self.client.futures_account()
            logger.info("Account information retrieved successfully")
            return account
        except BinanceAPIException as e:
            logger.error(f"API Exception in get_account_info: {e.status_code} - {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error in get_account_info: {str(e)}")
            raise
    
    def place_market_order(self, symbol, side, quantity):
        """
        Place a market order.
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): 'BUY' or 'SELL'
            quantity (float): Order quantity
            
        Returns:
            dict: Order details
        """
        try:
            logger.info(f"Placing MARKET order: {side} {quantity} {symbol}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            
            logger.info(f"Market order placed successfully: Order ID {order['orderId']}")
            logger.info(f"Order details: {order}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"API Exception in place_market_order: {e.status_code} - {e.message}")
            raise
        except BinanceOrderException as e:
            logger.error(f"Order Exception in place_market_order: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in place_market_order: {str(e)}")
            raise
    
    def place_limit_order(self, symbol, side, quantity, price, time_in_force='GTC'):
        """
        Place a limit order.
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): 'BUY' or 'SELL'
            quantity (float): Order quantity
            price (float): Limit price
            time_in_force (str): GTC (Good Till Cancel), IOC (Immediate or Cancel), FOK (Fill or Kill)
            
        Returns:
            dict: Order details
        """
        try:
            logger.info(f"Placing LIMIT order: {side} {quantity} {symbol} at {price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce=time_in_force
            )
            
            logger.info(f"Limit order placed successfully: Order ID {order['orderId']}")
            logger.info(f"Order details: {order}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"API Exception in place_limit_order: {e.status_code} - {e.message}")
            raise
        except BinanceOrderException as e:
            logger.error(f"Order Exception in place_limit_order: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in place_limit_order: {str(e)}")
            raise
    
    def place_stop_limit_order(self, symbol, side, quantity, price, stop_price, time_in_force='GTC'):
        """
        Place a stop-limit order.
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): 'BUY' or 'SELL'
            quantity (float): Order quantity
            price (float): Limit price
            stop_price (float): Stop price (trigger price)
            time_in_force (str): GTC (Good Till Cancel), IOC (Immediate or Cancel), FOK (Fill or Kill)
            
        Returns:
            dict: Order details
        """
        try:
            logger.info(f"Placing STOP_LIMIT order: {side} {quantity} {symbol} at {price}, stop at {stop_price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                timeInForce=time_in_force
            )
            
            logger.info(f"Stop-limit order placed successfully: Order ID {order['orderId']}")
            logger.info(f"Order details: {order}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"API Exception in place_stop_limit_order: {e.status_code} - {e.message}")
            raise
        except BinanceOrderException as e:
            logger.error(f"Order Exception in place_stop_limit_order: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in place_stop_limit_order: {str(e)}")
            raise
    
    def get_order_status(self, symbol, order_id):
        """
        Get the status of a specific order.
        
        Args:
            symbol (str): Trading pair
            order_id (int): Order ID
            
        Returns:
            dict: Order status details
        """
        try:
            logger.info(f"Fetching order status for Order ID {order_id}")
            
            order = self.client.futures_get_order(
                symbol=symbol,
                orderId=order_id
            )
            
            logger.info(f"Order status retrieved: {order['status']}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"API Exception in get_order_status: {e.status_code} - {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error in get_order_status: {str(e)}")
            raise
    
    def cancel_order(self, symbol, order_id):
        """
        Cancel an open order.
        
        Args:
            symbol (str): Trading pair
            order_id (int): Order ID to cancel
            
        Returns:
            dict: Cancellation details
        """
        try:
            logger.info(f"Cancelling Order ID {order_id} for {symbol}")
            
            result = self.client.futures_cancel_order(
                symbol=symbol,
                orderId=order_id
            )
            
            logger.info(f"Order cancelled successfully: Order ID {order_id}")
            return result
            
        except BinanceAPIException as e:
            logger.error(f"API Exception in cancel_order: {e.status_code} - {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error in cancel_order: {str(e)}")
            raise
    
    def get_current_price(self, symbol):
        """
        Get the current price of a symbol.
        
        Args:
            symbol (str): Trading pair
            
        Returns:
            float: Current price
        """
        try:
            logger.info(f"Fetching current price for {symbol}")
            
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            
            logger.info(f"Current price for {symbol}: {price}")
            return price
            
        except BinanceAPIException as e:
            logger.error(f"API Exception in get_current_price: {e.status_code} - {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error in get_current_price: {str(e)}")
            raise
