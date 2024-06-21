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

import os
def sort_domains_in_file(filename):
    def sort_domains(domain_part):
        domains = domain_part.split('|')
        sorted_domains = sorted(set(domains))
        return '|'.join(sorted_domains)
    script_dir = os.path.dirname(__file__)
    file_path = os.path.abspath(os.path.join(script_dir, '..', '..', filename))
    temp_file = file_path + '.tmp'
    with open(file_path, 'r') as file, open(temp_file, 'w') as temp:
        for line in file:
            if 'domain=' in line:
                start_index = line.find('domain=') + len('domain=')
                end_index = line.find(',', start_index)
                if end_index == -1:
                    end_index = line.find('$', start_index)
                if end_index == -1:
                    end_index = len(line)
                domain_part = line[start_index:end_index].strip()
                updated_domain_line = line[:start_index] + sort_domains(domain_part) + line[end_index:]
                if not updated_domain_line.endswith('\n'):
                    updated_domain_line += '\n'
                temp.write(updated_domain_line)
            elif '##' in line or '###' in line:
                separator_index = line.find('##') if '##' in line else line.find('###')
                domains_part = line[:separator_index].strip()
                sorted_domains_line = ','.join(sorted(set(domains_part.split(','))))
                updated_line = sorted_domains_line + line[separator_index:].strip() + '\n'
                temp.write(updated_line)
            elif '$' in line:
                dollar_index = line.find('$')
                params_part = line[dollar_index + 1:].strip()
                sorted_params_line = line[:dollar_index + 1] + ','.join(sorted(set(params_part.split(',')))) + '\n'
                temp.write(sorted_params_line)
            else:
                temp.write(line)
    os.replace(temp_file, file_path)
    print(f'Patches have been added to file {filename} and overwritten.')
filename = 'fuckfuckadblock.txt'
sort_domains_in_file(filename)