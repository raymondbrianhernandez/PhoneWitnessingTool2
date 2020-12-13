#!/usr/bin/python
"""
    Web Scrapper Script.  Parses data and generate report from:
    - TruePeopleSearch.com
    - FamilySearch.org

    Raymond Hernandez
    December 8, 2020
"""

import webbrowser
import globals
import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/41.0.2228.0 "
                         "Safari/537.3"}


globals.NAME = ""
globals.AGE = ""
globals.ADDRESS = ""
globals.PHONES = ""
globals.RELATIVES = ""
globals.COUNTRY = ""
globals.NO_CAPTCHA_NEEDED = True


# def solve_captcha():
#     """
#         Re-Captcha bypass for TruePeopleSearch.com
#     """
#     site_key = "6LcMUhgUAAAAAPn2MfvqN9KYxj7KVut-oCG2oCoK"
#     captcha_url = "https://www.truepeoplesearch.com/InternalCaptcha"
#
#     driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
#     driver.get(captcha_url)
#
#     with open(r"api_key.txt", "r") as f:
#         api_key = f.read()
#
#     form = {"method": "userrecaptcha",
#             "googlekey": site_key,
#             "key": api_key,
#             "pageurl": captcha_url,
#             "json": 1}
#
#     response = requests.post('http://2captcha.com/in.php', data=form)
#     request_id = response.json()['request']
#
#     request_url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1"
#
#     status = 0
#     while not status:
#         res = requests.get(request_url)
#         if res.json()['status'] == 0:
#             time.sleep(3)
#         else:
#             requ = res.json()['request']
#             js = f'document.getElementById("g-recaptcha-response").innerHTML="{requ}";'
#             driver.execute_script(js)
#             driver.find_element_by_id("recaptcha-demo-submit").submit()


def format_number(number):
    formatted_phone = re.sub("[^0-9]", "", number)

    if not formatted_phone:
        formatted_phone = '0'

    elif formatted_phone[0] == '1':
        formatted_phone = formatted_phone[1:]

    # new_formatted_phone = formatted_phone[:3] + '-' + formatted_phone[3:6] + '-' + formatted_phone[6:10]

    return formatted_phone


def generate_report(phone_number):
    robot = "Human test, sorry for the inconvenience."
    records = "\nWe could not find any records for that search criteria."
    surname = "Try searching another last name."
    invalid = "Full phone with area code required (555-555-1234), U.S. numbers only."

    parse_truePeopleSearch(phone_number, robot, records, surname, invalid)


def parse_truePeopleSearch(phone_number, robot, records, surname, invalid):
    """
        Let's make some soup!!!
        Parsing TruePeopleSearch.com
    """
    reg_url = "https://www.truepeoplesearch.com/details?phoneno=" + phone_number + "&rid=0x0"
    req = Request(url=reg_url, headers=HEADERS)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    captcha_needed = soup.findAll(text=robot)
    no_results = soup.findAll(text=records)
    invalid_phone = soup.findAll(text=invalid)

    # Opens URL to browser just in case captcha is needed
    if captcha_needed:
        webbrowser.open_new(reg_url)
        globals.SYSTEM_MSG = "Please click the Captcha check on your browser."
        globals.NAME = ""
        globals.AGE = ""
        globals.ADDRESS = ""
        globals.PHONES = ""
        globals.RELATIVES = ""
        globals.COUNTRY = ""

    # Test if records exist
    if no_results:
        globals.SYSTEM_MSG = "No records found."
        globals.NAME = ""
        globals.AGE = ""
        globals.ADDRESS = ""
        globals.PHONES = ""
        globals.RELATIVES = ""
        globals.COUNTRY = ""

    elif not no_results and not captcha_needed:
        name = format_string(soup.find("span", {"class": "h2"}).text)
        globals.NAME = name
        name = name.split()
        first_name = name[0]
        last_name = name[-1]

        age = format_string(soup.find("span", {"class": "content-value"}).text)
        globals.AGE = age

        address = format_string(soup.find("a", {"data-link-to-more": "address"}).text)
        address = address.replace('\n', ', ')
        globals.ADDRESS = address

        phones = [phone.text for phone in soup.find_all("a", {"data-link-to-more": "phone"})]
        phones_kinds = [phones_kind.text for phones_kind in soup.find_all("span", {"class": "content-label smaller"})]
        all_phones_dict = {phones[i]: phones_kinds[i] for i in range(len(phones))}
        all_phones_list = [phones[i] + ' ' + phones_kinds[i] for i in range(len(phones))]
        globals.PHONES = ", ".join(all_phones_list)

        relatives = [relative.text for relative in soup.find_all("a", {"data-link-to-more": "relative"})]
        globals.RELATIVES = ", ".join(relatives)

        parse_familySearch(last_name, surname, phone_number)

    globals.TASK_COMPLETED = True


def parse_familySearch(last_name, surname, phone_number):
    """
        Let's make another soup!!!
        FamilySearch.org
    """
    reg_url = "https://www.familysearch.org/en/surname?surname=" + last_name
    req = Request(url=reg_url, headers=HEADERS)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    no_surname = soup.findAll(text=surname)

    if no_surname:
        country = "No information available."
        globals.COUNTRY = country
    else:
        country = format_string(soup.find("h3", {"class": "countryTitleText"}).text)
        globals.COUNTRY = country

    globals.TASK_COMPLETED = True
    globals.SYSTEM_MSG = "Search results for 1(" + phone_number[0:3] + ") " + phone_number[3:6] + '-' + phone_number[6:10]


def print_report(phone_number, first_name, last_name, age, country, address, all_phones_dict, relatives):
    """ Print all parsed data from both websites """
    print("*************************************")
    print("** GENERATED REPORT FOR", phone_number, "**")
    print("*************************************")
    print("FULL NAME:\t\t", first_name, last_name)
    print("AGE:\t\t\t", age)
    print("INFOGRAPHIC:\t " + country)
    print("ADDRESS:\t\t " + address)
    print("OTHER PHONE(S): ", all_phones_dict)
    print("RELATIVES:\t\t", relatives)


def format_string(word):
    return word.lstrip().rstrip()


def open_google_map(address):
    g_map_address = address.replace(' ', '+')
    google_map = "https://www.google.com/maps/place/" + g_map_address
    webbrowser.open_new(google_map)


""" TEST HERE """
# generate_report("8183487845")


