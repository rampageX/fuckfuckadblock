# Fuck Fuckablock patches.
# Homepage: https://github.com/bogachenko/fuckfuckadblock
# Author: Bogachenko Vyacheslav <bogachenkove@gmail.com>
# License: MIT license <https://raw.githubusercontent.com/bogachenko/fuckfuckadblock/master/LICENSE.md>
# Last update: June 2024
# Donate:
#          Bitcoin (BTC) - 3JfwK6ULJ1xY8xjpu6uzpBKLm4ghkdSBzG
#          Ethereum (ETH) - 0xb08eE5bC90C2fCAFE453b7d536f158215Cca979A
#          Tron (TRX) - THXmTuAbnMrUWFXPJn92YkWbEzjBDGAEXZ
#          Toncoin (TON) - UQDohNKO4GJj4VGDNwK2GYXtnvWbwgiECYB6V6aijfS2RY28
#          Dogecoin (DOGE) - DFuMmJb8DstHZQpqaCtQaeW5D6CVZHvqFa
#          Litecoin (LTC) - LfW2NSBZ3UwG7Sm9MWKLjEdVt45XVZ1je2
#          Binance Coin (BNB) uses the ETH address.
#          Tether (USDT) or USD Coin (USDC) uses ETH, TRX or TON addresses, depending on the type of chain chosen.

import os, re
def sort_and_remove_duplicates(filename):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.abspath(os.path.join(script_dir, '..', '..', filename))
    sorted_lines = []
    pattern = re.compile(r'#[#?$@]?#')
    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                separator_index = match.start()
                if separator_index > 0:  # Check if there is text before '##' or '###'
                    words_part = line[:separator_index].strip()
                    unique_sorted_words = sorted(set(words_part.split(',')))
                    sorted_line = ','.join(unique_sorted_words) + line[separator_index:]
                    sorted_lines.append(sorted_line)
                else:
                    sorted_lines.append(line)
            else:
                sorted_lines.append(line)
    with open(file_path, 'w') as file:
        file.writelines(sorted_lines)
    print(f'Sorted and removed duplicates in lines matching pattern #[#?$@]?# in {filename}.')
    print(f'Lines have been sorted alphabetically and duplicates removed before the pattern.')
    print(f'File {filename} has been updated.')
main_filename = 'fuckfuckadblock.txt'
mining_filename = 'fuckfuckadblock-mining.txt'
sort_and_remove_duplicates(main_filename)
sort_and_remove_duplicates(mining_filename)