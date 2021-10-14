# Import dependencies
import subprocess
import json
import os
import pprint
from dotenv import load_dotenv

# Load and set environment variables
load_dotenv('token.env')
mnemonic = os.getenv('mnemonic')

# Import constants.py and necessary functions from bit and web3
from constants import *
from bit import wif_to_key
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from getpass import getpass

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


# "Chatter" function from Project 1 that prints lines one character at a time
import time
import sys
from random import randrange
from chatter import chatter
chatter('Testing chatter function..')
chatter('.........')
chatter('Testing complete.')
chatter('------------')

# Toggle chatter
chatter('Would you like to disable chatter function for faster text?')
chatter_io = input('Disable chatter function? (y/n): ')
if chatter_io.lower() == 'y':
    def chatter(npc_chatter):
        print(npc_chatter)
    chatter('Chatter is disabled.')
else:
    from chatter import chatter
    chatter('Chatter is enabled.')


# Create a function called `derive_wallets`
def derive_wallets(coin, stdout=subprocess.PIPE, shell=True):
    chatter(f'Enter mnemonic for {coin}. Leave blank to use test wallet.')
    user = input('Enter mnemonic without quotes: ')
    if user == '':
        chatter(f'No mnemonic specified. Accessing test {coin} wallet..')
        phrase = f'"{mnemonic}"'
        # print(phrase)
    else:
        chatter('Checking for user\'s {coin} wallet..')
        phrase = f'"{user}"'
        # print(phrase)
    
    command = f'php ./derive -g --mnemonic={phrase} --coin={coin} --numderive=2 --cols=address,index,path,privkey,pubkey --format=json'    
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    # wallet = return json.loads(output)
    # return wallet
    
    # Create global variables for the wallets
    if coin == ETH:
        global eth_wallet
        eth_wallet = json.loads(output)
        return json.loads(output)
    elif coin == BTCTEST:
        global btctest_wallet
        btctest_wallet = json.loads(output)
        return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {
    ETH: derive_wallets(ETH),
    BTCTEST: derive_wallets(BTCTEST),
    }
print()


# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)


# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to, amount):
    chatter(f'Creating unsigned {coin} transaction..')
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {'from': account.address, 'to': to, 'value': amount}
        )
        return {
            'from': account.address,
            'to': to,
            'value': amount,
            'gasPrice': w3.eth.gasPrice,
            'gas': gasEstimate,
            'nonce': w3.eth.getTransactionCount(account.address),
        }
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])


# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to, amount):
    if coin == ETH:
        raw_tx = create_tx(coin, account, to, amount)
        chatter('Unsigned transaction created.')
        chatter('Sending transaction..')
        signed_tx = account.sign_transaction(raw_tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        chatter('Transaction sent.')
        return result.hex()
    elif coin == BTCTEST:
        raw_tx = create_tx(coin, account, to, amount)
        chatter('Unsigned transaction created.')
        chatter('Sending transaction..')
        signed_tx = account.sign_transaction(raw_tx)
        chatter('Transaction sent.')
        return NetworkAPI.broadcast_tx_testnet(signed_tx)


# Create wallet variables
eth_account = priv_key_to_account(ETH, eth_privkey)
eth_address = coins[ETH][0]['address']
eth_privkey = coins[ETH][0]['privkey']
eth_receiver = '0x26077A0eaA11E133739F070b001D28267264D24A'
btctest_account = priv_key_to_account(BTCTEST, btctest_privkey)
btctest_address = coins[BTCTEST][0]['address']
btctest_privkey = coins[BTCTEST][0]['privkey']
btctest_receiver = 'mnLfB25RMps3ABSqK6orbwQDQdMhC1FvS2'



# # ETH Transaction
# chatter(f'# Commands to send a transaction using ETH:')
# chatter(f'priv_key_to_account(ETH, eth_privkey)')
# chatter(f'send_tx(ETH, eth_account, eth_receiver, 0.000001)')

# # BTC Transaction
# chatter(f'# Commands to send a transaction using BTCTEST:')
# chatter(f'priv_key_to_account(BTCTEST, btctest_privkey)')
# chatter(f'send_tx(BTCTEST, btctest_account, btctest_receiver, 0.000001)')

# # Get transaction history
# chatter(f'# Command to get BTCTEST transaction history:')
# chatter(f'btctest_account.get_transactions()')

# # Get balance
# chatter(f'# Command to get BTCTEST account balance:')
# chatter(f'btctest_account.get_balance("btc")')

