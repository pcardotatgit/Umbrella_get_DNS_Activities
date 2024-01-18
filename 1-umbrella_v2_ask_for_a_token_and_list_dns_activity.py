# Prerequisites
# pip install requests
# pip install requests requests_oauthlib
# pip install crayons
import requests
import json
import os
import time
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
from crayons import *
import sys

method="config.txt"
token_url = 'https://management.api.umbrella.com/auth/v2/oauth2/token'
Number_of_Umbrella_requests=3

def parse_config(text_content):
    text_lines=text_content.split('\n')
    conf_result=['','','']
    for line in text_lines:
        print(green(line,bold=True))
        if 'organizationId' in line:
            words=line.split('=')
            if len(words)==2:
                conf_result[0]=line.split('=')[1].strip()
                conf_result[0]=conf_result[0].replace('"','')
                conf_result[0]=conf_result[0].replace("'","")
            else:
                conf_result[0]=""
        if 'client_id' in line:
            words=line.split('=')
            if len(words)==2:
                conf_result[1]=line.split('=')[1].strip()
                conf_result[1]=conf_result[1].replace('"','')
                conf_result[1]=conf_result[1].replace("'","")
            else:
                conf_result[1]=""  
        if 'client_secret' in line:
            words=line.split('=')
            if len(words)==2:
                conf_result[2]=line.split('=')[1].strip()
                conf_result[2]=conf_result[2].replace('"','')
                conf_result[2]=conf_result[2].replace("'","")
            else:
                conf_result[2]=""                 
    print(yellow(conf_result))
    return conf_result
    

class UmbrellaAPI:
    def __init__(self, url, ident, secret):
        self.url = url
        self.ident = ident
        self.secret = secret
        self.token = None

    def GetToken(self):
        auth = HTTPBasicAuth(self.ident, self.secret)
        client = BackendApplicationClient(client_id=self.ident)
        oauth = OAuth2Session(client=client)
        self.token = oauth.fetch_token(token_url=self.url, auth=auth)
        return self.token

def main(token_url, client_id, client_secret):
    # Get token and make an API request
    api = UmbrellaAPI(token_url, client_id, client_secret)
    token0=str(api.GetToken())
    items=(str(api.GetToken())).split(',')
    token0=(items[1].split(':'))[1]
    token0=token0.replace("'","")
    token=token0.strip()
    print(green(token,bold=True))
    print()
    print("OK let gets last DNS activity")
    print()
    headers = {'Authorization':'Bearer ' + token}

    #print (response.json())
    #print(yellow(json.dumps(response.json(),sort_keys=True,indent=4, separators=(',', ': ')),bold=True))
    # save result
    fh = open("./out/output.txt", "w")
    domain_list=[]
    domain_acces_frequency={}
    for i in range (0,Number_of_Umbrella_requests):
        offset=i*5000
        reporting_url=f'https://reports.api.umbrella.com/v2/organizations/{organizationId}/activity/dns?from=-30days&to=now&limit=5000&offset={offset}'
        print(reporting_url)
        response = requests.get(reporting_url, headers=headers)
        resp=json.dumps(response.json())
        resp_text=json.dumps(response.json(),indent=4,sort_keys=True, separators=(',', ': '))
        data=response.json()['data']
        for item in data:
            line_out=item['date']+';'+item['time']+';'+item['domain']+';'+item['internalip']+';'+item['verdict']+'\r'
            fh.write(line_out)
            if item['domain'] not in domain_list:
                domain_list.append(item['domain'])
                domain_acces_frequency[item['domain']]=1
            else:
                domain_acces_frequency[item['domain']]+=1
                
    fh.close()
    with open('./out/visited_domains.txt','w') as file:    
        #print(yellow("Visited Domains : ",bold=True))
        #print()
        for domain in domain_list:
            #print(cyan(domain,bold=True))
            file.write(domain+'\n')
    sorted_list=sorted(domain_acces_frequency.items(), key=lambda x: x[1],reverse=True)   
    with open('./out/visited_domains_popularity.txt','w') as file:   
        for item in sorted_list:
            print(item)                          
            file.write(item[0]+';'+str(item[1])+'\n')
        

if __name__=="__main__":
    global organizationId
    global client_id
    global client_secret
    if method=="config.txt":
        with open('config.txt','r') as file:
            text_content=file.read()
        organizationId,client_id,client_secret = parse_config(text_content)
    print()
    print('organizationId :',organizationId)
    print('client_id :',client_id)
    print('client_secret : ',client_secret )
    main(token_url, client_id, client_secret)
    print()
    print(green('DONE - reports are into the ./out subfolder',bold=True))
