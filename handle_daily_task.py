import requests
import os
import pandas as pd
import datetime as dt
from handle_email import HandleEmail


class HandleDailyTask(HandleEmail):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.notion.com/v1/pages/"
        self.auth_key = f"Bearer {os.environ['NOTION_API_KEY']}"
        self.headers = {
            "Authorization": self.auth_key,
            "Content-Type": "application/json",
            "Notion-Version": "2021-08-16",
        }
        self.date_today = (dt.datetime.now()).strftime("%Y-%m-%d")
        self.day_tmrw = (dt.datetime.now() + dt.timedelta(days=1)).strftime("%A")
        self.tasks = (pd.read_csv("Tasks.csv", sep=",")).to_dict(orient="records")

    def decide_tmrw(self, label):
        if label == "Daily":
            return (dt.datetime.now() + dt.timedelta(days=1)).strftime("%Y-%m-%d")
        elif label == "Daily Work Task" and self.day_tmrw == "Saturday":
            return (dt.datetime.now() + dt.timedelta(days=3)).strftime("%Y-%m-%d")
        else:
            return (dt.datetime.now() + dt.timedelta(days=1)).strftime("%Y-%m-%d")

    def format_id(self, id):
        id_list = id.split("-")
        return "".join(id_list)

    def send_patch_req(self, id, body, msg):
        patch_url = f"{self.base_url}{id}"
        response = requests.patch(url=patch_url, headers=self.headers, json=body)
        response.raise_for_status()
        super().add_to_msg(msg)

    def update_daily_tasks(self):
        for task in self.tasks:
            if (
                task["Related To"] == "Daily"
                and task["ToDo On - Start"] == self.date_today
            ):
                page_id = self.format_id(task["id"])
                tmrw = self.decide_tmrw("Daily")
                patch_property = {"properties": {"ToDo On": {"date": {"start": tmrw}}}}
                self.send_patch_req(
                    id=page_id,
                    body=patch_property,
                    msg=f"[Task] - Daily task {task['Name']} set for next day i.e {tmrw}",
                )
            elif (
                task["Related To"] == "Daily Work Task"
                and task["ToDo On - Start"] == self.date_today
            ):
                page_id = self.format_id(task["id"])
                tmrw = self.decide_tmrw("Daily Work Task")
                patch_property = {"properties": {"ToDo On": {"date": {"start": tmrw}}}}
                self.send_patch_req(
                    id=page_id,
                    body=patch_property,
                    msg=f"[Task] - Daily work task {task['Name']} set for next day i.e {tmrw}",
                )
