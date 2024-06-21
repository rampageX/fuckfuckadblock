def sort_domains_in_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    updated_lines = []
    domain_index = None
    # Находим строку с "domain="
    for i, line in enumerate(lines):
        if 'domain=' in line:
            domain_index = i
            break
    if domain_index is not None:
        # Находим часть строки после "domain="
        domain_line = lines[domain_index]
        start_index = domain_line.find('domain=') + len('domain=')
        end_index = domain_line.find(',', start_index)  # ищем запятую после domain=, чтобы ограничить область
        if end_index == -1:
            end_index = domain_line.find('$', start_index)  # если запятая не найдена, ищем доллар

        if end_index == -1:
            end_index = len(domain_line)  # если и доллар не найден, берем до конца строки

        domain_part = domain_line[start_index:end_index].strip()

        # Разбираем домены, разделенные |
        domains = domain_part.split('|')
        sorted_domains = sorted(domains)

        # Формируем обновленную строку для записи
        updated_domain_line = domain_line[:start_index]
        updated_domain_line += '|'.join(sorted_domains)
        updated_domain_line += domain_line[end_index:]

        # Заменяем строку в списке lines
        lines[domain_index] = updated_domain_line

        # Перезаписываем файл
        with open(filename, 'w') as file:
            file.writelines(lines)

        print(f'Домены в файле {filename} были отсортированы и перезаписаны.')

    else:
        print(f'Не найдена строка с "domain=" в файле {filename}.')

# Пример использования:
filename = 'fuckfuckadblock.txt'
sort_domains_in_file(filename)
