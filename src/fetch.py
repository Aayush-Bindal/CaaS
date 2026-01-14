import urllib3
from environs import env
from requests import Session


def get_webkiosk_origin(intra: bool):
    if intra:
        print("Using intranet...")
        return "https://webkioskintra.thapar.edu:8443"
    return "https://webkiosk.thapar.edu"


def get_html():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    origin = get_webkiosk_origin(env.bool("USE_WEBKIOSK_INTRA", False))
    login_url = f'{origin}/CommonFiles/UserAction.jsp'
    grade_url = f'{origin}/StudentFiles/Exam/StudCGPAReport.jsp'

    payload = {
        'txtuType': 'Member Type',
        'UserType': 'S',
        'txtCode': 'Enrollment No',
        'MemberCode': env("USSR_ID"),  
        'txtPin': 'Password/Pin',
        'Password': env("PIN"),         
        'BTNSubmit': 'Submit'
    }

    headers = {
         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
         'Referer': f'{origin}/index.jsp',
         'Origin': f'{origin}'
    }

    session = Session()

    session.verify = False 

    try:
        print("Visiting homepage...")
        session.get(f'{origin}/index.jsp', headers=headers, verify=False)

        print("Attempting login...")
        response = session.post(login_url, data=payload, headers=headers, verify=False)

        print(f"Login Status: {response.status_code}")
    
        # print(response.text) # Uncomment this if you need to debug the HTML
        print("Fetching Grade Report...")

        grade_response = session.get(grade_url, headers=headers, verify=False)
    
        print(f"Grades Status: {grade_response.status_code}")
    
        if "CGPA" in grade_response.text or "Earned Credit" in grade_response.text:
            print("SUCCESS! Found Grade Data.")
            # print(grade_response.text) # Prints the HTML so you can see the table
            return grade_response.text
        else:
            print("Failed. Could not find grade table in response.")
            # print(grade_response.text) # Prints the HTML so you can see the table
            return grade_response.text

    except Exception as e:
        print(f"An error occurred: {e}")
        return None