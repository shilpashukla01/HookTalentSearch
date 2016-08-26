from github3 import GitHub
import subprocess
import json
import send_email
import os

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
for u in matchingUsers:
    cmd = 'curl -s https://githubcontributions.io/api/user/'+ u.login
    output = subprocess.check_output(cmd, shell=True)
    userActivityDict[u.login] = json.loads(output)['eventCount']

topUsers = sorted(userActivityDict.items(), key=lambda x: x[1], reverse= True)

f = open('file.txt','w')

print "Sending information of top 10 matching profiles..."

# TODO check if the top 10 of topUsers are already in cache, if yes check next 20 and so on
# Send the ones that are not already in the cache (not already sent before)
for u in topUsers[:10]:
    f.write("Name: {}\n".format(gh.user(u[0]).name))
    f.write("Login: {}\n".format(gh.user(u[0]).login))
    f.write("Company: {}\n".format(gh.user(u[0]).company))
    f.write("Profile URL: {}\n".format(gh.user(u[0]).html_url))
    f.write("City: {}\n".format(gh.user(u[0]).location))
    f.write("GitHub user since: {}\n".format(gh.user(u[0]).created_at.date()))
    f.write("Contributions: {}\n\n".format(u[1]))

    #TODO Add LinkedIn profile URL if possible
f.close()

send_email.send()