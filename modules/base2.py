import csv

if __name__ != "__main__":
    import modules.tools as tools
else:
    import tools

def base2(phone=None, surname=None, name=None, patronymic=None, ip=None, birth=None):
    if phone:
        phone = tools.format_number(phone)
    else:
        return {}

    data = {}

    csv.field_size_limit(1000000)  # Устанавливаем лимит на 1 миллион символов

    with open("base/tele2.csv", "r", encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=";")
        for i, line in enumerate(reader):
            if not line:
                continue

            coincidences = [line[0] == str(phone)]
            if True in coincidences:
                full_name = line[1].strip()
                name_parts = full_name.split()

                data['surname'] = ''
                data['name'] = ''
                data['patronymic'] = ''

                if len(name_parts) == 3:
                    data['surname'] = name_parts[0]
                    data['name'] = name_parts[1]
                    data['patronymic'] = name_parts[2]
                elif len(name_parts) == 2:
                    data['surname'] = name_parts[0]
                    data['name'] = name_parts[1]
                elif len(name_parts) == 1:
                    data['name'] = name_parts[0]

                data['phone'] = line[0] if line[0] else ""
                break

    return data

if __name__ == '__main__':
    print(base2('79040999863'))
