import json
from web3 import Web3

# Memuat ABI dari file
with open('abi.json') as f:
    contract_abi = json.load(f)

# Inisialisasi web3
web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))

# Alamat kontrak
contract_address = '0xd983c531A03072e34072537fae0A45660f919802'

# Inisialisasi kontrak
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Kunci pribadi dan alamat akun
private_key = '6d546249e8e680f23b9ef158ffd0897ff37eb9a1c9210fd1ce0f81ea9474ae62'
account_address = '0xe0Fbe16645338c02E1A4d863192C93B2fe882fbf'

def wrap(amount):
    try:
        # Konversi jumlah ke Wei
        amount_in_wei = Web3.toWei(amount, 'ether')
        
        # Membangun transaksi
        txn = contract.functions.mint(amount_in_wei).buildTransaction({
            'from': account_address,
            'value': amount_in_wei,
            'gas': 2000000,
            'gasPrice': web3.toWei('5', 'gwei'),
            'nonce': web3.eth.getTransactionCount(account_address),
        })

        # Menandatangani transaksi
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)

        # Mengirim transaksi
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return f'Transaksi dikirim: {web3.toHex(tx_hash)}'
    except Exception as e:
        return str(e)

def unwrap(amount):
    try:
        # Konversi jumlah ke Wei
        amount_in_wei = Web3.toWei(amount, 'ether')

        # Membangun transaksi
        txn = contract.functions.burn(amount_in_wei).buildTransaction({
            'from': account_address,
            'gas': 2000000,
            'gasPrice': web3.toWei('5', 'gwei'),
            'nonce': web3.eth.getTransactionCount(account_address),
        })

        # Menandatangani transaksi
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)

        # Mengirim transaksi
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return f'Transaksi dikirim: {web3.toHex(tx_hash)}'
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    action = input("Apakah Anda ingin membungkus atau membungkus BNB? (wrap/unwrap): ").strip().lower()
    amount = float(input("Masukkan jumlah dalam BNB: "))

    if action == 'wrap':
        print(wrap(amount))
    elif action == 'unwrap':
        print(unwrap(amount))
    else:
        print("Aksi tidak valid. Silakan masukkan 'wrap' atau 'unwrap'.")