# Binance Futures Testnet Trading Bot

A simplified Python trading bot for Binance Futures Testnet (USDT-M) with support for market, limit, and stop-limit orders.

## Features

- ✅ Market Orders (BUY/SELL)
- ✅ Limit Orders (BUY/SELL)
- ✅ Stop-Limit Orders (BUY/SELL) - Advanced order type
- ✅ Interactive CLI interface with input validation
- ✅ Real-time account information and balances
- ✅ Order status tracking and cancellation
- ✅ Comprehensive logging (file-based)
- ✅ Error handling for API requests
- ✅ Binance Futures Testnet support

## Requirements

- Python 3.7 or higher
- Binance Futures Testnet account
- API credentials (API Key and Secret)

## Installation

1. **Clone or download this repository**

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API credentials**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Binance Testnet API credentials:
   ```
   BINANCE_API_KEY=your_testnet_api_key_here
   BINANCE_API_SECRET=your_testnet_api_secret_here
   ```

## Getting Binance Testnet API Credentials

1. **Register for Binance Futures Testnet**
   - Visit: https://testnet.binancefuture.com
   - Click on "Register" or log in with your GitHub/Google account
   - Note: This is completely separate from production Binance

2. **Generate API Credentials**
   - After logging in, go to your account settings
   - Navigate to "API Key" section
   - Click "Generate HMAC_SHA256 Key"
   - Save your API Key and Secret Key securely
   - **Important**: The Secret Key is only shown once!

3. **Get Free Testnet USDT**
   - The testnet provides free test USDT for trading
   - Your account will have a default balance for testing

## Usage

1. **Activate the virtual environment** (if not already activated):
   ```bash
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate      # Windows
   ```

2. **Run the trading bot**:
   ```bash
   python main.py
   ```

3. **Deactivate virtual environment** (when done):
   ```bash
   deactivate
   ```

### Main Menu Options

```
1. View Account Information    - Check balances and open positions
2. Check Current Price         - Get real-time price for any symbol
3. Place Market Order          - Execute immediate buy/sell at market price
4. Place Limit Order           - Set buy/sell order at specific price
5. Place Stop-Limit Order      - Set trigger price and limit price
6. Check Order Status          - View details of a specific order
7. Cancel Order                - Cancel an open order
8. Exit                        - Close the application
```

### Example Usage

#### Market Order
```
Enter symbol: BTCUSDT
Enter side: BUY
Enter quantity: 0.001
```

#### Limit Order
```
Enter symbol: ETHUSDT
Enter side: SELL
Enter quantity: 0.01
Enter limit price: 2000
```

#### Stop-Limit Order
```
Enter symbol: BTCUSDT
Enter side: SELL
Enter quantity: 0.001
Enter stop price: 40000    (trigger price)
Enter limit price: 39900   (execution price after trigger)
```

## Project Structure

```
cryptotrade/
├── bot.py              # BasicBot class with order methods
├── main.py             # CLI interface and user interaction
├── config.py           # Configuration and settings
├── requirements.txt    # Python dependencies
├── .env.example        # Template for API credentials
├── .env               # Your actual API credentials (gitignored)
├── logs/
│   └── trading_bot.log # All API requests, responses, and errors
└── README.md          # This file
```

## Logging

All API requests, responses, and errors are logged to `logs/trading_bot.log`. 

The log includes:
- Bot initialization events
- All API requests with parameters
- API responses and order details
- Error messages with full stack traces
- Order execution status

Check the log file for detailed debugging information.

## Order Types Explained

### Market Order
- Executes immediately at the best available market price
- No price needs to be specified
- Use when you want instant execution

### Limit Order
- Executes only at your specified price or better
- Order sits in the order book until filled or cancelled
- Use when you want price control

### Stop-Limit Order (Advanced)
- Two prices: Stop Price (trigger) and Limit Price (execution)
- When market reaches stop price, a limit order is placed
- Use for stop-loss or take-profit strategies
- Example: Buy BTC if price goes above $45,000 (stop) but not more than $45,500 (limit)

## API Configuration

The bot uses:
- **Testnet Base URL**: https://testnet.binancefuture.com
- **Market**: USDT-M Futures
- **Time in Force**: GTC (Good Till Cancel) by default

## Error Handling

The bot handles:
- Invalid API credentials
- Network errors
- Invalid order parameters
- Insufficient balance
- API rate limits
- Order execution failures

All errors are logged and displayed to the user with helpful messages.

## Safety Features

- ✅ Input validation for all user entries
- ✅ Order confirmation before execution
- ✅ Current price display before placing orders
- ✅ Testnet-only operation (no real funds at risk)
- ✅ Comprehensive error handling
- ✅ Detailed logging for audit trail

## Troubleshooting

### "API credentials not found"
- Ensure you've created `.env` file from `.env.example`
- Check that your API key and secret are correctly added to `.env`

### "Import binance.client could not be resolved"
- Install dependencies: `pip install -r requirements.txt`

### "API Error 403" or "Invalid API Key"
- Verify your API credentials are correct
- Ensure you're using Testnet credentials (not production)
- Regenerate API keys if necessary

### Orders not executing
- Check your testnet account balance
- Verify the symbol is correct (e.g., BTCUSDT, not BTC)
- Review the log file for detailed error messages

## Important Notes

⚠️ **This bot is for Binance FUTURES TESTNET only**
- No real money is involved
- All trades are simulated with test funds
- Perfect for learning and testing strategies

⚠️ **Never commit your `.env` file**
- Keep your API credentials secure
- The `.env` file is gitignored by default

⚠️ **Rate Limits**
- Be mindful of API rate limits
- The bot includes logging to help track usage

## Support

For issues related to:
- **Binance API**: https://binance-docs.github.io/apidocs/futures/en/
- **Testnet Access**: https://testnet.binancefuture.com
- **Python-Binance Library**: https://python-binance.readthedocs.io/

## License

This project is for educational purposes.
