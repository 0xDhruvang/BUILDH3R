from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)

# Client to connect to localnet
algorand = AlgorandClient.default_local_net()

# Import dispenser from KMD 
dispenser = algorand.account.dispenser()
print("Dispenser Address: ", dispenser.address)

# Create a wallet for the creator of the token
creator = algorand.account.random()
print("Creator Address: ", creator.address)

# Fund creator address with Algo
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)

# Check the creator account changes after funding
print("Creator Account Info: ", algorand.account.get_information(creator.address))

# Create Algorand Standard Asset
sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=1000,
        asset_name="MyToken",
        unit_name="MTK",
        manager=creator.address,
        clawback=creator.address,
        freeze=creator.address
    )
)

# Extract the asset ID
asset_id = sent_txn["confirmation"]["asset-index"]
print("Asset ID: ", asset_id)

# Create three receiver accounts
receiver_accounts = [algorand.account.random() for _ in range(3)]
for i, receiver in enumerate(receiver_accounts):
    print(f"Receiver {i+1} Account: {receiver.address}")

# Fund and opt-in each receiver account to the ASA
for i, receiver in enumerate(receiver_accounts):
    # Fund receiver account
    algorand.send.payment(
        PayParams(
            sender=dispenser.address,
            receiver=receiver.address,
            amount=10_000_000
        )
    )
    print(f"Receiver {i+1} Account Info after funding: ", algorand.account.get_information(receiver.address))
    
    # Opt-in receiver account to the ASA
    algorand.send.asset_opt_in(
        AssetOptInParams(
            sender=receiver.address,
            asset_id=asset_id
        )
    )
    print(f"Receiver {i+1} Account Info after opt-in: ", algorand.account.get_information(receiver.address))

# Transfer the ASA to each receiver account
for i, receiver in enumerate(receiver_accounts):
    algorand.send.asset_transfer(
        AssetTransferParams(
            sender=creator.address,
            receiver=receiver.address,
            asset_id=asset_id,
            amount=10
        )
    )
    print(f"Receiver {i+1} Account Info after asset transfer: ", algorand.account.get_information(receiver.address))

# Print the entire information from all Receiver Accounts
for i, receiver in enumerate(receiver_accounts):
    print(f"Receiver {i+1} Final Account Info: ", algorand.account.get_information(receiver.address))

