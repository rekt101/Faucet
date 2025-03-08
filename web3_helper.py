from web3_helper import Web3

w3 = Web3()
private_key = "a5a5412f6e045c93c67917ed9bd0c7e0555008d45c5c2257e2e59aa88bd8b70"
account = w3.eth.account.from_key(private_key)
print(f"Derived Address: {account.address}")