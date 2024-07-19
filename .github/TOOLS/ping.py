# Fuck Fuckablock ping.
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

import os, re, requests, tempfile
redcolor = '\033[91m'
yellowcolor = '\033[93m'
resetcolor = '\033[0m'
input_files = [
    os.path.join(os.path.dirname(__file__), '..', '..', 'fuckfuckadblock-mining.txt'),
    os.path.join(os.path.dirname(__file__), '..', '..', 'fuckfuckadblock.txt')
]
output_file = os.path.join(tempfile.gettempdir(), 'ping', 'checkhosts.txt')
dead_hosts_file = os.path.join(tempfile.gettempdir(), 'ping', 'deadhosts.txt')
doh_url = 'https://dns.cloudflare.com/dns-query'
internet_test_url = 'http://1.1.1.1'
def internet_available():
    try:
        requests.get(internet_test_url, timeout=5)
        return True
    except requests.exceptions.RequestException:
        return False
def ping_domains(domains, output_file):
    dead_hosts = []
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for domain in domains:
            if domain.startswith('~'):
                domain = domain[1:]
            try:
                response = requests.get(doh_url, params={'name': domain, 'type': 'A'}, headers={'accept': 'application/dns-json'}, timeout=5)
                if response.status_code == 200 and 'Answer' in response.json():
                    f_out.write(f'{domain}: DNS Ping successful\n')
                    print(f'Pinged {yellowcolor}{domain}{resetcolor}: Success')
                else:
                    error_msg = f'{domain}: DNS Ping failed (No answer)' if response.status_code == 200 else f'{domain}: DNS Ping failed (Status Code: {response.status_code})'
                    f_out.write(f'{error_msg}\n')
                    print(f'Pinged {redcolor}{domain}{resetcolor}: {error_msg}')
                    dead_hosts.append(error_msg)
            except requests.exceptions.RequestException as e:
                error_msg = f'{domain}: DNS Ping failed (Exception: {str(e)})'
                f_out.write(f'{error_msg}\n')
                print(f'Pinged {redcolor}{domain}{resetcolor}: {error_msg}')
                dead_hosts.append(error_msg)
    with open(dead_hosts_file, 'w', encoding='utf-8') as f_dead:
        for line in dead_hosts:
            f_dead.write(f'{line}\n')
unique_domains = set()
domain_patterns = [
    r'\|\|(.*?)\^',
    r'domain=(.*?)(?:\s|,|$)',
    r'([a-zA-Z0-9\-_.]+(?:,[a-zA-Z0-9\-_.]+)*)(?=##[#$?@]?)'
]
for input_file in input_files:
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        for pattern in domain_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if match:
                    domains = match.split(',') if ',' in match else match.split('|')
                    filtered_domains = [domain.strip() for domain in domains if '/' not in domain]
                    unique_domains.update(filtered_domains)
sorted_domains = sorted(unique_domains)
if internet_available():
    ping_domains(sorted_domains, output_file)
    print('Checking the availability and quality of the network connection for the domains has been completed.')
else:
    print('No internet connection available. Please check your connection and try again.')