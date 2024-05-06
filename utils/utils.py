import json


def find_email_by_website_name(website: str) -> list[str]:
    # https://snov.io/email-finder
    pass


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
