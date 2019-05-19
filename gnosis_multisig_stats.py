import json
import requests
import sys
from multiprocessing import Pool

from config.general import (
    NUM_PROCESSES,
    ETHERSCAN_API_KEY, 
    INFURA_API_KEY, 
    ERC20_ABI,
    GNOSIS_MULTISIG_FACTORY_ADDRESS, 
    GNOSIS_MULTISIG_FACTORY_ABI,
    )
from config.multisig_addresses import KNOWN_NON_FACTORY_MULTISIGS, KNOWN_FACTORY_MULTISIGS
from config.tokens import TOKENS, TOP_TOKENS

from web3.exceptions import BadFunctionCallOutput
from web3 import Web3, HTTPProvider

def get_info_for_address(address, web3=None):
    if not web3:
        web3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/' + INFURA_API_KEY))

    eth_balance = Web3.fromWei(web3.eth.getBalance(address), 'ether')

    output = [address, not web3.toChecksumAddress(address) in KNOWN_NON_FACTORY_MULTISIGS, eth_balance]

    for token in TOKENS:
        if token['symbol'] not in TOP_TOKENS:
            continue
        contract = web3.eth.contract(address=web3.toChecksumAddress(token['address']), abi=ERC20_ABI)
        try:
            balance = contract.functions.balanceOf(address).call() / (10**token['decimals'])
        except BadFunctionCallOutput:
            balance = 0
        output.append(balance)

    print(','.join(str(item) for item in output))
    sys.stdout.flush()

    return

def main():
    web3 = Web3(HTTPProvider('https://mainnet.infura.io/' + INFURA_API_KEY))

    multisigs = []
    for multisig in KNOWN_FACTORY_MULTISIGS:
        multisigs.append(web3.toChecksumAddress(multisig))
    for multisig in KNOWN_NON_FACTORY_MULTISIGS:
        multisigs.append(web3.toChecksumAddress(multisig))

    column_names = ['multisig address', 'created_via_factory', 'ETH']
    for token in TOKENS:
        if token['symbol'] not in TOP_TOKENS:
            continue
        column_names.append('%s (%s)' % (token['symbol'], token['name']))

    print(','.join(column_names))
    # get_info_for_address(multisigs[0])
    with Pool(processes=NUM_PROCESSES) as pool:
        pool.map(get_info_for_address, multisigs)

if __name__ == '__main__':
    main()
