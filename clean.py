import pandas as pd


def list_clearance(data_list):
    clean_list = {}
    for data in data_list:
        data = clearance(data)
        data = data.split(":")
        clean_list[data[0]] = data[1]
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


# Cleaning mistakes, it could be done earlier
def clean_after_parse(df):
    df["Name"] = df["Name"].str[:-1]
    df["Club"] = df["Club"].str[:-1]
    df["National player"] = df["National player"].str[:-1]
    df["Current international"] = df["Current international"].str[:-1]
    df["Agent"] = df["Agent"].str[:-1]
    df["Height"] = df["Height"].str[:-2]
    df["Height"] = df["Height"].str.replace(",", ".")
    return (df)
