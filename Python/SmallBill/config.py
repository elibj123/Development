import os


class Config(object):
    class Paths(object):
        pdf2bmp = 'F:\\Programs\\pdf2bmp\\pdf2bmp.exe'
        chrome_driver = os.path.abspath('chromedriver.exe')

    class OCR(object):
        amount_crop_bouns = [321, 591, 387, 607]
        api_key = 'a3e1022eb288957'
        api_url = 'https://api.ocr.space/parse/image'

    class AuthGtw(object):
        url = 'http://pinsker14.pythonanywhere.com/auth'
        poll_interval = 5

    class Splitwise(object):
        class URLS(object):
            request_token = "https://secure.splitwise.com/api/v3.0/get_request_token"
            get_access_token = "https://secure.splitwise.com/api/v3.0/get_access_token"
            authorize = "https://secure.splitwise.com/authorize"
            create_expense = 'https://secure.splitwise.com/api/v3.0/create_expense'

        class Creds(object):
            key = 'jtT4VojXFrSEovcm25pjRoqv8Ix1i4YH0uHTslsg'
            secret = '0qNrqNB8TIEXpo27Abl6ejDj0aJSc47PDtDwVP0V'

        pinsker_group_id = '3318232'
        tests_group_id = '3453000'