import gspread
import matplotlib.pyplot as plt
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
def gsheet(sheet_id, json_file , xaxis, yaxis):
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    docid = sheet_id
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(docid)
    sheet = spreadsheet.sheet1
    list_of_gspread = sheet.get_all_records()
    data = pd.DataFrame.from_dict(list_of_gspread)
    fig, ax = plt.subplots()
    ax.plot(data[xaxis], color='black', label='Average sales')
    #ax.yaxis.set_major_locator(data.timestamp)
    ax.legend()
    ax.set_xlabel(yaxis)
    plt.savefig('saved_figure.png')
    plt.show()

