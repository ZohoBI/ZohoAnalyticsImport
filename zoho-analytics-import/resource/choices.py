import requests
import logging
from utils.authentication import get_headers,get_headerswithOrg,analyticsMap

logger = logging.getLogger(__name__) 


def do(payload, config, plugin_config, inputs):
    
    client_id = config.get("zanalytics_connection").get("client-id", "")
    client_secret = config.get("zanalytics_connection").get("client-secret", "")
    refreshtoken = config.get("zanalytics_connection").get("refreshtoken", "")
    dc = config.get("zanalytics_connection").get("dc", "")
    
    if payload.get('parameterName') == "workspace_id":

        # Request the connections

        LIST_COLLECTIONS = analyticsMap.get(dc)+"/restapi/v2/workspaces"

        response = requests.get(LIST_COLLECTIONS, headers=get_headerswithOrg(client_id, client_secret,refreshtoken,config["org_id"],dc))

        # Build choices

        choices = []

        if response.status_code == 200:
            coll = response.json().get("data").get("ownedWorkspaces", [])
            for item in coll:
                choices += [{"value": item["workspaceId"], "label": item["workspaceName"]}]
        else:
            logger.exception("Collection could not be retrieved")

        return {"choices": choices}

    if payload.get("parameterName") == "dataset_id":
        GET_DATASETS = analyticsMap.get(dc)+"/restapi/v2/workspaces/"+config["workspace_id"]+"/views"
        response = requests.get(GET_DATASETS, headers=get_headerswithOrg(client_id, client_secret,refreshtoken,config["org_id"],dc))
        logger.exception(response.json())
        # Build choices

        choices = []

        if response.status_code == 200:
            ds = response.json().get("data").get("views", [])
            for item in ds:
                if item["viewType"] == "Table":
                    choices += [{"value": item["viewId"], "label": item["viewName"]}]

        else:
            logger.exception("Dataset could not be retrieved")

        return {"choices": choices}
    
    if payload.get("parameterName") == "org_id":
        GET_ORGS = analyticsMap.get(dc)+"/restapi/v2/orgs"
        response = requests.get(GET_ORGS, headers=get_headers(client_id, client_secret,refreshtoken,dc))
        logger.exception(response.json())
        # Build choices
        choices = []

        if response.status_code == 200:
            ds = response.json().get("data").get("orgs", [])
            for item in ds:
                if item["role"] == "Account Admin" or item["role"] == "Organization Admin" :
                    choices += [{"value": item["orgId"], "label": item["orgName"]}]

        else:
            logger.exception("Organisations could not be retrieved")
            
        return {"choices": choices}