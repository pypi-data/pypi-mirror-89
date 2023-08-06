import requests
import jsons
from .responses import *

class IbpmClient:

    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.apiUrl = baseUrl + '/api/ext/'
        self.authorizationToken = ""
        self.userName = ""

    def _req(self, method, **kwargs):
        data = {
            "authenticationToken": self.authorizationToken,
            "userName": self.userName
        }
        
        for k,v in kwargs.items():
            if v != None:
                data[k]=v
        
        resp = requests.post(self.apiUrl + method, json = data)
        return resp.json()


    def createNewProcess(self, model, variables, startObject=None) -> createNewProcessResponse:
        resp = self._req("createNewProcess", model=model, variables=variables, startObject=startObject)
        return jsons.load(resp, createNewProcessResponse)

    def execTask(self, model=None, documentName=None, instanceId=None, activity=None, comments=None) -> ibpmResponse:
        resp = self._req("execTask", documentName=documentName, instanceId=instanceId, activity=activity, comments=comments)
        return jsons.load(resp, ibpmResponse)

    def updateProcess(self, model=None, documentName=None, instanceId=None, variables=None, resetGroups=None, state=None) -> ibpmResponse:
        resp = self._req("updateProcess", documentName=documentName, instanceId=instanceId, variables=variables, resetGroups=resetGroups, state=state)
        return jsons.load(resp, ibpmResponse)

        
