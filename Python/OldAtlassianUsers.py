import csv
import datetime
from math import floor

curr = datetime.datetime.now()
halfyear = datetime.timedelta(days=180)

users = {}

def getDate(csvdate):
    dateformat= "%d %b %Y"
    if csvdate == "Never accessed":
        return None
    else:
        return datetime.datetime.strptime(csvdate,dateformat)
    
def getLastAccessed(row, date1):
    key = str(row["email"])
    diff1 = curr - date1
    
    if key not in users:
        users[key] = diff1

    if users[key] > diff1:
        users[key] = diff1
    elif users[key] < diff1:
        pass

def getUsers(row):
        
    lastSeenJiraService  = row["Last seen in Jira Service Management - tmconnected"]
    lastSeenJiraSoftware = row["Last seen in Jira Software - tmconnected"]
    lastSeenConfluence   = row["Last seen in Confluence - tmconnected"]
    
    dateJiraService  = getDate(lastSeenJiraService)
    dateJiraSoftware = getDate(lastSeenJiraSoftware)
    dateConfluence   = getDate(lastSeenConfluence)
    
    if dateJiraService is not None:
        getLastAccessed(row, dateJiraService)
            
    if dateJiraSoftware is not None:
        getLastAccessed(row, dateJiraSoftware)
    
    if dateConfluence is not None:
        getLastAccessed(row, dateConfluence)
    
try:
    with open("export-users.csv", encoding="utf8") as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            if row["User status"] == "Active":
                getUsers(row)
            
        with open("old-users.csv", "w", newline="", encoding="utf8") as exportfile:
            fieldnames = ['Email', 'Last seen']
            writer = csv.DictWriter(exportfile, fieldnames=fieldnames)
            writer.writeheader()
            for key,val in users.items():
                if val > halfyear:
                    print(f"{floor(val.total_seconds()/(3600*24))} : {key}")
                    writer.writerow({'Email': key, 'Last seen': floor(val.total_seconds()/(3600*24))})
except FileNotFoundError as err:
    print("File not found:", err.filename)
    print("Download User export (csv) from Atlassian and paste it in same directory")
