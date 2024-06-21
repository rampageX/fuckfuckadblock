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

import os, shutil
def patches(main_filename, mining_filename):
    def sort_domains(domains_part):
        return '|'.join(sorted(set(domains_part.split('|'))))
    def sort_params(params_part):
        return ','.join(sorted(set(params_part.split(','))))
    def process_line(line):
        if 'domain=' in line:
            start_index = line.find('domain=') + len('domain=')
            end_index = line.find(',', start_index)
            if end_index == -1:
                end_index = line.find('$', start_index)
            if end_index == -1:
                end_index = len(line)
            domains_part = line[start_index:end_index].strip()
            return line[:start_index] + sort_domains(domains_part) + line[end_index:]
        elif '##' in line or '###' in line:
            separator_index = line.find('##') if '##' in line else line.find('###')
            domains_part = line[:separator_index].strip()
            return ','.join(sorted(set(domains_part.split(',')))) + line[separator_index:]
        elif '$' in line:
            dollar_index = line.find('$')
            params_part = line[dollar_index + 1:].strip()
            return line[:dollar_index + 1] + sort_params(params_part)
        return line
    def process_file(file_path):
        temp_file = file_path + '.tmp'
        with open(file_path, 'r') as file, open(temp_file, 'w') as temp:
            for line in file:
                processed_line = process_line(line)
                if not processed_line.endswith('\n'):
                    processed_line += '\n'
                temp.write(processed_line)
        shutil.move(temp_file, file_path)
    script_dir = os.path.dirname(__file__)
    main_file_path = os.path.abspath(os.path.join(script_dir, '..', '..', main_filename))
    mining_file_path = os.path.abspath(os.path.join(script_dir, '..', '..', mining_filename))
    process_file(main_file_path)
    process_file(mining_file_path)
    print(f'Patches have been added to files {main_filename} and {mining_filename}, and they have been overwritten.')
main_filename = 'fuckfuckadblock.txt'
mining_filename = 'fuckfuckadblock-mining.txt'
patches(main_filename, mining_filename)