# Fuck Fuckablock ping.
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
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    ping_domains(sorted_domains, output_file)
    print('Checking the availability and quality of the network connection for the domains has been completed.')
else:
    print('No internet connection available. Please check your connection and try again.')