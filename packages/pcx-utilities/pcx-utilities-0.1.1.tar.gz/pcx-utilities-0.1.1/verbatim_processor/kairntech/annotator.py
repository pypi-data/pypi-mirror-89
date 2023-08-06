from .client import KairntechClient
import requests
from time import sleep


class Annotator():

    def __init__(self, client: KairntechClient, project_name: str, annotator_name: str, sleep_between=0):
        self.project_name = project_name
        self.annotator_name = annotator_name
        self.client = client
        self.sleep_between = sleep_between

    def annotate(self, document: str):
        document = document.encode("utf-8")
        headers = KairntechClient.get_headers(self.client.token, "text/plain")
        r = requests.post(
            f"{self.client.api_url}projects/{self.project_name}/annotators/{self.annotator_name}/_annotate", headers=headers, data=document)
        results = []
        for c in r.json()["categories"]:
            
            if "label" in c:
                results.append(c["label"])
            else:
                results.append(c["labelName"])
        sleep(self.sleep_between)
        return results
