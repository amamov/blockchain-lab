import collections
import hashlib


def sorted_dict_by_key(unsorted_dict):
    return collections.OrderedDict(sorted(unsorted_dict.items(), key=lambda d: d[0]))


def print_block_chain(chains):
    for idx, chain in enumerate(chains):
        print(f"{'='*25} Chain {idx} {'='*25}")
        for key, value in chain.items():
            if key == "transactions":
                print(key)
                for transaction in value:
                    print(f"{'-'*40}")
                    for transaction_key, transaction_value in transaction.items():
                        print(f"{transaction_key:30}{transaction_value}")
            else:
                print(f"{key:15}{value}")

    print(f"{'*'*100}")


if __name__ == "__main__":
    print(hashlib.sha256("test".encode()).hexdigest())
    print(hashlib.sha256("test".encode()).hexdigest())
    print(hashlib.sha256("test2".encode()).hexdigest())
    print(hashlib.sha256("test2".encode()).hexdigest())

    block = {"b": 2, "a": 1}
    print(hashlib.sha256(str(block).encode()).hexdigest())
    block = {"a": 1, "b": 2}
    print(hashlib.sha256(str(block).encode()).hexdigest())

    collections.OrderedDict(sorted(block.items(), key=lambda d: d[0]))
