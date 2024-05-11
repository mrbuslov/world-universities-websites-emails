from copy import deepcopy
import json
import time
import requests
import tldextract
import pyautogui
import pyperclip


def find_email_by_website_name(website: str) -> list[str]:
    '''
    Uses Snov.io api to get first couple of emails
    DEPRECATED - Snov IO bans by IP for frequent requests for a long time. Use method below (with pyautogui)
    '''
    
    # https://snov.io/email-finder
    website = f'{tldextract.extract(website).domain}.{tldextract.extract(website).suffix}'
    print(f"https://app.snov.io/api/public/search/domainCompanies?query={website}")
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


def find_email_by_website_name_with_mouse(website: str) -> list[str]:
    '''
    Uses pyautogui (your computer) with Snov IO extension to get emails. Note: it gives much more, that their website
    To get movements especially for your laptop, read README (github link)
    Install official extension to Chrome from here: https://chromewebstore.google.com/detail/email-finder-by-snovio/einnffiilpmgldkapbikhkeicohlaapj
    '''
    time.sleep(1)
    pyautogui.click(x=1689, y=120)
    time.sleep(1)
    # pyautogui.keyDown('ctrl')
    # pyautogui.keyDown('a')
    # pyautogui.keyUp('a')
    # pyautogui.keyUp('ctrl')
    
    pyautogui.write(website)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(5)
    pyautogui.click(x=3242, y=126)
    time.sleep(2)
    pyautogui.click(x=2663, y=234, button='right')
    time.sleep(1)
    pyautogui.click(x=2837, y=421)
    time.sleep(1)
    pyautogui.click(x=864, y=414)
    time.sleep(2)
    
    pyautogui.write("const elements = document.querySelectorAll('.contact-name.js-contact-email');const res = Array.from(elements).slice(0, -1).map(element => element.textContent);")
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.write("copy(res)")
    pyautogui.press('enter')
    time.sleep(0.5)
    
    pyautogui.click(x=3242, y=126)
    time.sleep(2)
    
    res = eval(pyperclip.paste().strip())
    time.sleep(0.5)
    return res


def find_n_write_emails():
    file_name = 'world_universities.json'
    universities = []
    with open(file_name, 'r') as f:
        universities = json.loads(f.read())

    count = 0
    for university in universities:
        count += 1
        print(f'Processing {count}/{len(universities)}')
        website = university['website']
        emails = find_email_by_website_name_with_mouse(website)
        print(f'website {website} emails: {emails}')
        next(uni for uni in universities if uni['website'] == website)['emails'] = emails

        with open(file_name, 'w') as f:
            f.write(json.dumps(universities, indent=4))

    
    

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
