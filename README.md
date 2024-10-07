# Nillion Integration README

## Overview

This repository showcases a secure communication protocol using Nillion's multi-party computation, focusing on data exchange between two parties: Sync (Initiator) and User (Responder).

The protocol leverages SyncIDs and Nillion's infrastructure to handle sensitive information securely, ensuring that decryption occurs only on the User's local device.

## Key Components

- **Sync (Initiator):** Starts the program and stores encrypted messages.
- **User (Responder):** Creates a SyncID, inputs sensitive data, and securely interacts with Sync.
- **Delivery Node:** The User's local device that decrypts messages using its private key.

## Process Flow

1. **SyncID Creation:** User creates a SyncID, inputs their phone number, which is stored locally.
2. **Program Initialization:** Sync initiates the program and invites the User to accept.
3. **User Input:** User shares their SyncID and hashed secret identifier.
4. **Secure Computation:** The logic matches the hashed identifiers from Sync and the User.
   - If they match, the encrypted message is revealed to the delivery node.
5. **Decryption:** User’s device decrypts the message locally and sends it via WhatsApp or Telegram.

## Usage

Run the following commands to start the secure computation process:

```bash
python compute.py
python offchain.py
