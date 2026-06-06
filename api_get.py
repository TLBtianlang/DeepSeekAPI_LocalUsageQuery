import requests
import json

url_cost = "https://platform.deepseek.com/api/v0/usage/cost"  # 请求网址(消耗价格)
url_amount = "https://platform.deepseek.com/api/v0/usage/amount"  # 请求网址(消耗token)

with open("GET.json", "r", encoding="utf-8") as file:
    GET = json.load(file)

def get_api(month = GET["Query"]["month"], year = GET["Query"]["year"], cookie = GET["cookie"], headers = GET["Headers"], token = GET["Auth"]["Bearer token"], save = False):
    params = {
        "month": month,
        "year": year,
    }

    cookie_str = cookie

    headers = {
        "accept": headers["accept"],
        "accept-language": headers["accept-language"],
        "authorization": token,
        "cookie": cookie_str,
        "dnt": headers["dnt"],
        "priority": headers["priority"],
        "referer": headers["referer"],
        "sec-ch-ua": headers["sec-ch-ua"],
        "sec-ch-ua-mobile": headers["sec-ch-ua-mobile"],
        "sec-ch-ua-platform": f'{headers["sec-ch-ua-platform"]}',
        "sec-fetch-dest": headers["sec-fetch-dest"],
        "sec-fetch-mode": headers["sec-fetch-mode"],
        "sec-fetch-site": headers["sec-fetch-site"],
        "user-agent": headers["user-agent"],
        "x-app-version": headers["x-app-version"],
    }  # 请求头

    response_cost = requests.get(url_cost, headers=headers, params=params)
    response_amount = requests.get(url_amount, headers=headers, params=params)

    if save:
        with open('cost.json', 'w') as f:
            f.write(response_cost.text)
            f.close()

        with open('amount.json', 'w') as f:
            f.write(response_amount.text)
            f.close()

    return response_cost, response_amount
