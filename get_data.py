import requests
import user

USER_ID = user.USER_ID
AUTH_KEY = user.AUTH_KEY

INFO_URL = f"https://www.duolingo.com/2017-06-30/users/{USER_ID}"
WORDS_URL = f"https://www.duolingo.com/2017-06-30/users/{USER_ID}/courses/fr/en/learned-lexemes"
COUNT_URL = f"{WORDS_URL}/count"
COOKIES = "lang=en; wuuid=273c6c7e-6723-4e2e-b8c9-71c5e837b253; lu=https://www.duolingo.com/; initial_referrer=$direct; lp=splash; lr=; csrf_token=IjhiNjU3YTUwYWMzMTRkYjI4ODcyNDkzNWMzYjI5NTJjIg==; logged_out_uuid=320191491; logged_in=true; FCCDCF=%5Bnull%2Cnull%2Cnull%2C%5B%22CQNIGUAQNIGUAEsACBENBdFoAP_gAEPgACiQINJD7C7FbSFCwH5zaLsAMAhHRsAAQoQAAASBAmABQAKQIAQCgkAYFASgBAACAAAAICRBIQIECAAAAUAAQAAAAAAEAAAAAAAIIAAAgAEAAAAIAAACAIAAEAAIAAAAEAAAmAgAAIIACAAAgAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAQNVSD2F2K2kKFkPCmwXYAYBCujYAAhQgAAAkCBMACgAUgQAgFJIAgCIFAAAAAAAAAQEiCQAAQABAAAIACgAAAAAAIAAAAAAAQQAABAAIAAAAAAAAEAQAAIAAQAAAAIAABEhAAAQQAEAAAAAAAQAAA%22%2C%222~70.89.93.108.122.149.184.196.236.259.311.313.323.358.415.442.486.494.495.540.574.609.864.981.1029.1048.1051.1095.1097.1126.1205.1276.1301.1365.1415.1449.1514.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958.1960.2072.2253.2299.2373.2415.2506.2526.2531.2568.2571.2575.2624.2677.2778~dv.%22%2C%227047A3AF-1069-4A05-94BF-5393E04B170C%22%5D%5D; __gads=ID=fe99e1cefa737d24:T=1740046083:RT=1740047071:S=ALNI_Mb6AIOmw8h7qG3B93TITSAEhz3wvA; __gpi=UID=0000103a7c6efe7a:T=1740046083:RT=1740047071:S=ALNI_MZZAV0b1VZDrGAjKHmQ6golqKWw-g; __eoi=ID=fd7462d9d7b3ec62:T=1740046083:RT=1740047071:S=AA-AfjYmsdavrvTOsz6kjU0pcCou; FCNEC=%5B%5B%22AKsRol8k_6PPCnz4DPxwES5lr_vEBKyKqju3wB47Ik9FVVxgEWTEh76v4FrHJ7HRuqZV6hLGWZ8oi6UqV-yowNfkQ2DBZv3uLBi23xAHHrnHUD14ykCt15zDDMgN-lGyalqYDtKA23LjIDDCwd2EeDqx1zHisq3T9w%3D%3D%22%5D%5D; AWSALB=4lxQGPzr6uIOufK7h1k+DMmeE1usX4Mtuke9sQsXhb4J129LvXcr1Sp1bXzao+xcMkulkMrA6WNzOpLXJuMppc8g5KoKOMMG6XnxN3OHhA/mPGQKbWuU8ZnvrrEQ; AWSALBCORS=4lxQGPzr6uIOufK7h1k+DMmeE1usX4Mtuke9sQsXhb4J129LvXcr1Sp1bXzao+xcMkulkMrA6WNzOpLXJuMppc8g5KoKOMMG6XnxN3OHhA/mPGQKbWuU8ZnvrrEQ; jwt_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjYzMDcyMDAwMDAsImlhdCI6MCwic3ViIjozMjAxOTE0OTF9.dCg7mkdG-u6iUin0Qebn8mT9dl5jfU_Jxl5fM4iY4Y0; tsl=1740048230940; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Feb+20+2025+11%3A43%3A51+GMT%2B0100+(czas+%C5%9Brodkowoeuropejski+standardowy)&version=202404.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=1c77d9b4-da13-48bb-be71-7a50c5ecee9b&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&AwaitingReconsent=false"

HEADERS = {
        "Authorization": f"Bearer {AUTH_KEY}",
        "Accept": "application/json; charset=UTF-8",
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Cookie": f"{COOKIES}"
    }

def get_clean_word_list(json):
    with open("word_list.txt", "w") as word_list:
        for lexeme in json['learnedLexemes']:
            word = lexeme['text']
            translations = lexeme['translations']
            word_list.write(f"French word: {word}, English translations: {', '.join(translations)}\n")


def get_skills():    
    params = {
        "fields": "currentCourse",
        "_": "1740166617569"
    }

    response = requests.get(INFO_URL, headers=HEADERS, params=params)

    if response.status_code == 200:
        data = response.json()
        print("GET request succeeded")
        # print(data['currentCourse']['pathSectioned'][0])#.keys())

        skill_ids = []

        for i, section in enumerate(data['currentCourse']['pathSectioned']):
            completed_units = section['completedUnits']
            total_units = section['totalUnits']
            if completed_units > 0:
                print(f"Section {i}, completed units - {completed_units}")

            for unit in range(total_units if total_units == completed_units else completed_units + 1):
                for level in section['units'][unit]['levels']:
                    if level['state'] in ('active', 'passed', 'legendary'):
                        finished_sessions = level['finishedSessions']
                        client_data = level.get('pathLevelClientData', {})
                        if 'skillId' in client_data:
                            skill_ids.append((finished_sessions, client_data['skillId']))
        
        skill_ids_unique = list(dict.fromkeys(skill_ids))
        print(f"Skill IDs count: {len(skill_ids_unique)}")
        return skill_ids_unique
    else:
        print(f"GET request failed with status code {response.status_code}")
        print(response)

def create_progressed_skills(skills):
    return [ 
        {
            "finishedLevels": 1,
            "finishedSessions": finished_sessions,
            "skillId": {"id": skill_id}
        }
        for (finished_sessions, skill_id) in skills
    ]

def get_lexeme_count():
    payload = {
        "progressedSkills": create_progressed_skills(get_skills())
    }

    response = requests.post(COUNT_URL, headers=HEADERS, params={}, json=payload)
    
    if response.status_code == 200:
        print("POST request succeeded")
        lexeme_count = response.json()['lexemeCount']
        print(lexeme_count)
        return lexeme_count
    else:
        print(f"POST request failed with status code {response.status_code}")
        print(response.text)

def update():
    params = {
        "limit": 1000,
        "sortBy": "LEARNED_DATE",
        "startIndex": 0
    }

    payload = {
        "lastTotalLexemeCount": get_lexeme_count(),
        "progressedSkills": create_progressed_skills(get_skills()) # dont call twice! already done in prev step
    }

    response = requests.post(WORDS_URL, headers=HEADERS, params=params, json=payload)

    if response.status_code == 200:
        print("Success!")
        word_list = get_clean_word_list(response.json())
        print(word_list)
        # + save to a file
    else:
        print(f"POST request failed with status code {response.status_code}")
        print(response.text)
    
if __name__ == "__main__":
    update()