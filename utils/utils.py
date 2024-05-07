import json
import requests


def find_email_by_website_name(website: str) -> list[str]:
    '''Uses Snov.io api to get first couple of emails'''
    # https://snov.io/email-finder
    company_data = requests.get(f"https://app.snov.io/api/public/search/domainCompanies?query={website}").json()['data']
    if not company_data:
        return []
    company_id = company_data[0]['id']
    emails_list = requests.get(f"https://app.snov.io/api/public/search/emails?id={company_id}&domain={website}").json()['data']
    if not emails_list:
        return []
    return [
        f"{em['localPart']}@{em['domain']}"
        for em in emails_list
    ]


def update_separate_jsons() -> None:
    '''
    Takes world_universities.json and splits to 
        usa_colleges.json
        usa_universities.json
    '''
    colleges_usa = []
    universities_usa = []
    universities_world = []

    with open('world_universities.json', 'r') as f:
        universities_world = json.loads(f.read())
        
    colleges_usa = [
        uni for uni in universities_world
        if (
            uni['country'] == 'United States'
            and uni['type'] == 'College'
        )
    ]
    universities_usa = [
        uni for uni in universities_world
        if (
            uni['country'] == 'United States'
            and uni['type'] != 'College'
        )
    ]
        
    with open('usa_universities.json', 'w') as f:
        f.write(json.dumps(universities_usa, indent=4))

    with open('usa_colleges.json', 'w') as f:
        f.write(json.dumps(colleges_usa, indent=4))
