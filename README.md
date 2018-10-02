# gnosis-multisig-stats
Pulling some statistics about deployed Gnosis MultiSig contracts from the blockchain. 
Currently only balances for ETH and top tokens are pulled.

## 0: Prerequisites

- Install dependecies: `pip install -r requirements.txt` 
- Add Etherscan and Infure API keys to `config/general.py`

## 1: Check for new deployed MultiSigs
- Execute script: `python check_for_new_factory_multisigs.py`
- Add any new ones to `config/multisig_addresses.py`

## 2: Fetch stats
- Execute script: `python gnosis_multisig_stats.py`

## Optional: Fetch exchange rates for top tokens
- Check pricefeed from CryptoCompare: `python get_exchange_rates.py`