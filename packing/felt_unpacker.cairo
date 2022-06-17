%lang starknet

from starkware.starknet.common.syscalls import get_caller_address
from starkware.cairo.common.bitwise import bitwise_and
from starkware.cairo.common.cairo_builtins import HashBuiltin, BitwiseBuiltin
from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.pow import pow

# Returns an array of felts that were packed into packed_felt
#
# See corresponding python script to pack
# For example: 8594493568283152773212111322199588026419403 3 80 32 32
# Note that the order of elements is inverted compared to the Python script (LSB -> MSB)
# i.e. in python, you would pass 32, 32, 80
# Or use https://github.com/gaetbout/starknet-array-manipulation to flip the array

# Sample Use (matches Python example): nile call CONTRACT unpack_felt 8594493568283152773212111322199588026419403 3 80 32 32
@view
func unpack_felt{syscall_ptr : felt*,pedersen_ptr : HashBuiltin*, bitwise_ptr : BitwiseBuiltin*, range_check_ptr}(
    packed_felt: felt, schema_len: felt, schema: felt*) -> (values_len: felt, values: felt*
):
    alloc_locals
    let (unpacked_fields : felt*) = alloc()
    let unpacked_fields_len = 0
    let (unpacked_fields_len, unpacked_fields) = _unpack_felt(packed_felt, schema, schema_len, unpacked_fields, unpacked_fields_len)

    return (unpacked_fields_len, unpacked_fields)
end

func _unpack_felt{syscall_ptr : felt*,pedersen_ptr : HashBuiltin*, bitwise_ptr : BitwiseBuiltin*, range_check_ptr}(
    packed_felt: felt, schema: felt*, schema_len: felt, unpacked_felts: felt*, unpacked_felts_len: felt
) -> (unpacked_felts_len: felt, unpacked_felts: felt*):

    alloc_locals

    if schema_len == 0:
        return (unpacked_felts_len,unpacked_felts)
    end

    let current_field = [schema]

    let (offset) = pow(2, current_field)
    tempvar mask = offset - 1

    let (current_value) = bitwise_and(packed_felt, mask)

    tempvar _pf2 = packed_felt - current_value
    tempvar packed_felt_remainder = _pf2 / offset
    
    assert unpacked_felts[schema_len - 1] = current_value
    
    return _unpack_felt(packed_felt_remainder, &schema[1], schema_len - 1, unpacked_felts, unpacked_felts_len + 1)
end