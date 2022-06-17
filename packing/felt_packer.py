def pack(entries, schema):
    """ Returns a packed felt (int)

    Schema: [{key: length_in_bits},...]
    Entries: {key: value, ...}

    Packs the values of entries into a single felt, using the schema
    Schema is ordered MSB -> LSB
    Schema must fit in under 250 bits
    """
    # ensure data fits in felt
    assert sum(map(lambda x: x[1], schema)) <= 250
    packed = 0
    for i in range(len(schema)):
        key, size = schema[i]
        entry = entries[key]
        assert 0 <= entry <= 2**size
        
        if (i > 0):
            packed *= 2**size # note: can bitshift instead, e.g. packed << size
            
        packed += entry
        
    return packed


def unpack(packed_result, schema):
    """ Returns a Dict with the keys in schema extracted from packed_result

    Note that order in schema is not preserved
    """
    unpacked = {}
    packed_temp = packed_result
    for v in reversed(schema):
        key, size = v
        r = packed_temp & (2**size-1)
        unpacked[key] = r
        packed_temp -= r
        packed_temp = packed_temp // 2**size
    
    return unpacked

if __name__ == '__main__':
    print('''
    Example using
    # --------------------------------------------------------------------------------- #
    # | timestamp (32 bits)     | price (32 bits)              |   oracle (80 bits)   | #
    # | Eg. 1655239252          | 12303.01*10**2               |   Stork              | #  
    # --------------------------------------------------------------------------------- #
    ''')
    schema = [('timestamp', 32), ('price', 32), ('oracle', 80)]
    price = int(12303.01*10**2) # not using all 32 bits; just an example.
    oracle = int('Stork'.encode('ascii').hex(),16)
    
    entries = {
        'timestamp': 1655239252,
        'price': price, 
        'oracle': oracle
    }

    print(f'Entries: {entries}')
    packed_felt = pack(entries, schema)
    print(f'Packed Felt: {packed_felt}')
    unpacked_felts = unpack(packed_felt, schema)
    print(f'Unpacked Felt: {unpacked_felts}')

    assert entries == unpacked_felts

