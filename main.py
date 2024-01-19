import os.path
import json
from datetime import datetime, timedelta

import requests
from retry import retry
from urllib.parse import urljoin

from configurer import get_configuration

config = get_configuration()
pandora_next_base_url = config.get('pandora_next_base_url', '')
account_file = f"./{config.get('account_file', 'account.json')}"
expire_at_fmt = "%Y-%m-%d %H:%M:%S.%f"
k_e = 'email'
k_p = 'password'
k_at = 'access_token'
k_at_ea = 'access_token_expire_at'


@retry(tries=6, delay=1, backoff=2, exceptions=(
        requests.exceptions.HTTPError,
        requests.exceptions.Timeout,
        requests.exceptions.SSLError,
        requests.exceptions.ProxyError,
        requests.exceptions.RequestException
))
def get_access_and_session_token_pandora(email, password):
    # {
    #     'access_token': 'eyJhbGciOiJ...',
    #     'expires_in': 864000,
    #     'session_token': 'eyJhbGciOvZKyxEbl...',
    #     'token_type': 'Bearer'
    # }
    url = urljoin(pandora_next_base_url, "api/auth/login")
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'username': email,
        'password': password
    }

    res = requests.post(url, headers=headers, data=data, timeout=(20, 20))
    res.raise_for_status()

    json_content = res.json()

    if (
            (session_token := json_content.get('session_token')) and
            (access_token := json_content.get('access_token')) and
            (session_token_expire_at := datetime.utcnow() + timedelta(days=90)) and
            (access_token_expire_at := datetime.utcnow() + timedelta(seconds=json_content.get('expires_in'))) and
            len(session_token) > 0 and
            len(access_token) > 0  # noqa
    ):
        return session_token, access_token, session_token_expire_at, access_token_expire_at  # noqa
    else:
        print(f'Fetch failed. json_content:')
        print(json_content)

    return None, None, None, None


def is_valid_json(file_path):
    try:
        with open(file_path, 'r') as file:
            json.load(file)
        return True
    except json.JSONDecodeError:
        return False


def refresh():
    # 1. check account.json file existing
    # 2. check account.json content is valid or not
    # 3. loop it and use PandoraNext to get access token
    # 4. cron job
    if os.path.exists(account_file):
        if is_valid_json(account_file):
            with open(account_file, 'r') as rFile:
                data = json.load(rFile)
                update_count = 0
                if isinstance(data, list):
                    for index, item in enumerate(data):
                        if k_e not in item or k_p not in item:
                            print("email and password are required")
                            exit(-1)

                        email = item[k_e]
                        password = item[k_p]
                        access_token_expire_at = item[k_at_ea] if k_at_ea in item else None
                        if access_token_expire_at is not None:
                            is_expired = datetime.strptime(access_token_expire_at, expire_at_fmt) < datetime.now()
                        else:
                            is_expired = True

                        if is_expired:
                            session_token, access_token, session_token_expire_at, access_token_expire_at = \
                                get_access_and_session_token_pandora(email, password)
                            obj = {
                                k_e: email,
                                k_p: password,
                                k_at: access_token,
                                k_at_ea: access_token_expire_at.strftime(expire_at_fmt)
                            }
                            data[index] = obj
                            print(f"updated {email}")
                            update_count = update_count + 1

                    if update_count > 0:
                        print(f'updated {update_count} account')
                        with open(account_file, 'w') as wFile:
                            json.dump(data, wFile, indent=2)
                            wFile.close()
                    else:
                        print('No changes')

                    rFile.close()
    else:
        print("No account.json file found")
        exit(-1)


if __name__ == '__main__':
    refresh()
