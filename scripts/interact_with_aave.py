from brownie import config, network, interface
import scripts.helpful_scripts as helpful_scripts
from web3 import Web3


def main():
    amount = 100*(10**18)
    account = helpful_scripts.get_account()
    price_of_eth()
    #weth_contract = get_weth_contract()
    get_weth_tokens(amount)
    deposit_to_aave(amount)
    _dai_eth_price_feed = config["networks"][network.show_active()]["DaiEth"]
    _dai = config["networks"][network.show_active()]["Dai"]
    dai = get_ERC20(_dai)
    print(amount * 0.1 * get_asset_price(_dai_eth_price_feed))
    borrow(dai, amount * 0.1 * get_asset_price(_dai_eth_price_feed))


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

def get_weth_tokens(amount, account = None):
    account = account if account else helpful_scripts.get_account()
    weth_contract = get_weth_contract()
    print_balances(weth_contract)
    tx = weth_contract.deposit({"from":account, "value":amount})
    tx.wait(1)
    print_balances(weth_contract)

def print_balances(token, account = None):
    account = account if account else helpful_scripts.get_account()
    eth_balance = Web3.fromWei(account.balance(), "ether")
    token_balance = Web3.fromWei(token.balanceOf(account), "ether")
    print(f"ETH balance: {eth_balance}")
    print(f"token balance: {token_balance}")

def approve(token, spender, amount, account = None):
    account = account if account else helpful_scripts.get_account()
    token.approve(spender, amount, {"from":account})

def get_pool_user_data(lending_pool, account = None):
    account = account if account else helpful_scripts.get_account()
    (
        collateral_usd,
        debt_usd,
        borrowable_usd,
        liquidation_treshold,
        ltv,
        helth_factor
    ) = lending_pool.getUserAccountData(account)
    print(f"collateral: {collateral_usd} worth of Usd")
    print(f"debt: {debt_usd} worth of Usd")
    print(f"borrowable {borrowable_usd} worth of Usd")
    #collateral_eth = Web3.fromWei(collateral_eth, "ether")
    # print(f"collateral: {collateral_eth} worth of Eth")
    # print(f"debt: {debt_eth/10**18} worth of Eth")
    # print(f"borrowable {borrowable_eth/10**18} worth of Eth")
    return collateral_usd, debt_usd, borrowable_usd

def deposit_to_aave(amount, account = None):
    account = account if account else helpful_scripts.get_account()
    weth_contract = get_weth_contract()
    lending_pool = get_lending_pool()
    approve(weth_contract, lending_pool, amount, account)
    tx = lending_pool.supply(weth_contract, amount, account, 0, {"from":account})
    tx.wait(1)
    print_balances(weth_contract)
    convert_pool_user_data_to_eth_and_print()
    #pool_user_data = lending_pool.getUserAccountData(account)
    #print(f"pool user data: {pool_user_data}")

def get_asset_price(price_feed_address):
    price_feed = interface.AggregatorV3Interface(price_feed_address)
    price = price_feed.latestRoundData()[1]
    print(f"price: {price}")
    return price

def price_of_eth():
    _dai_eth_price_feed = config["networks"][network.show_active()]["DaiEth"]
    price = get_asset_price(_dai_eth_price_feed)
    price_of_eth = (1 / price) * 10 ** 18
    print(print(f"price of eth: {price_of_eth}"))
    return price_of_eth

def convert_pool_user_data_to_eth_and_print(account = None):
    account = account if account else helpful_scripts.get_account()
    lending_pool = get_lending_pool()
    _dai_eth_price_feed = config["networks"][network.show_active()]["DaiEth"]
    price_of_eth = (1/get_asset_price(_dai_eth_price_feed)) *10**18
    print(f"price of eth: {price_of_eth}")
    collateral_usd, debt_usd, borrowable_usd = get_pool_user_data(lending_pool, account)
    collateral_eth = collateral_usd / (price_of_eth*10**8)
    debt_eth = debt_usd / (price_of_eth*10**8)
    borrowable_eth = borrowable_usd / (price_of_eth*10**8)
    print(f"collateral: {collateral_eth} worth of Eth")
    print(f"debt: {debt_eth} worth of Eth")
    print(f"borrowable {borrowable_eth} worth of Eth")
    return collateral_eth, debt_eth, borrowable_eth

def get_ERC20(token_address):
    token_contract = interface.IERC20(token_address)
    return token_contract

# def get_Dai_contract():
#     dai_address = config["networks"][network.show_active()]["Dai"]
#     dai_contract = get_ERC20(dai_address)
#     return dai_contract

def borrow(asset, amount, interestMode = 2, refferal = 0, onBehalfOf = None, account = None):
    account = account if account else helpful_scripts.get_account()
    onBehalfOf = onBehalfOf if onBehalfOf else account
    lending_pool = get_lending_pool()
    print_balances(asset)
    tx = lending_pool.borrow(asset, amount, interestMode, refferal, onBehalfOf, {"from":account})
    tx.wait(1)
    print_balances(asset)
    convert_pool_user_data_to_eth_and_print()





