import asyncio
import py_nillion_client as nillion
import os
import pytest

from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey
import hashlib
from nillion_python_helpers import get_quote_and_pay, create_nillion_client, create_payments_config

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")


CONFIG_PROGRAM_NAME="SyncNotify"

def hashify_string(name: str):
    hash_object = hashlib.sha256(name.encode())
    hash_value = hash_object.hexdigest()

    # Convert the hexadecimal hash to an integer
    hash_int = int(hash_value[:14], 16)
    
    return hash_int

async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    
    sync_seed = "sync_seed123"
    
    sync_client = create_nillion_client(
        UserKey.from_seed(sync_seed), NodeKey.from_seed(sync_seed)
    )
    user_id_1 = sync_client.user_id
    program_mir_path = f"/{compute}.nada.bin"

    # Create payments config and set up Nillion wallet with a private key to pay for operations
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )
    
    # Get cost quote, then pay for operation to store program
    receipt_store_program = await get_quote_and_pay(
        sync_client,
        nillion.Operation.store_program(program_mir_path),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # Sync Initiates Notification
    action_id = await sync_client.store_program(
        cluster_id, CONFIG_PROGRAM_NAME, program_mir_path, receipt_store_program
    )

    program_id = f"{user_id_1}/{CONFIG_PROGRAM_NAME}"
    print("Stored program. action_id:", action_id)
    print("Stored program_id:", program_id)


    # Demo User Initialization
    demo_user_seed = "fayaz_seed123"
    client_n = create_nillion_client(
        UserKey.from_seed(demo_user_seed), NodeKey.from_seed(demo_user_seed)
    )
    party_id_n = client_n.party_id
    user_id_n = client_n.user_id
    
    party_name = "User"
    secret_name = "fayaz.sync"
    
    
    # Sync stores notification payload
    
    permissions = nillion.Permissions.default_for_user(sync_client.user_id)
    permissions.add_compute_permissions({sync_client.user_id: {program_id}})
    
    stored_secret_1 = nillion.NadaValues(
        {
            "secret_sync_recipient": nillion.SecretInteger(hashify_string("fayaz.sync")),
            "encryptedMessage": nillion.SecretBlob(bytearray("Hello BRO!", "utf-8"))
        }
    )
    receipt_store = await get_quote_and_pay(
        sync_client,
        nillion.Operation.store_values(stored_secret_1, ttl_days=5),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    store_id_1 = await sync_client.store_values(
        cluster_id, stored_secret_1, permissions, receipt_store
    )
    
    

    # Demo User stores info in program

    stored_secret = nillion.NadaValues(
        {
            "secret_user": nillion.SecretInteger(hashify_string(secret_name)),             
            "phno": nillion.SecretBlob(bytearray("+9188888888", "utf-8"))
        }
    )

    receipt_store = await get_quote_and_pay(
        client_n,
        nillion.Operation.store_values(stored_secret, ttl_days=5),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    user_permissions = nillion.Permissions.default_for_user(user_id_n)
    
    # Give compute permissions to the Sync
    
    compute_permissions = {
        sync_client.user_id: {program_id},
    }
    user_permissions.add_compute_permissions(compute_permissions)

    # Store the permissioned payload
    store_id_n = await client_n.store_values(
        cluster_id, stored_secret, user_permissions, receipt_store
    )
    
    
    # Bind the parties in the computation to the client to set inputs and output parties
    compute_bindings = nillion.ProgramBindings(program_id)
    compute_bindings.add_input_party("SyncRecipient", sync_client.party_id)
    compute_bindings.add_output_party("SyncRecipient", sync_client.party_id)

    compute_bindings.add_input_party("User", party_id_n)

    compute_time_secrets = nillion.NadaValues({})

    receipt_compute = await get_quote_and_pay(
        sync_client,
        nillion.Operation.compute(program_id, compute_time_secrets),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    compute_id = await sync_client.compute(
        cluster_id,
        compute_bindings,
        [store_id_1, store_id_n],
        compute_time_secrets,
        receipt_compute,
    )

    # Print compute result
    print(f"The computation was sent to the network. compute_id: {compute_id}")
    while True:
        compute_event = await sync_client.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):

            if compute_event.result.value["is_same_user"]:

                # Give notification payload access permission to demo user
                
                new_permissions = nillion.Permissions.default_for_user(sync_client.user_id)
                new_permissions.add_retrieve_permissions(set([user_id_n, sync_client.user_id]))

                receipt_update_permissions = await get_quote_and_pay(
                    sync_client,
                    nillion.Operation.update_permissions(),
                    payments_wallet,
                    payments_client,
                    cluster_id,
                )
                
                await sync_client.update_permissions(
                    cluster_id, store_id_1, new_permissions, receipt_update_permissions
                )
                
            # Now demo user can access it
            
            receipt_retrieve = await get_quote_and_pay(
                client_n,
                nillion.Operation.retrieve_value(),
                payments_wallet,
                payments_client,
                cluster_id,
            )

            result_tuple = await client_n.retrieve_value(
                cluster_id, store_id_1, "encryptedMessage", receipt_retrieve
            )
            
            print(f"The encrypted message is {result_tuple[1].value}")
            
            return compute_event.result.value
    
    
if __name__ == "__main__":
    asyncio.run(main())

