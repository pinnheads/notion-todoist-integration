from notion_requests import NotionRequests
import pandas as pd


class HandleNotionData(NotionRequests):
    def __init__(self):
        super().__init__()
        self.task_list = []

    def format_notion_data(self):
        # Get task data from notion
        data = super().query_notion_db()
        # Extract task list
        tasks = data["results"]
        # Format task list and add new task in task list
        for task in tasks:
            new_task = {
                "id": task["id"],
                "Name": task["properties"]["Name"]["title"][0]["plain_text"],
                "Status": task["properties"]["Status"]["select"]["name"],
                "Related To": task["properties"]["Related To"]["select"]["name"],
                "Priority": task["properties"]["Priority"]["select"]["name"],
                "ToDo On - Start": task["properties"]["ToDo On"]["date"]["start"],
                "ToDo On - End": task["properties"]["ToDo On"]["date"]["end"],
            }
            self.task_list.append(new_task)

    def add_tasks_csv(self):
        self.format_notion_data()
        # Create a dataframe
        df = pd.DataFrame(self.task_list)
        print(df)
        # Add the dataframe to csv
        df.to_csv("./Tasks.csv", sep=",", index=False)
