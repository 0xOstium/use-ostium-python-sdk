# Use Ostium Python SDK

This is a project that show cases how to use the Ostium Python SDK (https://github.com/0xOstium/ostium-python-sdk aka `ostium-python-sdk`, which is a python based SDK developed for interacting with Ostium v1 Trading Platform - https://ostium.app/ available on Arbitrum One Mainnet and Arbitrum Sepolia Testnet). Install the SDK itself via pip:
`pip install ostium-python-sdk`.


This project demonstrates how to use `ostium-python-sdk` to:

- Get list of all feeds to trade
- Get latest price of a feed
- Perform a trade (limit and market orders)
- Get list of open trades
- Update take profit and stop loss for an open trade
- Get trade metrics for an open trade aka: open PnL, Funding fee, Rollover fee, Percent profit, etc.
- Close a trade


## Prerequisites

- Python 3.10+

## Environment Variables

You will need an EVM private key and a RPC URL to use the SDK. By default the project is configured to use Sepolia Arbitrum so the below RPC_URL should be a Sepolia Arbitrum one


### Create a .env file

```bash
cp .envexample .env
```

### Edit the .env file

- `PRIVATE_KEY`: The private key of the account to use for the trades.
- `RPC_URL`: The RPC URL to use to access the blockchain. Can use either Sepolia Arbitrum or Arbitrum One Mainnet. Can
get it for free from Alchemy.

## Create a virtual environment and install the dependencies

```bash
python -m venv venv 
```

## Activate the virtual environment

```bash
source venv/bin/activate
```

## To install the dependencies

```bash
pip install -r requirements.txt
```

This will install the `ostium-python-sdk`.

## Run the project

```bash
python main.py
```

This will run the project and you will see the output in the terminal.

You might need to go to Ostium.app website, switch to Sepolia Testnet and get some testnet USDC tokens from the testnet faucet to be able to run this project for the first time.








