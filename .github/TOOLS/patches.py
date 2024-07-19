# Fuck Fuckablock patches.
# Homepage: https://github.com/bogachenko/fuckfuckadblock
# Author: Bogachenko Vyacheslav <bogachenkove@gmail.com>
# License: MIT license <https://raw.githubusercontent.com/bogachenko/fuckfuckadblock/master/LICENSE.md>
# Last update: July 2024
# Donate:
#   Bitcoin (BTC) - bc1qnmderzmag45pa3a0jyaqah654x0055n6y8madh
#   Bitcoin Cash (BCH) - qzptqmjr0vrj053wgcxa5yesdlejk973xq9xctmxcg
#   Ethereum (ETH) - 0xE4869C3140134522383E316d329612bC886F85E2
#   Ethereum Classic (ETC) - 0x4A11511a9C69eA1CFa8B1135c9B8A3B27c84eE55
#   Tron (TRX) - TW8ocDJLPTnVFG4Karb7zctbBfjFaZfuJn
#   Toncoin (TON) - UQCt3JyjW8EvFidU18qnrnfMnSdTWdqKJkJpvuxW9W0dwTU7
#   Dogecoin (DOGE) - D7BHKJ4ymU5uZKrju5BbYQpSfdENc5qtr1
#   Litecoin (LTC) - ltc1q3t9hmgqyze8qlrw56rxepyw8ll44jcl7uc8z4p
#   Solana (SOL) - 5fsRA5NiQKX5GLzatbmYS7UbZ9Q2LMqdCH7pBgtrXDJM
#   Ripple (XRP) - rnEWArfEDm4yFJeG7xnvDCkW7GKperxf6t
#   Cardano (ADA) - addr1q8yjcner4yq7kgd0gleq4qf0gae2xemvvpu790nhfk7a3y8gje4zxphcq0kyg3ry5yvgtzy2huhd49l9rdwmh6khmm4se2er3a
#   Zcash (ZEC) - t1N8QRJg6jFt2m92DyFkYVDEv36ZK3JnQP2
#   Binance Coin (BNB) uses the ETH address.
#   Tether (USDT) uses TRX, ETH, BNB, TON or SOL addresses, depending on the type of chain chosen.
#   USD Coin (USDC) uses TRX, ETH, BNB or SOL addresses, depending on the type of chain chosen.
#   Binance USD (BUSD) uses TRX, ETH, BNB addresses, depending on the type of chain chosen.

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