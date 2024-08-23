import random
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
SAMPLE_SPREADSHEET_ID = '1la2Myn0VCSWVVb3eX4CNBrCJBxvuCxiG-R6t3ksWgLQ'
SAMPLE_RANGE_NAME = 'Лист1'
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

def yacheika(x):
    y = ''
    if x == 'Понедельник':
        y = random.choice((['B', 'C', 'D', 'E', 'F']))
    if x == 'Вторник':
        y = random.choice((['G', 'H', 'I', 'J', 'K']))
    if x == 'Среда':
        y = random.choice((['L', 'M', 'N', 'O', 'P']))
    if x == 'Четверг':
        y = random.choice((['G', 'R', 'S', 'T', 'U']))
    if x == 'Пятница':
        y = random.choice((['V', 'W', 'X', 'Y', 'Z']))
    if x == 'Суббота':
        y = random.choice((['AA', 'AB', 'AC', 'AD', 'AE']))
    if x == 'Воскресенье':
        y = random.choice((['AF', 'AG', 'AH', 'AI', 'AJ']))
    return y
        
def yacheika2(y):
    return str(y - 3)

def zapis(x, y, z):
    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range='Лист1!' + str(yacheika(x) + yacheika2(y)), valueInputOption="USER_ENTERED", body={"values":[[z]]}).execute()



