#!/usr/bin/env python

import requests,json,sys
import matplotlib.pyplot as plt
import numpy as np
from itertools import islice

MAX_SETS_LIMIT = 100
API_URL = "https://api.warframe.market/v2/"

# takes in item_slug, returns dict of top 5 orders (from users that were online in the past 7 days)
def get_top_orders(slug:str):
    res = requests.get(API_URL + "orders/item/" + slug + "/top")
    return res.json()["data"] if res.status_code == 200 else None

def get_top_sell_orders(slug:str):
    top_orders = get_top_orders(slug)
    assert type(top_orders) == dict
    return top_orders["sell"]

# returns all orders (from users active in teh past
def get_all_items():
    res = requests.get(API_URL + "/items")
    return res.json()["data"] if res.status_code == 200 else None

def get_set_items(slug:str):
    res = requests.get(API_URL + "/item/" + slug + "/set")
    return res.json()["data"]["items"] if res.status_code == 200 else None


def save_items(save_path:str):
    with open(save_path, "w") as file:
        return file.write(json.dumps(get_all_items(), indent=4))

# get price for set when bought as parts
# returns -1 when not all parts in set are available
def get_parts_price(set):
    price = 0
    set_items = get_set_items(set["slug"])
    assert type(set_items) == list

    for item in set_items:
        # set (itself) is included is set_items
        item_sell_orders = get_top_sell_orders(item["slug"])
        if len(item_sell_orders) == 0: return -1
        if item["slug"] != set["slug"]:
            price += item_sell_orders[0]["platinum"]

    return price

if __name__=="__main__":
    items = get_all_items()
    assert type(items) == list
    sets = [item for item in items if "set" in item["slug"]]

    cnt = 0
    prices_arr = []
    # TODO: chose better names for prices and prices_arr
    for set in islice(sets, 0, len(sets)): # replace len(sets) with MAX_SETS_LIMIT
        cnt+=1
        print(f"COUNT/MAX: {cnt}/{MAX_SETS_LIMIT}")

        prices = {}
        prices["set_slug"] = set["slug"]
        set_sell_orders = get_top_sell_orders(set["slug"])
        if (len(set_sell_orders) == 0): continue
        prices["set_price"] = set_sell_orders[0]["platinum"]

        prices["parts_price"] = get_parts_price(set)
        if (prices["parts_price"] == -1): continue

        prices_arr.append(prices)

    # save prices_arr
    with open("set_prices", "w") as file:
        json.dump(prices_arr, file)


    # graph price differences
    margin_arr = [prices["parts_price"] - prices["set_price"] for prices in prices_arr]

    # ind = np.arange(len(margin_arr))
    # plt.bar(ind, margin_arr)
    # plt.show()
