
def list_clearance(data_list):
    clean_list = {}
    for data in data_list:
        data = clearance(data)
        data = data.split(":")
        clean_list[data[0]]=data[1]
    return clean_list


def clearance(string):
    result = string.replace("\n", "")
    result = result.replace("  ", "")
    return result


def value_count(value):
    digit_value = float(''.join(i for i in value if i.isdigit()))
    if "k" in value:
        return (digit_value / 1000)
    else:
        return (digit_value / 100)
