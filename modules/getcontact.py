import csv
import ast

if __name__ != "__main__":
    import modules.tools as tools
else:
    import tools

def get_contact(phone):
    data = {}

    if not phone:
        return
    else:
        phone = tools.format_number(phone)

    with open("base/getcontact_numbuster.141K.csv", "r", encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=";")
        for i, line in enumerate(reader):
            if line and i == 0:
                continue

            line = [value if value != 'NULL' else '[]' for value in line]

            try:
                line[1] = ast.literal_eval(line[1])
                line[2] = ast.literal_eval(line[2])
            except:
                continue
            
            if len(line) > 1:
                line[1] = line[1][:5]
            if len(line) > 2:
                line[2] = line[2][:5]

            line[1] = line[1] + line[2]
            line.pop(2)

            if line[0] == str(phone):
                data['phone'] = line[0] if line[0] else ""
                data['tags'] = line[1] if line[1] else []
                break
    
    return data

if __name__ == '__main__':
    print(get_contact('79649350646'))