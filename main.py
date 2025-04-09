import random
from ostium_python_sdk import OstiumSDK
from ostium_python_sdk.config import NetworkConfig
from ostium_python_sdk.utils import get_order_details
import asyncio
from dotenv import load_dotenv
from eth_account import Account
import os

# Load environment variables from .env file
load_dotenv()


async def main():
    # Get private key from environment variable
    private_key = os.getenv('PRIVATE_KEY')
    # if not private_key:
    #     raise ValueError("PRIVATE_KEY not found in .env file")

    rpc_url = os.getenv('RPC_URL')
    if not rpc_url:
        raise ValueError("RPC_URL not found in .env file")

    # Initialize SDK
    config = NetworkConfig.testnet()
    sdk = OstiumSDK(config, private_key)

    pairs = await sdk.subgraph.get_pairs()

    print("\nPair Information:")
    print("----------------------------------------")

    for pair in pairs:
        # Get detailed information for each pair from the Graph API
        pair_details = await sdk.subgraph.get_pair_details(pair['id'])
        print("\nPair Details:")
        print("----------------------------------------")
        # Print all available fields in pair_details
        for key, value in pair_details.items():
            print(f"{key}: {value}")
        print("----------------------------------------")
        
    # Will choose a random asset and place a order on it
    random_asset = random.choice(pairs)

    
    # Define trade parameters
    order_params = {
        'collateral': 20,         # USDC amount
        'leverage': 50,           # Leverage multiplier
        'asset_type': random_asset['id'],         
        'direction': False,       # True for Long, False for Short
        'order_type': 'LIMIT'     # 'MARKET', 'LIMIT', or 'STOP'
    }

    print(f"Random asset for {order_params['order_type']} order: {random_asset}")

    try:
        sdk.ostium.set_slippage_percentage(1)
        print(f"Slippage percentage set to: {sdk.ostium.get_slippage_percentage()}%")

        # Get latest price for ETH
        latest_price, _ = await sdk.price.get_price(random_asset['from'], random_asset['to'])
        
        print(f"Latest price for {random_asset['from']} to {random_asset['to']}: {latest_price} {random_asset['to']}")
        # Execute trade at current market price
        receipt = sdk.ostium.perform_trade(order_params, at_price=latest_price * 1.1)
        print(
            f"Order successful! Transaction hash: {receipt['transactionHash'].hex()}")

        # Wait for the transaction to be confirmed
        await asyncio.sleep(10)

        # Get public address from private key
        account = Account.from_key(private_key)
        trader_public_address = account.address

        # Get the trade details
        open_orders = await sdk.subgraph.get_orders(trader_public_address)
        for order_index, order_data in enumerate(open_orders):
            print(f"Order {order_index + 1}: {order_data}\n")
            limit_type, _, _, _, _, _, _, pairIndex, index, _, _ = get_order_details(order_data)
            print(f"You can cancel_limit_order / update_limit_order using pair_id: {pairIndex} and index: {index}\n")
            receipt = sdk.ostium.cancel_limit_order(pairIndex, index)
            print(
            f"Limit Order cancelled! Transaction hash: {receipt['transactionHash'].hex()}")

        if len(open_orders) == 0:
            print(
                "No open order found. Maybe the order failed? enough USDC and ETH in the account?")
        else:
            opened_order = open_orders[len(open_orders) - 1]
            print(f"Opened order: {opened_order}\n")

    except Exception as e:
        print(f"Order failed: {str(e)}")

    #
    # Now do something Write
    #
    random_asset = random.choice(pairs)

    # Define trade parameters
    trade_params = {
        'collateral': 100,        # USDC amount
        'leverage': 10,           # Leverage multiplier
        'asset_type': 0,          # 0 for BTC, see pair_details above for other asset types 
        'direction': True,        # True for Long, False for Short
        'order_type': 'MARKET'    # 'MARKET', 'LIMIT', or 'STOP'
    }

    print(f"Random asset for {trade_params['order_type']} trade: {random_asset}")

    try:
        sdk.ostium.set_slippage_percentage(1)
        print(f"Slippage percentage set to: {sdk.ostium.get_slippage_percentage()}%")

        # Get latest price for BTC
        latest_price, _ = await sdk.price.get_price(random_asset['from'], random_asset['to'])
        print(f"Latest price: {latest_price}")
        # Execute trade at current market price
        receipt = sdk.ostium.perform_trade(trade_params, at_price=latest_price)
        print(f"Trade successful! Transaction hash: {receipt['transactionHash'].hex()}")

        # Wait for the transaction to be confirmed
        await asyncio.sleep(10)

        # Get public address from private key
        account = Account.from_key(private_key)
        trader_public_address = account.address

        # Get the open trades details
        open_trades = await sdk.subgraph.get_open_trades(trader_public_address)
        for trade_index, trade_data in enumerate(open_trades):
            print(f"Open Trade {trade_index + 1}/{len(open_trades)}: {trade_data}\n")

        if len(open_trades) == 0:
            print(
                "No open trades found. Maybe the trade failed? enough USDC and ETH in the account?")
        else:
            newly_opened_trade = open_trades[len(open_trades) - 1]

            if (newly_opened_trade):
                print(f"The Opened trade is: {newly_opened_trade}\n")
                sdk.ostium.update_tp(
                newly_opened_trade['pair']['id'], newly_opened_trade['index'], latest_price * 1.05)

                print(f"Trade Take Profit set to 5% above the current price (aka: {latest_price * 1.05})!\n")

                await asyncio.sleep(10)

                sdk.ostium.update_sl(
                    newly_opened_trade['pair']['id'], newly_opened_trade['index'], latest_price * 0.95)
                print(f"Trade Stop Loss set to 5% below the current price (aka: {latest_price * 0.95})!\n")

                await asyncio.sleep(10)
            else:
                print(f"The Opened trade was not located!\n")

            if (len(open_trades) > 0):
                print("Monitoring trades metrics for the next 10 minutes of all the opened trades...")
                # Monitor trade metrics for 10 minutes
                for iteration in range(10):
                    try:
                        for trade_index, trade_data in enumerate(open_trades):
                            trade_metrics = await sdk.get_open_trade_metrics(
                                newly_opened_trade['pair']['id'], 
                                newly_opened_trade['index']
                            )
                            print(f"Open Trade {trade_index+1}/{len(open_trades)} Metrics: {trade_metrics}\n")

                        print(f"\nIteration {iteration + 1}/10 - Trade Metrics:")
                        print("----------------------------------------")
                        for key, value in trade_metrics.items():
                            print(f"{key}: {value}")
                        print("----------------------------------------")
                        
                        # Wait for 60 seconds before next iteration
                        if iteration < 9:  # Don't wait after the last iteration
                            print(f"Waiting for 1 minute before next iteration...")
                            await asyncio.sleep(60)
                            
                    except Exception as e:
                        print(f"Failed to get trade metrics: {str(e)}")
            #
            if (newly_opened_trade):
                print("Closing trade...")
                receipt = sdk.ostium.close_trade(
                    newly_opened_trade['pair']['id'], newly_opened_trade['index'])
                print(
                    f"Closed trade! Transaction hash: {receipt['transactionHash'].hex()}\n")
                

    except Exception as e:
        print(f"Trade failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
