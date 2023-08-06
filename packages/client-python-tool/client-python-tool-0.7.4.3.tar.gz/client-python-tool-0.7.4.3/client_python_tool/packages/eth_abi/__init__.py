import pkg_resources

from client_python_tool.packages.eth_abi.abi import (
    decode_single,
    decode_abi,
    encode_single,
    encode_abi,
    is_encodable,
)
try:
   __version__ = pkg_resources.get_distribution('eth-abi').version
except:
    __version__='0.7.1'