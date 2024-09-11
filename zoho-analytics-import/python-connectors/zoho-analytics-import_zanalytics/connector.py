import json
import requests
import logging
import pandas as pd
from dataiku.connector import Connector
from utils.authentication import get_headers,get_headerswithOrg,analyticsMap

logger = logging.getLogger(__name__) 


class MyConnector(Connector):

    EMPTY_CONNECTION = { "client-id": None, "client-secret": None,"refreshtoken":None}
    
    def __init__(self, config, plugin_config):

        Connector.__init__(self, config, plugin_config) 

        # Retrieve credentials and token
    
        self.client_id = config.get("zanalytics_connection").get("client-id", "")
        if not self.client_id:
            raise ValueError("Zoho Analytics account is necessary to fetch the data. Please provide a Client Id.")

        self.client_secret = config.get("zanalytics_connection").get("client-secret", "")
        if not self.client_secret:
            raise ValueError("Zoho Analytics account is necessary to fetch the data. Please provide a Client Secret.")
            
        self.refreshtoken = config.get("zanalytics_connection").get("refreshtoken", "")
        if not self.refreshtoken:
            raise ValueError("Zoho Analytics account is necessary to fetch the data. Please provide a Refresh Token.")
        
        self.orgId = config.get("org_id","")
        if not self.orgId:
            raise ValueError("Choosing a Organization is necessary to fetch the data. Please provide one in the Organization field.")
        
        self.dc = config.get("zanalytics_connection").get("dc", "")
        if not self.dc:
            raise ValueError("Choosing a DC is necessary to fetch the data. Please provide one in the DC field.")
        
        self.headers = get_headerswithOrg(self.client_id, self.client_secret,self.refreshtoken,self.orgId,self.dc)

        # Retrieve ids of collection and dataset

        self.workspace_id = config.get("workspace_id", "")
        if not self.workspace_id:
            raise ValueError("Choosing a collection is necessary to fetch the data. Please provide one in the collection field.")

        self.dataset_id = config.get("dataset_id", "")
        if not self.client_secret:
            raise ValueError("Choosing a dataset is necessary to fetch the data. Please provide one in the collection field.")

    def get_read_schema(self):

        # We don't specify a schema here, so DSS will infer the schema
        # from the columns actually returned by the generate_rows method

        return None

    def generate_rows(self, dataset_schema=None, dataset_partitioning=None, partition_id=None, records_limit=-1):

        url_asset = analyticsMap.get(self.dc)+"/restapi/v2/workspaces/"+self.workspace_id+"/views/"+self.dataset_id+"/data" 
        payload = {}
        payload["CONFIG"]=json.dumps({"responseFormat":"json"})
        response = requests.get(url_asset, headers=self.headers,params=payload)
        status_code = response.status_code
        logger.info("Response status code : {}".format(status_code))

        if status_code == 504:
            raise Exception("Timeout error. Known issue - Zoho Analytics is working on that!")

        # Other errors
        if status_code >= 400:
            logger.info(response.json())
            raise Exception("Unknown error. Status code: {}!".format(status_code))

        content = response.json()
        logger.info(content)
        # If no asset, abort it

        nb_assets = len(content.get("data", []))

        if(nb_assets == 0):
            raise ValueError("No asset. Please contact Zoho Analytics for access to data.")

        else:
            logger.info("Received {} assets".format(nb_assets))

        # Generate dataframe

        df = pd.DataFrame(content.get("data", []))

        # Yield results

        for record in df.iterrows():
            yield dict(record[1])

    def get_writer(self, dataset_schema=None, dataset_partitioning=None, partition_id=None):
        raise Exception("Unimplemented")

    def get_partitioning(self):
        raise Exception("Unimplemented")

    def list_partitions(self, partitioning):
        return []

    def partition_exists(self, partitioning, partition_id):
        raise Exception("unimplemented")

    def get_records_count(self, partitioning=None, partition_id=None):
        raise Exception("unimplemented")
