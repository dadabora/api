
import json
import requests
from pprint import pprint

nickname = input('User Nickname: ')

main_link = f'https://api.github.com/users/{nickname}/repos'
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    'Authorization':'Basic cG9zdG1hbjpwYXNzd29yZA=='}
response = requests.get(main_link)
user_data = response.json()
with open('repos.json', 'w') as file_repo: json.dump(user_data, file_repo)

user_data1 = []
for i in user_data: user_data1.append(i['name'])
repos = {nickname:user_data1}
print(repos)

rep = f'{nickname}_repo.json'
with open(rep, 'w') as f:
    json.dump(user_data1, f)