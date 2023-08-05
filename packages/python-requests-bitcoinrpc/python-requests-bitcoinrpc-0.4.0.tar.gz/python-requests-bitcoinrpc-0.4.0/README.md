[![GitHub Release](https://img.shields.io/github/v/release/normoes/python-bitcoinrpc.svg)](https://github.com/normoes/python-bitcoinrpc/releases)
[![GitHub Tags](https://img.shields.io/github/v/tag/normoes/python-bitcoinrpc.svg)](https://github.com/normoes/python-bitcoinrpc/tags)

This project further improves [`python-bitcoinrpc`](https://github.com/jgarzik/python-bitcoinrpc) by making use of the `requests` module.

`requests` replaces plain `http.client` and `httplib`, respectively.

It's basically a mixture of the projects [`python-bitcoinrpc`](https://github.com/jgarzik/python-bitcoinrpc) and [`python-monerorpc`](https://github.com/monero-ecosystem/python-monerorpc).

The first version to contain the above change is tag `v0.4.0`.

---

AuthServiceProxy is an improved version of python-jsonrpc.

It includes the following generic improvements:

- HTTP connections persist for the life of the AuthServiceProxy object
- sends protocol 'version', per JSON-RPC 1.1
- sends proper, incrementing 'id'
- uses standard Python json lib
- can optionally log all RPC calls and results
- JSON-2.0 batch support

It also includes the following bitcoin-specific details:

- sends Basic HTTP authentication headers
- parses all JSON numbers that look like floats as Decimal,
  and serializes Decimal values to JSON-RPC connections.

Installation:

- change the first line of setup.py to point to the directory of your installation of python 2.*
- run setup.py

Note: This will only install bitcoinrpc. If you also want to install jsonrpc to preserve
backwards compatibility, you have to replace 'bitcoinrpc' with 'jsonrpc' in setup.py and run it again.

Example usage:

    from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

    # rpc_user and rpc_password are set in the bitcoin.conf file
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(rpc_user, rpc_password))
    best_block_hash = rpc_connection.getbestblockhash()
    print(rpc_connection.getblock(best_block_hash))

    # batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
    commands = [ [ "getblockhash", height] for height in range(100) ]
    block_hashes = rpc_connection.batch_(commands)
    blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
    block_times = [ block["time"] for block in blocks ]
    print(block_times)

Logging all RPC calls to stderr:

    from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
    import logging

    logging.basicConfig()
    logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(rpc_user, rpc_password))
    print(rpc_connection.getinfo())

Produces output on stderr like:

    DEBUG:BitcoinRPC:-1-> getinfo []
    DEBUG:BitcoinRPC:<-1- {"connections": 8, ...etc }
