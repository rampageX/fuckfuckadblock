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
    script_dir = os.path.dirname(__file__)
    file_path = os.path.abspath(os.path.join(script_dir, '..', '..', filename))
    updated_lines = []
    js_lines = []
    script_has_text_lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if 'domain=' in line:
            start_index = line.find('domain=') + len('domain=')
            end_index = line.find(',', start_index)
            if end_index == -1:
                end_index = line.find('$', start_index)
            if end_index == -1:
                end_index = len(line)
            domain_part = line[start_index:end_index].strip()
            domains = domain_part.split('|')
            sorted_domains = sorted(domains)
            updated_domain_line = line[:start_index]
            updated_domain_line += '|'.join(sorted_domains)
            updated_domain_line += line[end_index:]
            if not updated_domain_line.endswith('\n'):
                updated_domain_line += '\n'
            updated_lines.append(updated_domain_line)
        elif '##+js(' in line:
            js_start_index = line.find('##+js(')
            js_domains_part = line[:js_start_index].strip()
            js_domains = js_domains_part.split(',')
            sorted_js_domains = sorted(js_domains)
            updated_js_line = ','.join(sorted_js_domains)
            updated_js_line += line[js_start_index:].strip() + '\n'
            updated_lines.append(updated_js_line)
        elif '##^script:has-text(' in line:
            script_start_index = line.find('##^script:has-text(')
            script_domains_part = line[:script_start_index].strip()
            script_domains = script_domains_part.split(',')
            sorted_script_domains = sorted(script_domains)
            updated_script_line = ','.join(sorted_script_domains)
            updated_script_line += line[script_start_index:].strip() + '\n'
            updated_lines.append(updated_script_line)
        else:
            updated_lines.append(line)
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)
    print(f'Patches have been added to file {filename} and overwritten.')
filename = 'fuckfuckadblock.txt'
sort_domains_in_file(filename)