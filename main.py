from os import sep
from handle_notion_data import HandleNotionData
from todoist_requests import TodoistRequests
from handle_email import HandleEmail
import pandas as pd

# TODO - Create and manage recurring tasks

# Add week worth of tasks to csv file
hd = HandleNotionData()
hd.add_tasks_csv()

# Prepare a list of dictionaries of tasks from notion
df = pd.read_csv("./Tasks.csv", sep=",")
task_list = df.to_dict(orient="records")

# Create tasks in todoist from notion
td = TodoistRequests()
td.delete_all_tasks()
td.create_task(task_list)

# Send email with all the logs
email_handler = HandleEmail()
email_handler.send_email()
