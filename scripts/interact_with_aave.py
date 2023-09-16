from brownie import config, network, interface
import scripts.helpful_scripts as helpful_scripts
from web3 import Web3


def main():
    amount = 100*(10**18)
    get_weth_tokens(amount)
    deposit_to_aave(amount)

def get_lending_pool():
    addresses_provider = get_pool_addresses_provider()
    _lending_pool = addresses_provider.getPool()
    lending_pool = interface.IPool(_lending_pool)
    print(f"lending pool: {lending_pool}")
    return lending_pool

def get_pool_addresses_provider():
    _addresses_provider = config["networks"][network.show_active()]["PoolAddressesProvider"]
    addresses_provider = interface.IPoolAddressesProvider(_addresses_provider)
    print(f"addresses provider: {addresses_provider}")
    return addresses_provider

def get_weth_contract():
    _weth_contract = config["networks"][network.show_active()]["WethToken"]
    weth_contract = interface.IWETH(_weth_contract)
    print(f"weth contract: {weth_contract}")
    return weth_contract

def get_weth_tokens(amount, account_i = 0):
    account = helpful_scripts.get_account(account_i)
    weth_contract = get_weth_contract()
    print_balances(account, weth_contract)
    tx = weth_contract.deposit({"from":account, "value":amount})
    tx.wait(1)
    print_balances(account, weth_contract)

def print_balances(account, token):
    eth_balance = Web3.fromWei(account.balance(), "ether")
    token_balance = Web3.fromWei(token.balanceOf(account), "ether")
    print(f"ETH balance: {eth_balance}")
    print(f"WETH balance: {token_balance}")

def approve(token, spender, amount, account):
    token.approve(spender, amount, {"from":account})

def get_pool_user_data(lending_pool, account):
    (
        collateral_eth,
        debt_eth,
        borrowable_eth,
        liquidation_treshold,
        ltv,
        helth_factor
    ) = lending_pool.getUserAccountData(account)
    #collateral_eth = Web3.fromWei(collateral_eth, "ether")
    print(f"collateral: {collateral_eth} worth of Eth")
    print(f"debt: {debt_eth/10**18} worth of Eth")
    print(f"borrowable {borrowable_eth/10**18} worth of Eth")

def deposit_to_aave(amount, account_i = 0):
    account = helpful_scripts.get_account(account_i)
    weth_contract = get_weth_contract()
    lending_pool = get_lending_pool()
    approve(weth_contract, lending_pool, amount, account)
    tx = lending_pool.supply(weth_contract, amount, account, 0, {"from":account})
    tx.wait(1)
    get_pool_user_data(lending_pool, account)
    print_balances(account, weth_contract)
    #pool_user_data = lending_pool.getUserAccountData(account)
    #print(f"pool user data: {pool_user_data}")


