import csv
import json

if __name__ != "__main__":
    import modules.tools as tools
else:
    import tools

def base1(phone=None, surname=None, name=None, patronymic=None, ip=None, birth = None):
    data = {}

    with open("base/1.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            line = [value if value != 'NULL' else '' for value in line]
            coincidences = [phone and line[4] == phone, ip and line[24] == ip]
            
            if True in coincidences:
                data["email"] = line[1]

                data["surname"] = line[2].split()[0]
                if len(line[2].split()) == 2:
                    data["name"] = line[2].split()[1]
                if len(line[2].split()) == 3:
                    data["name"] = line[2].split()[1]
                    data["patronymic"] = line[2].split()[2]

                data["phone"] = line[4]
                data["ip"] = line[24]

    return data

def base2(phone = None, surname = None, name = None, patronymic = None, ip = None, birth = None):
    data = {}

    with open("base/2.txt", "r", encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            line = [value if value != 'NULL' else '' for value in line]
            coincidences = [phone and line[4] == phone]

            if True in coincidences:
                data["address"] = line[0]

                data["surname"] = line[3]
                data["name"] = line[2]

                data["phone"] = line[4]
                data["address"] = line[5]

    return data

def base3(phone = None, surname = None, name = None, patronymic = None, ip = None, birth = None):
    data = {}

    with open("base/3.csv", "r", encoding='utf-8-sig' ) as f:
        reader = csv.reader(f, delimiter=";")
        for i, line in enumerate(reader):
            line = [value if value != 'NULL' else '' for value in line]
            coincidences = [phone and line[0] == phone]

            if True in coincidences:
                data["mail_index"] = line[9]
                data["passport"] = line[2]

                data["surname"] = line[1].split()[0]
                data["name"] = line[1].split()[1]
                data["patronymic"] = line[1].split()[2]

                data["phone"] = line[0] if line[0] and line[0][0] == '7' else ''
                data["address"] = f'{line[5]} {line[6]} Дом {line[7]} Квартира {line[8]}'

    return data

def base4(phone = None, surname = None, name = None, patronymic = None, ip = None, birth = None):
    data = {}

    with open("base/4.csv", "r", encoding='utf-8-sig' ) as f:
        reader = csv.reader(f, delimiter="\t")
        for i, line in enumerate(reader):
            line = [value if value != 'NULL' else '' for value in line]
            coincidences = [phone and '7' + line[5] == phone]

            if True in coincidences:
                data["surname"] = line[2]
                data["name"] = line[3]
                data["patronymic"] = line[4]

                data["phone"] = '7' + line[5] if line[5] else 'Неизвестно'
                data["email"] = line[1] if line[1] else line[0]

    return data

def base5(phone = None, surname = None, name = None, patronymic = None, ip = None, birth = None):
    data = {}

    with open("base/5.txt", "r", encoding='utf-8-sig' ) as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            if len(line) != 5:
                continue

            line = [value if value != 'NULL' else '' for value in line]
            coincidences = [phone and line[4] == phone]

            if True in coincidences:
                data["surname"] = line[2].split()[0]
                data["name"] = line[2].split()[1]
                data["patronymic"] = line[2].split()[2]

                data["phone"] = line[4] if line[4] else 'Неизвестно'
                data["email"] = line[3] if line[3] else 'Неизвестно'

    return data

def base6(phone = None, surname = None, name = None, patronymic = None, ip = None, birth = ''):
    data = {}

    with open("base/6.csv", "r", encoding='utf-8-sig' ) as f:
        reader = csv.reader(f, delimiter=";")
        for i, line in enumerate(reader):
            line = [value if value != 'NULL' else '' for value in line]
            line = [value.replace('\t', '') for value in line]
            coincidences = [phone and line[3] == phone, line[1] and line[0] and surname and name and patronymic and ' '.join([surname, name, patronymic]).title() == line[1] and line[0] == birth]

            if True in coincidences:
                data["surname"] = line[1].split()[0]
                data["name"] = line[1].split()[1]
                data["patronymic"] = line[1].split()[2]

                data["phone"] = line[3] if line[3] else 'Неизвестно'
                data["address"] = line[4]
                data["birth"] = line[0]

    return data

def base7(phone = None, surname = None, name = None, patronymic = None, ip = None, birth = ''):
    data = {}

    with open("base/11.csv", "r", encoding='utf-8' ) as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            line = [value if value != 'NULL' else '' for value in line]
            line = [value.replace('\t', '') for value in line]
            line[3] = line[3].split('-') if line[3] else ''

            if line[3]:
                line[3] = f'{line[3][2]}.{line[3][1]}.{line[3][0]}'

            coincidences = [phone and line[6] == phone, line[3] and surname == line[0] and name == line[1] and patronymic == line[2] and line[3] == birth]

            if True in coincidences:
                data["surname"] = line[0]
                data["name"] = line[1]
                data["patronymic"] = line[2]

                data["phone"] = line[6] if line[6] else 'Неизвестно'
                data["birth"] = line[3]
                data["email"] = line[5]

    return data

def base8(phone = None, surname = None, name = None, patronymic = None, ip = None, birth = ''):
    data = {}

    with open("base/17.csv", "r", encoding='utf-8-sig' ) as f:
        reader = csv.reader(f, delimiter=";")
        for i, line in enumerate(reader):
            line = [value if value != 'NULL' else '' for value in line]
            line = [value.replace('\t', '') for value in line]

            line[3] = line[3].replace('-', '.') if line[3] else ''

            coincidences = [phone and tools.format_number(line[0]) == phone]

            if True in coincidences:
                data["surname"] = line[2].split()[0]
                if len(line[2].split()) == 2:
                    data["name"] = line[2].split()[1]
                if len(line[2].split()) == 3:
                    data["name"] = line[2].split()[1]
                    data["patronymic"] = line[2].split()[2]

                data["phone"] = line[0] if line[0] else 'Неизвестно'
                data["birth"] = line[3]
                data["email"] = line[1]

    return data

def base9(phone = None, surname = None, name = None, patronymic = None, ip = None, birth = ''):
    data = {}

    with open("base/20.csv", "r", encoding='utf-8-sig' ) as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            if not line:
                continue
            
            line = [value if value != 'NULL' else '' for value in line]
            line = [value.replace('\t', '') for value in line]

            line[3] = line[3].replace('-', '.') if line[3] else ''
            
            coincidences = [phone and tools.format_number(line[6]) == phone]

            if True in coincidences:
                data["surname"] = line[2]
                data["name"] = line[0]
                data["patronymic"] = line[1]

                data["phone"] = line[6]
                data["birth"] = line[3]
                data["email"] = line[5]

    return data

def base10(phone = None, surname = None, name = None, patronymic = None, ip = None, birth = ''):
    data = {}

    with open("base/46.csv", "r", encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=";")
        for i, line in enumerate(reader):
            line = [value if value != 'NULL' else '' for value in line]
            line = [value.replace('\t', '') for value in line]

            if not line:
                continue
            
            coincidences = [phone and tools.format_number(line[0]) == phone]

            if True in coincidences:
                data["surname"] = line[2].split()[0]
                if len(line[2].split()) == 2:
                    data["name"] = line[2].split()[1]
                if len(line[2].split()) == 3:
                    data["name"] = line[2].split()[1]
                    data["patronymic"] = line[2].split()[2]

                data["phone"] = line[0]
                data["email"] = line[3]
                if len(line) == 7 :
                    data["address"] = f'{line[4] if line[4] else ""} {line[5] if line[5] else ""} {line[6] if line[6] else ""} {line[7] if line[7] else ""}'

    return data

def full_search(phone = None, surname = None, name = None, patronymic = None, ip = None, birth = None):
    if phone:
        phone = tools.format_number(phone)

    result = {}

    # 1 база
    inf1 = base1(phone, surname, name, patronymic, ip, birth)
    if inf1:
        result = {**result, **inf1}

    # 2 база
    inf2 = base2(phone, surname, name, patronymic, ip, birth)
    if inf2:
        result = {**result, **inf2}
    
    # 3 база
    inf3 = base3(phone, surname, name, patronymic, ip, birth)
    if inf3:
        result = {**result, **inf3}

    # 4 база
    inf4 = base4(phone, surname, name, patronymic, ip, birth)
    if inf4:
        result = {**result, **inf4}
    
    # 5 база
    inf5 = base5(phone, surname, name, patronymic, ip, birth)
    if inf5:
        result = {**result, **inf5}
    
    # 6 база
    inf6 = base6(phone, surname, name, patronymic, ip, birth)
    if inf6:
        result = {**result, **inf6}
    
    # 7 база
    inf7 = base7(phone, surname, name, patronymic, ip, birth)
    if inf7:
        result = {**result, **inf7}

    # 8 база
    inf8 = base8(phone, surname, name, patronymic, ip, birth)
    if inf8:
        result = {**result, **inf8}
    
    # 9 база
    inf9 = base9(phone, surname, name, patronymic, ip, birth)
    if inf9:
        result = {**result, **inf9}

    # 10 база
    inf10 = base10(phone, surname, name, patronymic, ip, birth)
    if inf10:
        result = {**result, **inf10}

    return result



if __name__ == "__main__":
    print(full_search("79925256844"))
    print(full_search("79262813694"))