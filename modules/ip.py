import requests #подключаем библиотеку

def ip_detect(ip):
    response = requests.get( f'http://ipinfo.io/{ ip }/json' )

    try:
        user_ip = response.json()[ 'ip' ]
        user_city = response.json()[ 'city' ]
        user_region = response.json()[ 'region' ]
        user_country = response.json()[ 'country' ]
        user_location = response.json()[ 'loc' ]
        user_org = response.json()[ 'org' ]
        user_timezone = response.json()[ 'timezone' ]
        user_location = response.json()[  'loc'  ]

        return {
            'ip': user_ip,
            'city': user_city,
            'region': user_region,
            'country': user_country,
            'prov': user_org,
            'time_zone': user_timezone,
            'loc': user_location
        }
    except Exception as ex:
        return {}