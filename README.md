# Utilities for Starknet
## Felt Packing
Until further optimizations are implemented, storage on StarkNet is expensive see [this excellent analysis](https://hackmd.io/@RoboTeddy/BJZFu56wF) to learn more. A reasonable way to work around this is to refund fees paid for reused storage between L1 updates. But alas, this isn't the case today.

In the interim, felts can safely fit 252 bits, which is a fair amount of data (e.g. 7 32-bit ints, 31 ASCII characeters, etc).

The provided libraries allow you to "stuff" or "pack" multiple values into a single felt. 

For example, you can pack a 32-bit timestamp, 32-bit price, and a short oracle name in a single felt, and still have headroom to spare. 

``` python
    # Example using
    # --------------------------------------------------------------------------------- #
    # | timestamp (32 bits)     | price (32 bits)              |   oracle (80 bits)   | #
    # | Eg. 1655239252          | 12303.01*10**2               |   Stork              | #  
    # --------------------------------------------------------------------------------- #
    
    schema = [('timestamp', 32), ('price', 32), ('oracle', 80)]
    price = int(12303.01*10**2)
    oracle = int('Stork'.encode('ascii').hex(),16)
    
    entries = {
        'timestamp': 1655239252,
        'price': price, 
        'oracle': oracle
    }

    packed_felt = pack(entries, schema)
    # packed_felt => 8594493568284625242442550301055646065193579
```

And then the same values can be unpacked in Cairo:
```
execution_info = await contract.unpack_felt(packed_felt=8594493568284625242442550301055646065193579, schema=[80,32,32]).call()
# execution_info.result => [1655239252, 1230301, 358435746411]
```

Just note that the schema order has to be reversed in Cairo (32,32,80 in Python vs. 80,32,32 in Cairo – ofc feel free to reverse it programmatically, e.g. using https://github.com/gaetbout/starknet-array-manipulation)
