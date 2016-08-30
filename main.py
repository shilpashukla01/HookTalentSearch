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

DEFAULT_DESIRED_CANDIDATES_PER_EMAIL_DIGEST = 5

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('\n%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s\n')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
logger.propagate = False

def getGitHubProfiles(locations, languages, num):
    logger.info("Locations: {0}".format(locations))
    logger.info("Languages: {0}".format(languages))

    num = int(num) if num else DEFAULT_DESIRED_CANDIDATES_PER_EMAIL_DIGEST
    logger.info("Number of Profiles requested: {0}".format(num))
    
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
    
    logger.info("Using githubcontributions api to get the number of contributions for each user")
    
    # TODO: Remove the top 25 when ready
    for u in matchingUsers[:25]:
        
        cmd = 'curl -s https://githubcontributions.io/api/user/'+ u.login
        output = subprocess.check_output(cmd, shell=True)
        userActivityDict[u.login] = json.loads(output)['eventCount']

    logger.info("Sorting the profiles based on # of contributions")

    topUsers = sorted(userActivityDict.items(), key=lambda x: x[1], reverse= True)

    logger.info("Emailing top {} profiles not already in the cache (not already sent before)".format(num))
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    format.initialize(num)

    # TODO Run the following when done debugging, to clear the cache
    # redis-cli flushall
    count = 0
    for u in topUsers:
        if count < num:
            usr = gh.user(u[0])
            contributions = u[1]
            
            if not r.exists(usr.login) and (usr.company == None or 'HookLogic' not in usr.company or 'Hooklogic' not in usr.company):
                
                # Query StackExchange for User id
                cmd = 'curl -s http://data.stackexchange.com/stackoverflow/csv/670133?Name=' + usr.login
                output = subprocess.check_output(cmd, shell=True)
                user_id = ''
                user_id = output.split('\n')[1].replace('\"', '')
                stackoverflow_url = "http://stackoverflow.com/users/"+ user_id + "/" +usr.login
                format.format_html(usr, contributions, stackoverflow_url if user_id else '')
                r.set(usr.login, True)
                count = count + 1
    
    format.save_file()
    
    send_email.send()

if __name__ == '__main__':
    parser = ArgumentParser("Hook Talent Search")
    parser.add_argument("-lang", "--languages", required=True)
    parser.add_argument("-loc", "--locations", required=True)
    parser.add_argument("-num", "--numberOfProfiles", required=False)
    options = parser.parse_args()
    
    getGitHubProfiles( options.locations.split(','), options.languages.split(','), options.numberOfProfiles)