import csv
import json

from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import parse
from phonenumbers import geocoder
from phonenumbers import timezone
from phonenumbers import carrier


def russia_num(phone):
    num_one = None
    two_num = None

    if phone[0:1] == "+":
        num_one = phone[2:5]
        two_num = phone[5:]
    elif phone[0:1] == "8" or phone[0:1] == "7":
        num_one = phone[1:4]
        two_num = phone[4:]

    if num_one is None or two_num is None:
        return False
    
    return csv_read(num_one, two_num, phone)

def phnum_parse(phone):
    info = {
                'base': 'phonenumbers'
    }
    try:
        ph_parse = parse(phone)
    except NumberParseException:
        print('[-] Неправильный регион')
        return
    ph_timezone = timezone.time_zones_for_number(ph_parse)
    ph_region = geocoder.description_for_number(ph_parse, 'ru')
    ph_prov = carrier.name_for_number(ph_parse, 'ru')

    if ph_prov == "":
        ph_prov = "Неизвестно"
    elif ph_region == "":
        ph_region = "Неизвестно"

    info['phone'] = phone
    info['prov'] = ph_prov
    info['region'] = ph_region
    info['time_zone'] = ph_timezone[0] if ph_timezone[0] else "Неизвестно"
    info["territory"] = ph_region

    yield info

def csv_read(zone, number, phone):
    with open('base/zone.json', 'r', encoding='utf-8') as f:
        zone_t = json.load(f)

    try:
        
        for i in ["base/ABC-3xx.csv", "base/ABC-4xx.csv", "base/ABC-8xx.csv", "base/DEF-9xx.csv"]:
            info = {
                'base': i.split(".")[0]
            }
            with open(i, "r", encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="\t")
                for i, line in enumerate(reader):
                    if i != 0:
                        line_data = line[0].split(";")
                        if line_data[0] == zone and \
                                int(line_data[1]) <= int(number) <= int(line_data[2]):
                            prov = line_data[4]
                            region = line_data[5].strip()
                            territory = line_data[6]

                            time_zone = None
                            for z in zone_t:
                                if region in z:
                                    time_zone = z[region]
                                    break  # Останавливаемся, когда нашли временную зону
                            
                            info['phone'] = phone
                            info['prov'] = prov
                            info['region'] = region
                            info['time_zone'] = time_zone if time_zone else "Неизвестно"
                            info["territory"] = territory

                            yield info
    except:
        return False