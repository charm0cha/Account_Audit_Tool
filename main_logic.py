import http.client
import requests
import json
import os 
from dotenv import find_dotenv, load_dotenv
import time 
from datetime import datetime, timezone, timedelta


load_dotenv(find_dotenv())

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
AUDIENCE = f"https://{AUTH0_DOMAIN}/api/v2/"



def get_management_token():
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET, 
        "audience": AUDIENCE,
        "grant_type":"client_credentials"
        }
    
    headers = { 'content-type': "application/json", "accept" : "application/json" }

    r = requests.post(url, json=payload, headers=headers, timeout=30)

    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(f"Auth0 token request failed: {r.status_code} {r.text}")
    data = r.json()
    if "access_token" not in data:
        raise RuntimeError(f"No access_token in response: {data}")

    return data["access_token"]


# to test token retrevial 
if __name__ == "__main__":
    token_test = get_management_token()
    print(token_test)


def get_static_users():
    token = get_management_token()
    url = f"{AUDIENCE}users"

    headers = { 
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
        }
    params = {
        "q": (
            'identities.connection:"Username-Password-Authentication" AND ('
            'email:*@jcdecaux.com OR '
            'email:*@afadecaux.dk OR '
            'email:*@igpdecaux.it OR '
            'email:*@walldecaux.de OR '
            'email:*@dunnhumby.com OR '
            'email:*@gewista.at'
            ')'
        ),    
        "fields" : "email,created_at",
        "include_fields" : "true",
        "search_engine" : "v3",
        "per_page": 50,
        "page": 0
            }

    response = requests.get(url, headers=headers, params=params, timeout=30)

    if response.status_code != 200:
        print(f"[ERROR] /users returned {resp.status_code}")
        print(resp.text)
        raise SystemExit(1)
    
    data = response.json()

    return data

# # test if list of users + created at date prints
# # def main():
# #     users = get_static_users()
# #     print(users)
# # if __name__ == "__main__":
# #     main()




def get_expired_accounts():
    maximum_days = 30
    users = get_static_users()
    now = datetime.now(timezone.utc) #current utc time 

    expired = [ ]
    found = 0
    for user in users:
        user_creation_date = user.get("created_at")
        if not user_creation_date:
            continue     #skip if user has no created_at field

        created_at = datetime.fromisoformat(user_creation_date.replace("Z", "+00:00")) #format created_at
        acc_age_days = (now - created_at).days     #calc how many days acc is 

        if acc_age_days > maximum_days: 
            found += 1
            print(f"{user.get('email')} created {acc_age_days} days ago on {created_at}.")
        

            # expired.append(user)
            # return expired
    print(found)
    if found == 0:
        print(f"No accounts older than {maximum_days} days found")     


if __name__ == "__main__":
    get_expired_accounts()
        

# tue:
# go through .get / os for secrets + then rotate 
# push to github 
# loop though pages until no result

# wednesday 
# add exception of if second account link - do not delete 

# thursday
# guardrails - dry run=true / print accounts for disable
# option to diable if created_at older than N days


# friday
# protect some domains (app_metadata.role in "admin", "support")
# app_metadata.disable_reason before blocking for auditability

# saturday
# logging & database stuff 






