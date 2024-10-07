from nada_dsl import *

def nada_main():
    party_user = Party(name="User")
    
    party_sync_recipient = Party(name="SyncRecipient")

    secret_user = SecretInteger(Input(name="secret_user", party=party_user))
    
    secret_sync_user = SecretInteger(Input(name="secret_sync_recipient", party=party_sync_recipient))
    
    is_same_num = secret_user == secret_sync_user
    
    return [Output(is_same_num, "is_same_user", party_user)]