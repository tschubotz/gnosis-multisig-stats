import requests
from web3 import Web3, HTTPProvider

from config.general import (
    ETHERSCAN_API_KEY, 
    INFURA_API_KEY, 
    GNOSIS_MULTISIG_FACTORY_ADDRESS, 
    GNOSIS_MULTISIG_FACTORY_ABI,
    GNOSIS_MULTISIG_FACTORY_CREATION_BLOCK,
    )
from config.multisig_addresses import KNOWN_FACTORY_MULTISIGS

def main():
    

    headers = {'content-type': 'application/json'}
    url_template = "https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=0x4fb057ad4a26ed17a57957fa69c306f11987596069b89521c511fc9a894e6161&apikey=%s"
    
    block_spans = [
        (GNOSIS_MULTISIG_FACTORY_CREATION_BLOCK, 5658995),
        (5658996, 6587076),
        (6587077, 'latest')
    ]

    unknown_factory_multisigs = []
    for start, end in block_spans:
        url = url_template % (start, end, GNOSIS_MULTISIG_FACTORY_ADDRESS, ETHERSCAN_API_KEY)
        response = requests.get(url, headers=headers).json()
        if len(response.get("result")) >= 1000:
            print("API limit reached, you might miss some multi sigs!")
        
        unknown_factory_multisigs.extend(process(response))

    if not len(unknown_factory_multisigs):
        print("No new factory MultiSigs found")
    else:
        print("Found the following new factory MultiSigs:")
        for address in unknown_factory_multisigs:
            print("    '%s'," % address)

def process(response):
    web3 = Web3(HTTPProvider('https://mainnet.infura.io/' + INFURA_API_KEY))

    # Check if there are new ones
    unknown_factory_multisigs = []
    for result in response.get("result"):
        address = "0x%s" % (result["data"][90:])
        address = web3.toChecksumAddress(address)
        if address not in KNOWN_FACTORY_MULTISIGS:
            unknown_factory_multisigs.append(address)
    return unknown_factory_multisigs

if __name__ == '__main__':
    main()
