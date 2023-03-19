api_key="XTpKrQGSk3GhXzqiEV4OfwGJzmTVcLh8dKGwHo4aQBH4p0mOqPDpIsxdh95tjGVf"
secret ="A0eqZGEWHsyL3NMM6WuDrucIanr7A2YZAnrwXVPhXpf2WGauIANwa5zsoNeNt0hs"

import ccxt

binance = ccxt.binance(config={
    'apiKey' : api_key,
    'secret' : secret
})

balance = binance.fetch_balance(params={'type': "future"})
print(balance)
