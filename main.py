from github3 import GitHub
import subprocess
import json
import send_email
import os
import format
from argparse import ArgumentParser
import logging, sys
import redis
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

DESIRED_CANDIDATES_PER_EMAIL_DIGEST = 5

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('\n%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s\n')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
logger.propagate = False

def getGitHubProfiles(locations, languages):
    logger.info("Locations: {0}".format(locations))
    logger.info("Languages: {0}".format(languages))
    
    logger.info("Building query string")
    queryString = ''
    for location in locations:
        queryString = queryString + 'location:\"' + location + '\" '
        
    for language in languages:
        queryString = queryString + 'language:\"' + language + '\" '
        
    queryString = queryString + 'type:User'
    logger.info("Query String = {}".format(queryString))
    
    logger.info("Connecting to Github")
    gh = GitHub(token=os.environ['TOKEN'])
    
    logger.info("Getting a list of matching users using GitHub API")
    matchingUsers = []
    for userSearchResult in gh.search_users(queryString):
        matchingUsers.append(userSearchResult.user)
    
    logger.info("Number of matching profiles: {}".format(len(matchingUsers)))
     
    userActivityDict = {}
    
    logger.info("Use githubcontributions api to get the number of contributions for each user")
    
    # TODO: Remove the top 25 when ready
    for u in matchingUsers[:25]:
        cmd = 'curl -s https://githubcontributions.io/api/user/'+ u.login
        output = subprocess.check_output(cmd, shell=True)
        userActivityDict[u.login] = json.loads(output)['eventCount']
    
    topUsers = sorted(userActivityDict.items(), key=lambda x: x[1], reverse= True)

    logger.info("Emailing top 5 profiles not already in the cache (not already sent before)")
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    # Run the following when done debugging, to clear the chache
    # redis-cli flushall
    count = 0
    for u in topUsers:
        if count < DESIRED_CANDIDATES_PER_EMAIL_DIGEST:
            usr = gh.user(u[0])
            contributions = u[1]
            if not r.exists(usr.login):
                format.format_html(usr, contributions)
                r.set(usr.login, True)
                count = count + 1
    
    format.save_file()
    
    send_email.send()

if __name__ == '__main__':
    parser = ArgumentParser("Hook Talent Search")
    parser.add_argument("-lang", "--languages", required=True)
    parser.add_argument("-loc", "--locations", required=True)
    options = parser.parse_args()
    
    getGitHubProfiles( options.locations.split(','), options.languages.split(','))