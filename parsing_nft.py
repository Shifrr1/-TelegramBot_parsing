import requests
import asyncio
import httpx


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
    return count


async def get_data(set) -> list:
    owner_data_lim = list()
    url = f'https://api.ton.cat/v2/contracts/nft_collection/EQCgzMqjoWbxXrGKZMPeqUacpXVgfHoH3CdRNiwWc1IVBfEJ/items?limit=24&offset={set}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url)
        for i in response.json()['items']:
            if i['owner_address'] is None:
                break
            else:
                owner_data_lim.append(i['owner_address'])
    return owner_data_lim


async def main() -> list:
    count = get_count()
    task_list = list()
    owner_data = list()
    for set in range(0, count, 24):  # limit 24
        tsak = asyncio.create_task(get_data(set))
        task_list.append(tsak)
    for i in await asyncio.gather(*task_list, return_exceptions=True):
        owner_data += i
    return owner_data
    # print(owner_data)


if __name__ != "__main__":
    owner_data = asyncio.run(main())
