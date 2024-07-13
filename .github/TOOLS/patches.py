# Fuck Fuckablock patches.
# Homepage: https://github.com/bogachenko/fuckfuckadblock
# Author: Bogachenko Vyacheslav <bogachenkove@gmail.com>
# License: MIT license <https://raw.githubusercontent.com/bogachenko/fuckfuckadblock/master/LICENSE.md>
# Last update: July 2024
# Donate:
#          Bitcoin (BTC) - 1PvKpxpGRiw83afJi2kWFUXwSdxpFXLUW9
#          Bitcoin Cash (BCH) - 1hE3asiyEzVoMPQifKq8c34yAgVE1BquX
#          Ethereum (ETH) - 0xb08eE5bC90C2fCAFE453b7d536f158215Cca979A
#          Ethereum Classic (ETC) - 0x908E4623Ba8a0518F2CCAb9b4123B336AE4e0078
#          Tron (TRX) - THXmTuAbnMrUWFXPJn92YkWbEzjBDGAEXZ
#          Toncoin (TON) - UQDohNKO4GJj4VGDNwK2GYXtnvWbwgiECYB6V6aijfS2RY28
#          Dogecoin (DOGE) - DFuMmJb8DstHZQpqaCtQaeW5D6CVZHvqFa
#          Litecoin (LTC) - LfW2NSBZ3UwG7Sm9MWKLjEdVt45XVZ1je2
#          Solana (SOL) - 9oboHCvKTcwc47eFyhuYpwYcsyyvybv4qsspsbn1q9gA
#          Ripple (XRP) - rUPys7DwSu9BPSKJNcX9NknjrMHiD6KZmL
#          Binance Coin (BNB) uses the ETH address.
#          Tether (USDT) uses TRX, ETH, BNB, TON or SOL addresses, depending on the type of chain chosen.
#          USD Coin (USDC) uses TRX, ETH, BNB or SOL addresses, depending on the type of chain chosen.
#          Binance USD (BUSD) uses TRX, ETH, BNB addresses, depending on the type of chain chosen.

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
    pattern3 = re.compile(r'(.*\$)(.*)')
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
                match3 = pattern3.search(line)
                if match3:
                    pre_dollar = match3.group(1)
                    post_dollar = match3.group(2).strip()
                    sorted_params = ','.join(sorted(post_dollar.split(',')))
                    sorted_line = f'{pre_dollar}{sorted_params}\n'
                    sorted_lines.append(sorted_line)
                else:
                    sorted_lines.append(line)
    with open(file_path, 'w') as file:
        file.writelines(sorted_lines)
    shutil.rmtree(temp_dir)
    print(f'File {filename} has been updated.')
patch(main_filename)
patch(mining_filename)