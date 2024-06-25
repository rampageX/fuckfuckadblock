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
                params = {'name': domain, 'type': 'A'}
                headers = {'accept': 'application/dns-json'}
                response = requests.get(doh_url, params=params, headers=headers, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if 'Answer' in data:
                        f_out.write(f'{domain}: DNS Ping successful\n')
                        print(f'Pinged {domain}: Success')
                    else:
                        f_out.write(f'{domain}: DNS Ping failed (No answer)\n')
                        print(f'Pinged {domain}: Failed (No answer)')
                        dead_hosts.append(f'{domain}: DNS Ping failed (No answer)')
                else:
                    f_out.write(f'{domain}: DNS Ping failed (Status Code: {response.status_code})\n')
                    print(f'Pinged {domain}: Failed (Status Code: {response.status_code})')
                    dead_hosts.append(f'{domain}: DNS Ping failed (Status Code: {response.status_code})')
            except requests.exceptions.RequestException as e:
                f_out.write(f'{domain}: DNS Ping failed (Exception: {str(e)})\n')
                print(f'Pinged {domain}: Failed (Exception: {str(e)})')
                dead_hosts.append(f'{domain}: DNS Ping failed (Exception: {str(e)})')
    with open(dead_hosts_file, 'w', encoding='utf-8') as f_dead:
        for line in dead_hosts:
            f_dead.write(f'{line}\n')
unique_domains = set()
for input_file in input_files:
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        domains = re.findall(r'\|\|(.*?)\^', content)
        filtered_domains = [domain for domain in domains if '/' not in domain]
        unique_domains.update(filtered_domains)
        domain_lines = re.findall(r'domain=(.*?)(?:\s|$)', content)
        for line in domain_lines:
            domains = line.split('|')
            filtered_domains = [domain.strip() for domain in domains if '/' not in domain]
            unique_domains.update(filtered_domains)
sorted_domains = sorted(unique_domains)
if internet_available():
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)
    ping_domains(sorted_domains, output_file)
    print('Checking the availability and quality of the network connection for the domains has been completed.')
else:
    print('No internet connection available. Please check your connection and try again.')