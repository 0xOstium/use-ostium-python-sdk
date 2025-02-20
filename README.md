# Use Ostium Python SDK

This is a project to show how to use the Ostium Python SDK.

## Prerequisites

- Python 3.10+

## Environment Variables

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

## Run the project

```bash
python main.py
```







