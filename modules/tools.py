from fake_useragent import UserAgent

def generate_useragent() -> str:
    fua = UserAgent()
    return str(fua.random)

def format_number(number: str) -> str:
    number = number.replace("-", "").replace("(", "").replace(")", "").replace(" ", "").replace("+", "")
    if number and number[0] == '8': 
        number = list(number)
        number[0] = '7'
        number = ''.join(number)

    return number