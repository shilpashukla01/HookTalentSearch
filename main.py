from github3 import GitHub
import subprocess
import json
import send_email
import os
import format

# Connect to Github a.k.a. login
gh = GitHub(token=os.environ['TOKEN'])

# TODO take locations and languages as input from user and then construct the querystring by parsing those parameters

# Find all users with location = Ann Arbor or Detroit, language = Python or Java, type = User
matchingUsers = []
for userSearchResult in gh.search_users('location:Detroit location:"Ann Arbor" language:Python language:Java type:User'):
    matchingUsers.append(userSearchResult.user)

print "Number of matching profiles: %s" % len(matchingUsers)
 
userActivityDict = {}

# Use githubcontributions api to get the number of contributions for each user
for u in matchingUsers[:5]:
    cmd = 'curl -s https://githubcontributions.io/api/user/'+ u.login
    output = subprocess.check_output(cmd, shell=True)
    userActivityDict[u.login] = json.loads(output)['eventCount']

topUsers = sorted(userActivityDict.items(), key=lambda x: x[1], reverse= True)

print "Sending information of top 5 matching profiles..."

# TODO check if the top 5 of topUsers are already in cache, if yes check next 20 and so on
# Send the ones that are not already in the cache (not already sent before)

for u in topUsers:
    usr = gh.user(u[0])
    contributions = u[1]
    format.format_html(usr, contributions)

format.save_file()

send_email.send()
