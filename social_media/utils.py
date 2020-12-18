import os
import re
import time 
import string
import requests
import subprocess

def smart_int(string):
    string = string.replace(",","").strip()
    if 'K' in string:
        string = float(string.replace("K",""))*1e+3
    elif 'M' in string:
        string = float(string.replace("M",""))*1e+6
    elif 'B' in string:
        string = float(string.replace("B",""))*1e+9

    return int(string)

def camel_case_split(str): 
    words = [[str[0]]] 
  
    for c in str[1:]: 
        if (words[-1][-1].islower() and c.isupper()) or (words[-1][-1].islower() and c.isdigit()): 
            words.append(list(c)) 
        else: 
            words[-1].append(c) 
  
    return [''.join(word) for word in words] 

# eg template: "<TEXT> by <TEXT> <INT> <TEXT> ago <INT> <TEXT> <INT> <TEXT> <INT> views"
def split_by_template(text, template):
    separators = template.replace("<TEXT>", "").replace("<INT>", "").strip().split()
    curr_txt = copy.deepcopy(text)
    curr_tmp = copy.deepcopy(template)
    res = []
    
    for separator in separators:
        txt = curr_txt.split(separator)[0].strip()
        tmp = curr_tmp.split(separator)[0].strip()

        integers = []
        for i in range(tmp.count('<INT>')):
            integers.append(int(re.findall(r"([0-9]+)", txt)[i].strip()))
        txt = re.sub(r"([0-9]+)", "<INT>", txt).strip().split("<INT>")
        texts = [item.strip() for item in txt if item is not '']
        
        int_ctr=0
        text_ctr=0
        for temp in tmp.split():
            if temp == '<TEXT>':
                res.append(texts[text_ctr])
                text_ctr += 1
            elif temp == '<INT>':
                res.append(integers[int_ctr])
                int_ctr += 1
        #         print(tmp)
        curr_txt = curr_txt.split(separator)[-1].strip()
        curr_tmp = curr_tmp.split(separator)[-1].strip()
    
    return res

def format_time(time_str):
    if time_str.count(':') == 1:
        time_str = '00:'+time_str
    return time_str

def get_attribute_rec(div, attr):
    attr += '='
    inner_html = div.get_attribute('innerHTML')
    match_index = inner_html.find(attr)
    # print(match_index)
    end_index = inner_html[match_index+len(attr)+1 : ].find('"')
    attr_val = inner_html[match_index+len(attr)+1 : match_index+len(attr)+1+end_index]
    # print(end_index)

    return attr_val

# def install_tiv(test_url="https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png"):
#     open("test.png","wb").write(requests.get(test_url).content)
#     try:
#         subprocess.run(['tiv', "test.png"])
#     except NotADirectoryError:
#         print("Installing tiv ...")
#         os.system("git clone https://github.com/stefanhaustein/TerminalImageViewer.git")
#         os.system("cd TerminalImageViewer/src/main/cpp")
#         os.system("make")
#         os.system("sudo make install")

def install_tiv():
    print("Installing tiv ...")
    os.system("git clone https://github.com/stefanhaustein/TerminalImageViewer.git")
    os.system("cd TerminalImageViewer/src/main/cpp")
    os.system("make")
    os.system("sudo make install")