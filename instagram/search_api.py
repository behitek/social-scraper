import json

import requests

SEARCH_API = "https://www.instagram.com/web/search/topsearch/"
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'


def search(query, top=-1):
    headers = {
        'User-Agent': USER_AGENT,
    }
    params = {
        "context": "blended",
        "query": query,
        "rank_token": "0.983739742880634",
        "include_reel": True
    }
    r = requests.get(SEARCH_API, headers=headers, params=params)
    if r.status_code != 200:
        return []
    users = json.loads(r.text)['users']
    results = []
    for user in users:
        username = user['user']['username']
        is_verified = user['user']['is_verified']
        if is_verified:
            results.append(username)
    if top > 0:
        return results[:top]
    return results


if __name__ == '__main__':
    users = []
    for query in open('../resources/person.txt', encoding='utf8').read().splitlines():
        rs = search(query.lower())
        if len(rs) > 0:
            users.extend(rs)
        print('{} found {}'.format(query, len(rs)))
    with open('instagram_account.txt', 'w') as fp:
        for user in users:
            fp.write(user + '\n')
    print(len(users))
