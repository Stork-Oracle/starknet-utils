import os
import pytest

from starkware.starknet.testing.starknet import Starknet

# The path to the contract source code.
CONTRACT_FILE = os.path.join(
    os.path.dirname(__file__), "felt_unpacker.cairo")

# The testing library uses python's asyncio. So the following
# decorator and the ``async`` keyword are needed.
@pytest.mark.asyncio
async def test_unpack():
    # Create a new Starknet class that simulates the StarkNet
    # system.
    starknet = await Starknet.empty()

    # Deploy the contract.
    contract = await starknet.deploy(
        source=CONTRACT_FILE,
    )

    execution_info = await contract.unpack_felt(packed_felt=8594493568283152773212111322199588026419403, schema=[80,32,32]).call()

    print(execution_info.result)
    assert execution_info.result == ([1655239252, 12303, 249834169927883],)