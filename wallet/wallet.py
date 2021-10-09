# Import dependencies
import subprocess
import json
import os
import pprint
from dotenv import load_dotenv

# Load and set environment variables
load_dotenv('token.env')
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
from constants import *
from bit import wif_to_key

from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account

 
# Create a function called `derive_wallets`
def derive_wallets(coin, stdout=subprocess.PIPE, shell=True):
    command = f'php ./derive -g --mnemonic=mnemonic --coin={coin} --numderive=3 --cols=address,index,path,privkey,pubkey,pubkeyhash,xprv,xpub --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {
    'btc-test': derive_wallets(BTCTEST),
    'eth': derive_wallets(ETH),
    }

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
# def priv_key_to_account(# YOUR CODE HERE):
    # YOUR CODE HERE

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
# def create_tx(account, recipient, amount):
    # gasEstimate = w3.eth.estimateGas(
    #     {'from': account.address, 'to': recipient, 'value': amount}
    # )
    # return {
    #     'from': account.address,
    #     'to': recipient,
    #     'value': amount,
    #     'gasPrice': w3.eth.gasPrice,
    #     'gas': gasEstimate,
    #     'nonce': w3.eth.getTransactionCount(account.address),
    # }


# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
# def send_tx(# YOUR CODE HERE):
    # YOUR CODE HERE
