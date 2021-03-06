import os
import requests
import json
import random
import uuid
import pandas as pd


class HandleProjects:
    def __init__(self):
        self.base_url = "https://api.todoist.com/rest/v1"
        self.auth_key = f"Bearer {os.environ['TODOIST_AUTH_KEY']}"
        self.project_id = ""
        self.section_names = ["Backlog", "To Do", "On-Going"]
        self.found_project = {}
        self.section_ids = {}
        self.delete_all_projects()

    def delete_all_projects(self):
        projects = requests.get(
            "https://api.todoist.com/rest/v1/projects",
            headers={"Authorization": self.auth_key},
        ).json()
        for project in projects:
            requests.delete(
                f"https://api.todoist.com/rest/v1/projects/{project['id']}",
                headers={"Authorization": self.auth_key},
            )
        print("Deleted all the Projects")
        try:
            os.remove("Data/projects.csv")
        except FileNotFoundError:
            print("File not found")
            pass
        print("Deleted projects csv file")

    def create_project(self, project_name):
        project_not_exist = self.check_project(project_name)
        if project_not_exist:
            color = random.choice(
                [
                    30,
                    31,
                    32,
                    33,
                    34,
                    35,
                    36,
                    37,
                    38,
                    39,
                    40,
                    41,
                    42,
                    43,
                    44,
                    45,
                    46,
                ]
            )
            response = requests.post(
                f"{self.base_url}/projects",
                data=json.dumps({"name": project_name, "color": color}),
                headers={
                    "Content-Type": "application/json",
                    "X-Request-Id": str(uuid.uuid4()),
                    "Authorization": self.auth_key,
                },
            ).json()
            print("Created project.")
            new_project = self.create_sections(response)
            return new_project
        else:
            print("Project already present")
            return self.found_project

    def create_sections(self, project):
        new_project = {}
        new_project["project_name"] = project["name"]
        new_project["project_id"] = project["id"]
        section_order = 0
        for section_name in self.section_names:
            response = requests.post(
                "https://api.todoist.com/rest/v1/sections",
                data=json.dumps(
                    {
                        "project_id": project["id"],
                        "name": section_name,
                        "order": section_order,
                    }
                ),
                headers={
                    "Content-Type": "application/json",
                    "X-Request-Id": str(uuid.uuid4()),
                    "Authorization": self.auth_key,
                },
            ).json()
            new_project[f"{section_name}_id"] = response["id"]
            section_order += 1

        df = pd.DataFrame([new_project])
        self.write_to_file(df)
        return df

    def write_to_file(self, project_data_frame):
        try:
            open("Data/projects.csv", "r")
        except FileNotFoundError:
            project_data_frame.to_csv("Data/projects.csv", index=False)
        else:
            project_data_frame.to_csv(
                "Data/projects.csv", mode="a+", header=False, index=False
            )

    def check_project(self, p_name):
        try:
            df = pd.read_csv("Data/projects.csv", sep=",")
        except FileNotFoundError:
            print("File not found")
            return True
        else:
            df = pd.read_csv("Data/projects.csv", sep=",")
            project = df[df["project_name"] == p_name]
            if project["project_name"].any():
                self.found_project = project
                return False
            else:
                print("not false")
                return True
