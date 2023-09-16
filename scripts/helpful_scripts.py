from brownie import accounts, network, config

LOCAL_NETWORKS = ["mainnet-fork-dev", "development"]

def get_account(i = 0):
    if network.show_active() in LOCAL_NETWORKS:
        return accounts[i]
    else:
        return accounts.add(config["wallets"]["account_" + str(i)])
    