from os import sep
from handle_notion_data import HandleNotionData
from handle_daily_task import HandleDailyTask
from todoist_requests import TodoistRequests
from handle_email import HandleEmail
import pandas as pd

hd = HandleNotionData()
email_handler = HandleEmail()
td = TodoistRequests()
daily_task = HandleDailyTask()

# Add week worth of tasks to csv file
hd.add_tasks_csv()

# Prepare a list of dictionaries of tasks from notion
df = pd.read_csv("./Tasks.csv", sep=",")
task_list = df.to_dict(orient="records")

# Create tasks in todoist from notion
td.delete_all_tasks()
td.create_task(task_list)

# Update daily task for next day
email_handler.add_to_msg("\n\n")
daily_task.update_daily_tasks()

# Send email with all the logs
email_handler.send_email()
