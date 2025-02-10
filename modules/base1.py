import csv

if __name__ != "__main__":
    import modules.tools as tools
else:
    import tools

def base1_by_phone(phone):
    phone = tools.format_number(phone)
    data = {}
    with open("base/налоговая 2.csv", "r") as f:
        reader = csv.reader(f, delimiter="|")
        for line in reader:
            if line and line[4] == str(phone):
                data['surname'] = line[0] if line[0] else "Неизвестно"
                data['name'] = line[1] if line[1] else "Неизвестно"
                data['patronymic'] = line[2] if line[2] else "Неизвестно"
                data['birth'] = line[3] if line[3] else "Неизвестно"
                data['phone'] = line[4] if line[4] else "Неизвестно"
                data['snils'] = line[5] if line[5] else "Неизвестно"
                data['inn'] = line[6] if line[6] else "Неизвестно"
                data['email'] = line[7] if line[7] else "Неизвестно"
                break

    return data

def base1_by_email(email):
    data = {}
    with open("base/налоговая 2.csv", "r") as f:
        reader = csv.reader(f, delimiter="|")
        for line in reader:
            if line and line[7].lower() == str(email):
                data['surname'] = line[0] if line[0] else "Неизвестно"
                data['name'] = line[1] if line[1] else "Неизвестно"
                data['patronymic'] = line[2] if line[2] else "Неизвестно"
                data['birth'] = line[3] if line[3] else "Неизвестно"
                data['phone'] = line[4] if line[4] else "Неизвестно"
                data['snils'] = line[5] if line[5] else "Неизвестно"
                data['inn'] = line[6] if line[6] else "Неизвестно"
                data['email'] = line[7] if line[7] else "Неизвестно"
                break

    return data

def base1_by_fio(name, surname, patronymic, birth):
    data = {}
    with open("base/налоговая 2.csv", "r") as f:
        reader = csv.reader(f, delimiter="|")
        for line in reader:
            if not birth:
                if line and line[0].lower() == surname and line[1].lower() == name and line[2].lower() == patronymic:
                    data['surname'] = line[0] if line[0] else "Неизвестно"
                    data['name'] = line[1] if line[1] else "Неизвестно"
                    data['patronymic'] = line[2] if line[2] else "Неизвестно"
                    data['birth'] = line[3] if line[3] else "Неизвестно"
                    data['phone'] = line[4] if line[4] else "Неизвестно"
                    data['snils'] = line[5] if line[5] else "Неизвестно"
                    data['inn'] = line[6] if line[6] else "Неизвестно"
                    data['email'] = line[7] if line[7] else "Неизвестно"
                    break
            else:
                if line and line[0].lower() == surname and line[1].lower() == name and line[2].lower() == patronymic and line[3] == birth:
                    data['surname'] = line[0] if line[0] else "Неизвестно"
                    data['name'] = line[1] if line[1] else "Неизвестно"
                    data['patronymic'] = line[2] if line[2] else "Неизвестно"
                    data['birth'] = line[3] if line[3] else "Неизвестно"
                    data['phone'] = line[4] if line[4] else "Неизвестно"
                    data['snils'] = line[5] if line[5] else "Неизвестно"
                    data['inn'] = line[6] if line[6] else "Неизвестно"
                    data['email'] = line[7] if line[7] else "Неизвестно"
                    break
    return data

if __name__ == '__main__':
    print(base1_by_phone("79776018359"))