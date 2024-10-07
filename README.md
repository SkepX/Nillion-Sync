# Nillion Integration README

## Overview

This project demonstrates secure communication and computation using Nillion's infrastructure, focusing on interactions between two parties: Sync (Initiator) and User (Responder). Nillion enables the encrypted storage and secure handling of sensitive data during the communication process.

## Key Components

- **Sync (Initiator):** Initiates the program, triggers notifications, and manages data through Nillion's network.
- **User (Responder):** Creates a SyncID, attaches sensitive data, and interacts with Sync using Nillion's secure computation.
- **Delivery Node (User's Local Device):** The device where decryption occurs, using the Sync mobile app to access the message securely.

## Process Flow

1. **SyncID Creation:** The User creates a SyncID and attaches sensitive details (like their WhatsApp number) to it. This information is securely stored on the Nillion network with a unique secret.
   
2. **Data Storage on Nillion:** The sensitive information linked to the SyncID is encrypted and stored in Nillion's decentralized network.

3. **Notification Trigger:** When a notification is generated in the Sync network for delivery to a specific SyncID, it is directed to the User's delivery node (local device) via the Sync mobile app.

4. **Secret Matching:** The Sync app on the delivery node securely matches the secret identifier provided by both Sync and User with the encrypted data stored in Nillion's network.
   - If the secret identifiers match, Nillion facilitates the secure decryption of the message locally on the delivery node.

5. **Decryption and Message Delivery:** The decrypted message is accessed locally on the User's device, and the Sync app triggers the delivery to WhatsApp or Telegram using the decrypted data.

## Security Features

- **Local Decryption:** Sensitive data is decrypted only on the User's device, ensuring privacy.
- **Data Integrity:** The logic matching and validation are securely handled by Nillion without exposing sensitive information.
- **Decentralized Execution:** Leverages Nillion’s infrastructure for secure computation and encrypted data handling.

## Usage

To start the secure computation and interaction process, execute the following commands:

```bash
python compute.py
python offchain.py
