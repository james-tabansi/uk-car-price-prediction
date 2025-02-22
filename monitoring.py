import pandas as pd
from dotenv import load_dotenv
import os
from evidently.future.datasets import Dataset
from evidently.future.datasets import DataDefinition
from evidently.future.report import Report
from evidently.future.metrics import *
from evidently.future.presets import *
from evidently.future.tests import *
from evidently.ui.workspace.cloud import CloudWorkspace
load_dotenv()

class ProjectMonitor():
    def __init__(self, project_name, org_id, key):
        self.project_name = project_name
        self.org_id = org_id
        self.key = key
        self.path = r"data\Cleaned_used_cars_data.csv"
        self.ws = CloudWorkspace(token=self.key, url="https://app.evidently.cloud")

    def createNewProject(self, description):

        project_names = [projects.name for projects in self.ws.list_projects(org_id = self.org_id)]
        if self.project_name not in project_names:
            self.project = self.ws.create_project(self.project_name, org_id=self.org_id)
            self.project.description = description
            self.project.save()
            print("New Project Created")
        
        else:
            print("Project already exists")
            
    
    def getProject(self):
        for projects in self.ws.list_projects(org_id = self.org_id):
            if self.project_name in projects.name:
                project_id = projects.id
                self.project_id = project_id
                project = self.ws.get_project(project_id=project_id)
                print("Project retrieved successfully")
                return project
                break
            else:
                return "Project not found"

    def getData(self):
        data = pd.read_csv(self.path)
        data.drop('Price', axis=1, inplace=True)
        return data
    
    def createDataDefinition(self):
        data = self.getData()

        schema = DataDefinition(
            numerical_columns=data.select_dtypes(include='number').columns.tolist(),
            categorical_columns=data.select_dtypes(exclude='number').columns.tolist())
        
        return data, schema
        
    def hostProdData(self):
        data, schema = self.createDataDefinition()

        prodData = Dataset.from_pandas(pd.DataFrame(data), data_definition=schema)
        return prodData
    
    def getNewData(self, newPath):
        newDf = pd.read_csv(newPath)
        return newDf
    
    def hostNewData(self, newPath):
        _, schema = self.createDataDefinition()
        newDf = self.getNewData(newPath=newPath)
        newData = Dataset.from_pandas(pd.DataFrame(newDf), data_definition=schema)
        return newData
    
    def getReport(self, newPath):
        prodData = self.hostProdData()
        newData = self.hostNewData(newPath=newPath)
        report = Report(
            [DataSummaryPreset()],
            include_tests="True")

        my_eval = report.run(prodData, newData)

        #upload report
        self.ws.add_run(self.project_id, my_eval, include_data=True)

        return my_eval


