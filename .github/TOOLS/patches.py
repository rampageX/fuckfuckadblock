# Fuck Fuckablock patches.
# Homepage: https://github.com/bogachenko/fuckfuckadblock
# Author: Bogachenko Vyacheslav <bogachenkove@gmail.com>
# License: MIT license <https://raw.githubusercontent.com/bogachenko/fuckfuckadblock/master/LICENSE.md>
# Last update: July 2024
# Donate:
#          Bitcoin (BTC) - 3JfwK6ULJ1xY8xjpu6uzpBKLm4ghkdSBzG
#          Ethereum (ETH) - 0xb08eE5bC90C2fCAFE453b7d536f158215Cca979A
#          Tron (TRX) - THXmTuAbnMrUWFXPJn92YkWbEzjBDGAEXZ
#          Toncoin (TON) - UQDohNKO4GJj4VGDNwK2GYXtnvWbwgiECYB6V6aijfS2RY28
#          Dogecoin (DOGE) - DFuMmJb8DstHZQpqaCtQaeW5D6CVZHvqFa
#          Litecoin (LTC) - LfW2NSBZ3UwG7Sm9MWKLjEdVt45XVZ1je2
#          Binance Coin (BNB) uses the ETH address.
#          Tether (USDT) or USD Coin (USDC) uses ETH, TRX or TON addresses, depending on the type of chain chosen.

import os, re, shutil, tempfile
main_filename = 'fuckfuckadblock.txt'
mining_filename = 'fuckfuckadblock-mining.txt'
def patch(filename):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.abspath(os.path.join(script_dir, '..', '..', filename))
    if not os.path.exists(file_path):
        print(f'File {filename} does not exist.')
        return
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, os.path.basename(filename))
    shutil.copy(file_path, temp_file_path)
    sorted_lines = []
    pattern = re.compile(r'#[#?$@]?#')
    pattern1 = re.compile(r'^[^a-zA-Z0-9#@!/|]+')
    pattern2 = re.compile(r'domain=(.*?)(,|$)')
    with open(temp_file_path, 'r') as file:
        for line in file:
            match1 = pattern1.search(line)
            if match1:
                line = line[match1.end():]
            line = pattern2.sub(lambda m: f'domain={"|".join(sorted(set(m.group(1).split("|"))))}{m.group(2)}', line)
            match = pattern.search(line)
            if match:
                separator_index = match.start()
                if separator_index > 0:
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
    shutil.rmtree(temp_dir)
    print(f'File {filename} has been updated.')
patch(main_filename)
patch(mining_filename)