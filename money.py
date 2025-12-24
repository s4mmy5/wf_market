#!/usr/bin/env python

import requests,json

API_URL = "https://api.warframe.market/v2/"

# takes in item_slug, returns json dict of top 5 orders (from users that were online in the past 7 days)
def get_top_orders(item_slug):
    response = requests.get(API_URL + "orders/item/" + item_slug + "/top")

    return response.json() if response.status_code == 200 else None

def get_all_items():
    response = requests.get(API_URL + "/items")
    return response.json() if response.status_code == 200 else None

def save_items(save_path):
    with open(save_path, "w") as file:
        file.write(json.dumps(get_all_items(), indent=4))


# orders_json = get_top_orders("abating_link")
# pretty_json = json.dumps(orders_json, indent=4)
# print(pretty_json)
# save_items("./items")

orders = get_top_orders("abating_link")

assert type(orders) == dict
print(orders["data"]["sell"])
