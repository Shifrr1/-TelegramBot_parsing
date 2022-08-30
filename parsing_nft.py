import requests


def get_count():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://tonscan.org',
        'Connection': 'keep-alive',
        'Referer': 'https://tonscan.org/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
    }
    response_count = requests.get('https://api.ton.cat/v2/contracts/nft/EQCgzMqjoWbxXrGKZMPeqUacpXVgfHoH3CdRNiwWc1IVBfEJ', headers=headers)
    count = response_count.json()['nft_collection']['item_count']
    return get_data(count)


def get_data(count) -> dict:
    owner_data = dict()
    for set in range(0, count, 24):  # limit 24
        url = f'https://api.ton.cat/v2/contracts/nft_collection/EQCgzMqjoWbxXrGKZMPeqUacpXVgfHoH3CdRNiwWc1IVBfEJ/items?limit=24&offset={set}'
        response = requests.get(url=url)
        try:
            for i in response.json()['items']:
                owner_data[i['metadata']['name']] = i['owner_address']
        except TypeError:
            break
    # with open("index.txt", "w") as file:
    #     for i in owner_data.items():
    #         print(i, file=file)
    return owner_data
