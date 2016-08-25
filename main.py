from github3 import GitHub
import subprocess
import json
from collections import OrderedDict

# Connect to Github a.k.a. login
gh = GitHub(token='73f34b63c3a3abc2e9fc85526f5e75590ad10b41')
 
# Find all users with location = Ann Arbor and Detroit, language = Python, language = Java, type = user
# 'location:"Ann Arbor" 
matchingUsers = []
for userSearchResult in gh.search_users('location:Detroit language:Python language:Java type:User'):
    matchingUsers.append(userSearchResult.user)

print len(matchingUsers)
 
userActivityDict = {}
# Use githubcontributions api to get top 100 candidates
for u in matchingUsers[:10]:
    cmd = 'curl -s https://githubcontributions.io/api/user/'+ u.login
    output = subprocess.check_output(cmd, shell=True)
    userActivityDict[u.login] = json.loads(output)['eventCount']

print userActivityDict

topUsers =  sorted(userActivityDict.items(), key=lambda x: x[1], reverse= True)

for u in topUsers:
    print gh.user(u[0]).name
    print gh.user(u[0]).login
    print gh.user(u[0]).company
    print gh.user(u[0]).html_url
    print gh.user(u[0]).location
    print gh.user(u[0]).created_at
    print "Contributions = {}".format(u[1])
    print
    