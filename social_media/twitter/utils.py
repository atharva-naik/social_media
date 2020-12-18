"""
TO BE DELETED
"""

def get_attribute_rec(div, attr):
    attr += '='
    inner_html = div.get_attribute('innerHTML')
    match_index = inner_html.find(attr)
    # print(match_index)
    end_index = inner_html[match_index+len(attr)+1 : ].find('"')
    attr_val = inner_html[match_index+len(attr)+1 : match_index+len(attr)+1+end_index]
    # print(end_index)

    return attr_val