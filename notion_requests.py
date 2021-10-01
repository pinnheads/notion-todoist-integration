import os
import requests
import datetime as dt
from handle_email import HandleEmail

# Get the week later date from now
week_later = (dt.datetime.now() + dt.timedelta(days=7)).strftime(
    "%Y-%m-%dT21:00:00Z"
)
weekly_task_query = {
    "filter": {
        "and": [{"property": "Status", "select": {"does_not_equal": "Done"}}]
    }
}


class NotionRequests(HandleEmail):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.notion.com/v1/"
        self.auth_key = f"Bearer {os.environ['NOTION_API_KEY']}"
        self.headers = {
            "Authorization": self.auth_key,
            "Content-Type": "application/json",
            "Notion-Version": "2021-08-16",
        }
        self.database_id = os.environ["NOTION_DB_ID"]

    def query_notion_db(self):
        """Query the notion task list DB for a week worth of tasks from today"""
        query_url = f"{self.base_url}databases/{self.database_id}/query"
        response = requests.post(
            url=query_url, json=weekly_task_query, headers=self.headers
        )
        response.raise_for_status()
        data = response.json()
        super().add_to_msg("[Internal] - Tasks data fetched from notion")
        return data
