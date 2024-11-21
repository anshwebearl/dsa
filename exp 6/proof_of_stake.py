import hashlib
import time
import random
import json
import os


class Transaction:
    def __init__(self, sender, receiver, amount, timestamp=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp if timestamp else time.time()

    def __repr__(self):
        return f"Transaction(sender='{self.sender}', receiver='{self.receiver}', amount={self.amount}, timestamp={self.timestamp})"



class Block:
    def __init__(self, index, previous_hash, timestamp, transaction, validator):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transaction = transaction  # Single transaction
        self.validator = validator
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.validator}".encode() + \
                       str(self.transaction).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'transaction': self.transaction.__dict__,
            'validator': self.validator,
            'hash': self.hash
        }


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_validators = {}
        self.load_blockchain()
        if not self.chain:  # If the chain is empty, create a genesis block
            self.create_genesis_block()

    def create_genesis_block(self):
        genesis_transaction = Transaction(
            "Genesis", "Genesis", 0)  # No real transaction
        self.create_block(
            previous_hash='0', validator='Genesis Validator', transaction=genesis_transaction)

    def create_block(self, previous_hash, validator, transaction=None):
        index = len(self.chain) + 1
        timestamp = time.time()
        new_block = Block(index, previous_hash, timestamp,
                          transaction, validator)
        self.chain.append(new_block)
        self.save_blockchain()
        return new_block

    def add_validator(self, validator_id, stake):
        self.current_validators[validator_id] = stake

    def select_validator(self):
        total_stake = sum(self.current_validators.values())
        if total_stake == 0:
            return None

        random_value = random.uniform(0, total_stake)
        cumulative_stake = 0

        for validator, stake in self.current_validators.items():
            cumulative_stake += stake
            if cumulative_stake > random_value:
                return validator

    def mint_block(self):
        sender = input("Enter sender's ID: ")
        receiver = input("Enter receiver's ID: ")
        amount = float(input("Enter amount: "))
        transaction = Transaction(sender, receiver, amount)

        validator = self.select_validator()
        if validator:
            previous_hash = self.chain[-1].hash if self.chain else '0'
            self.create_block(previous_hash, validator, transaction)
            print("Block minted successfully.")
        else:
            print("No validators available to mint the block.")

    def save_blockchain(self):
        with open('blockchain.json', 'w') as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=4)

    def load_blockchain(self):
        if os.path.exists('blockchain.json'):
            with open('blockchain.json', 'r') as f:
                blockchain_data = json.load(f)
                for block_data in blockchain_data:
                    transaction = Transaction(**block_data['transaction'])  # Includes timestamp now
                    block = Block(
                        index=block_data['index'],
                        previous_hash=block_data['previous_hash'],
                        timestamp=block_data['timestamp'],
                        transaction=transaction,
                        validator=block_data['validator']
                    )
                    self.chain.append(block)



def display_menu():
    print("\nBlockchain Menu:")
    print("1. Add Validator")
    print("2. Mint Block")
    print("3. View Blockchain")
    print("4. Exit")


def main():
    blockchain = Blockchain()

    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            validator_id = input("Enter validator ID: ")
            stake = int(input("Enter stake amount: "))
            blockchain.add_validator(validator_id, stake)
            print(f"Validator {validator_id} with stake {stake} added.")

        elif choice == '2':
            blockchain.mint_block()

        elif choice == '3':
            for block in blockchain.chain:
                print(f"Block {block.index}:")
                print(f"Hash: {block.hash}")
                print(f"Previous Hash: {block.previous_hash}")
                print(f"Timestamp: {block.timestamp}")
                print(f"Transaction: {block.transaction}")
                print(f"Validator: {block.validator}\n")

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
