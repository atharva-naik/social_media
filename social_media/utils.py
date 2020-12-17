def smart_int(string):
    string = string.replace(",","").strip()
    if 'K' in string:
        string = float(string.replace("K",""))*1e+3
    elif 'M' in string:
        string = float(string.replace("M",""))*1e+6
    elif 'B' in string:
        string = float(string.replace("B",""))*1e+9

    return int(string)