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
from bit import PrivateKeyTestnet

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
    ETH: derive_wallets(ETH),
    BTCTEST: derive_wallets(BTCTEST),
    }
print(coins)
print()


# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin):
    if coin == ETH:
        return Account.privateKeyToAccount(coins[coin][0]['privkey'])
    if coin == BTCTEST:
        return PrivateKeyTestnet(coins[coin][0]['privkey'])
print(priv_key_to_account(ETH))
print()
print(priv_key_to_account(BTCTEST))
print()


# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to, amount):
    if coin == ETH:
        # Convert ETH to WEI
        value = w3.toWei(amount, coin)
        gasEstimate = w3.eth.estimateGas({'from': account, 'to': to, 'amount': value})
        return {
            'from': account,
            'to': to,
            'value': value,
            'gasPrice': w3.eth.gasPrice,
            'gas': gasEstimate,
            'nonce': w3.eth.getTransactionCount(account),
            'chainID': w3.eth.chain_id
        }
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])


# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, recipient, amount):
    if coin == ETH:
        tx = create_tx(coin, account.address, to, amount)
        signed_tx = account.signTransaction(tx)
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    if coin == BTCTEST:
        tx = create_tx(coin, account.address, to, amount)
        signed_tx = account.sign_transaction(tx)
        return NetworkAPI.broadcast_tx_testnet(signed)



