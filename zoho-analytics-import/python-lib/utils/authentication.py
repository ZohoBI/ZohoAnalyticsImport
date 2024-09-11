import requests
import logging

logger = logging.getLogger(__name__)  

accountsMap = {
    "US":"https://accounts.zoho.com",
    "EU":"https://accounts.zoho.eu",
    "IN":"https://accounts.zoho.in",
    "AU":"https://accounts.zoho.com.au",
    "JP":"https://accounts.zoho.jp",
    "CN":"https://accounts.zoho.com.cn",
    "CA":"https://accounts.zohocloud.ca"
}

analyticsMap = {
    "US":"https://analytics.zoho.com",
    "EU":"https://analytics.zoho.eu",
    "IN":"https://analytics.zoho.in",
    "AU":"https://analytics.zoho.com.au",
    "JP":"https://analytics.zoho.jp",
    "CN":"https://analytics.zoho.com.cn",
    "CA":"https://analytics.zohocloud.ca"
}

def get_headers(client_id, client_secret, refreshToken,dc):
    data = {"refresh_token": refreshToken,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token"
    }
    response = requests.post(accountsMap.get(dc)+'/oauth/v2/token', data=data)
    #assert_response_ok(response, while_trying="retrieving access token")
    token = response.json().get("access_token")
    headers = {'Authorization': 'Zoho-oauthtoken ' + token,'Content-Type': 'application/json'}
    return headers

def get_headerswithOrg(client_id, client_secret, refreshToken,orgId,dc):
    data = {"refresh_token": refreshToken,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token"
    }
    response = requests.post(accountsMap.get(dc)+'/oauth/v2/token', data=data)
    #assert_response_ok(response, while_trying="retrieving access token")
    token = response.json().get("access_token")
    headers = {'Authorization': 'Zoho-oauthtoken ' + token,'Content-Type': 'application/json','ZANALYTICS-ORGID' : ""+orgId}
    return headers