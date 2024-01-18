# Umbrella_get_DNS_Activities

The script shared into this repo reads the 15000 last DNS activities from Umbrella V2 DNS activity and create a few text reports.

Reports are located into the **./out** subfolder this is 3 text files.

- output.txt : every DNS activities within the period in a csv format with a few column among all keys contained into the JSON result
- visited_domains.txt : List of unique visited domains
- visited_domains_popularity.txt : List of unique visited domains with the number of requests for each of them

## Required python modules

This script requires the following python modules :

- requests
- requests requests_oauthlib
- crayons

## Run the script

Before running the script edit the **config.txt** file and set the correct values for the variable it contains

organizationId=
client_id=
client_secret=

And run the script :

    python 1-umbrella_v2_ask_for_a_token_and_list_dns_activity.py
    
The result will be contained into the **./out** subfolder

## Want to collect more than the last 15000 DNS Activities

Every API Call to Umbrella backend collect 5000 Events. And by default the script send 3 successive api calls to umbrella.

This number of call is defined thru the **Number_of_Umbrella_requests** variable att the top of the script.

You can modify the value of this variable in order to collect more  Umbrella DNS Activities.

## XDR Workflow

The following XDR worflow uses the same principle as the python script. 

With an addtionnal purpose which is to check if some internal machines reqested for access to a list of risky domains you manually define.

[(W0017c) - Search DNS Activity to domain in Umbrella](https://github.com/pcardotatgit/XDR_Workflows_and_Stuffs/tree/master/500-SecureX_Workflow_examples/Workflows/XDR_Get_Umbrella_DNS_Actitivity)

