# Fuck Fuckablock ping.
# Homepage: https://github.com/bogachenko/fuckfuckadblock
# Author: Bogachenko Vyacheslav <bogachenkove@gmail.com>
# License: MIT license <https://raw.githubusercontent.com/bogachenko/fuckfuckadblock/master/LICENSE.md>
# Created: June 2024
# Donate:
#          Bitcoin (BTC) - 3JfwK6ULJ1xY8xjpu6uzpBKLm4ghkdSBzG
#          Ethereum (ETH) - 0xb08eE5bC90C2fCAFE453b7d536f158215Cca979A
#          Tron (TRX) - THXmTuAbnMrUWFXPJn92YkWbEzjBDGAEXZ
#          Toncoin (TON) - UQDohNKO4GJj4VGDNwK2GYXtnvWbwgiECYB6V6aijfS2RY28
#          Dogecoin (DOGE) - DFuMmJb8DstHZQpqaCtQaeW5D6CVZHvqFa
#          Litecoin (LTC) - LfW2NSBZ3UwG7Sm9MWKLjEdVt45XVZ1je2
#          Binance Coin (BNB) uses the ETH address.
#          Tether (USDT) or USD Coin (USDC) uses ETH, TRX or TON addresses, depending on the type of chain chosen.

import os
import re
import requests
input_file = os.path.join(os.path.dirname(__file__), '..', '..', 'fuckfuckadblock-mining.txt')
output_file = os.path.join(os.getenv('TEMP'), 'ping', 'checkhosts.txt')
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()
domains = re.findall(r'\|\|(.*?)\^', content)
with open(output_file, 'w', encoding='utf-8') as f_out:
    for domain in domains:
        try:
            response = requests.get(f'http://{domain}', timeout=5)
            if response.status_code == 200:
                f_out.write(f'{domain}: Ping successful\n')
                print(f'Pinged {domain}: Success')
            else:
                f_out.write(f'{domain}: Ping failed (Status Code: {response.status_code})\n')
                print(f'Pinged {domain}: Failed (Status Code: {response.status_code})')
        except requests.exceptions.RequestException as e:
            f_out.write(f'{domain}: Ping failed (Exception: {str(e)})\n')
            print(f'Pinged {domain}: Failed (Exception: {str(e)})')
print(f'Found domains have been pinged and results saved to {output_file}')
