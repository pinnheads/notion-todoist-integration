from notion_requests import NotionRequests
from handle_email import HandleEmail
import pandas as pd


class HandleNotionData(NotionRequests, HandleEmail):
    def __init__(self):
        super().__init__()
        self.task_list = []

    def format_notion_data(self):
        """
        Helper function to format and extract useful data received from Notion API
        """

        # Get task data from notion
        data = super().query_notion_db()
        # Extract task list
        tasks = data["results"]
        # Format task list and add new task in task list
        super().add_to_msg("\n\n")
        for task in tasks:
            if len(task["properties"]["Name"]["title"]) == 0:
                super().add_to_msg(
                    f"[Internal] - A empty 'name' task was found. Skiping this task. Task id - {task['id']}"
                )
                continue
            else:
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
                super().add_to_msg(
                    f"[Internal] - Task {new_task['id']} added to task list further to be added to csv file"
                )
        super().add_to_msg("\n\n")

    def add_tasks_csv(self):
        """
        Add all the tasks to a csv file
        """

        self.format_notion_data()
        # Create a dataframe
        df = pd.DataFrame(self.task_list)
        # Add the dataframe to csv
        df.to_csv("./Tasks.csv", sep=",", index=False)
        super().add_to_msg("[Internal] - Week worth of task added to the csv file...")
