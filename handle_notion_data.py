from notion_requests import NotionRequests
from handle_email import HandleEmail
import pandas as pd


class HandleNotionData(NotionRequests, HandleEmail):
    def __init__(self):
        super().__init__()
        self.task_list = []

    def extract_notes(self, data_list: list) -> str:
        """
        Extracts strings form the passed list
        """
        desc = ""
        for data in data_list:
            desc += data["text"]["content"]

        return desc

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
            id = task["id"]
            name = task["properties"]["Name"]["title"][0]["plain_text"]
            status = task["properties"]["Status"]["select"]
            related_to = task["properties"]["Related To"]["select"]
            priority = task["properties"]["Priority"]["select"]
            todo_on = task["properties"]["ToDo On"]["date"]
            notes = self.extract_notes(task["properties"]["Notes"]["rich_text"])
            project = task["properties"]["Project"]["select"]
            # Check if task has a 'name' value
            if len(task["properties"]["Name"]["title"]) == 0:
                super().add_to_msg(
                    f"[Internal] - A empty 'name' task was found. Skiping this task. Task id - {task['id']}"
                )
                continue
            else:
                new_task = {
                    "id": id,
                    "Name": name,
                    "Status": "" if status == None else status["name"],
                    "Related To": ""
                    if related_to == None
                    else related_to["name"],
                    "Priority": "" if priority == None else priority["name"],
                    "ToDo On": "" if todo_on == None else todo_on["start"],
                    "Notes": notes,
                    "Project": "" if project == None else project["name"],
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
        df.to_csv("./Data/Tasks.csv", sep=",", index=False)
        super().add_to_msg("[Internal] - All tasks added to the csv file...")
