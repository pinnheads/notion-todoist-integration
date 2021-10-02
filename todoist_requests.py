import requests
import os
from handle_projects import HandleProjects
from handle_email import HandleEmail

# Dictionary of todoist label ids that can be assigned
label_ids = {
    "Personal": 2157991715,
    "Work": 2157991720,
    "College": 2157991727,
    "Personal Growth": 2157991879,
    "Daily": 2157998666,
    "Daily Work Task": 2157998668,
}


class TodoistRequests(HandleEmail):
    def __init__(self):
        super().__init__()
        self.handle_project = HandleProjects()
        self.base_url = "https://api.todoist.com/rest/v1"
        self.auth_key = f"Bearer {os.environ['TODOIST_AUTH_KEY']}"
        self.headers = {"Authorization": self.auth_key}

    def assign_label_ids(self, label):
        """
        Helper function to assign label id based on 'Related to' tab in notion
        """
        for key in label_ids:
            # if label == 0:
            #     return []
            if key == label:
                return [label_ids[label]]
            else:
                continue
        return []

    def assign_priority(self, priority_text):
        """
        Helper function to assign priority level to tasks in Todoist
        Ranges b/w 1(Low) - 4(Urgent)
        """
        if priority_text == 0:
            return 1
        elif priority_text == "Medium":
            return 2
        elif priority_text == "High":
            return 3
        elif priority_text == "#SuperHigh":
            return 4
        else:
            return 1

    def assign_section(self, project, status):
        if status == "To Do":
            return project["To Do_id"]
        elif status == "Backlog" or status == 0:
            return project["Backlog_id"]
        else:
            return project["On-Going_id"]

    def get_active_tasks(self):
        """Returns active task currently there in todoist"""
        url = f"{self.base_url}/tasks"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        super().add_to_msg(f"Active tasks retrived from todoist. URL: {url}")
        return data

    def create_task(self, task_list):
        """Creates tasks  from a give task list in a specific format"""
        post_url = f"{self.base_url}/tasks"
        headers = {
            "Authorization": self.auth_key,
            "Content-Type": "application/json",
        }

        super().add_to_msg("\n\n")

        for task in task_list:
            if task["Project"] == 0:
                new_task = {
                    "content": task["Name"],
                    "description": f"Notion ID: {task['id']}"
                    if task["Notes"] == 0
                    else task["Notes"],
                    "label_ids": self.assign_label_ids(task["Related To"]),
                    "priority": self.assign_priority(task["Priority"]),
                    "due_date": "" if task["ToDo On"] == 0 else task["ToDo On"],
                }
                response = requests.post(
                    url=post_url, headers=headers, json=new_task
                )
                response.raise_for_status()
                super().add_to_msg(f"[Task] - {task['Name']} created")
            else:
                created_project = self.handle_project.create_project(
                    project_name=task["Project"]
                )
                created_project = created_project.to_dict(orient="records")[0]
                new_task = {
                    "content": task["Name"],
                    "description": f"Notion ID: {task['id']}"
                    if task["Notes"] == 0
                    else task["Notes"],
                    "label_ids": self.assign_label_ids(task["Related To"]),
                    "priority": self.assign_priority(task["Priority"]),
                    "due_date": "" if task["ToDo On"] == 0 else task["ToDo On"],
                    "project_id": created_project["project_id"],
                    "section_id": self.assign_section(
                        status=task["Status"], project=created_project
                    ),
                }
                response = requests.post(
                    url=post_url, headers=headers, json=new_task
                )
                response.raise_for_status()
                super().add_to_msg(f"[Task] - {task['Name']} created")

        super().add_to_msg(f"Active tasks added to todoist. URL: {post_url}")

    def delete_all_tasks(self):
        """Deletes all current active task"""
        all_tasks = self.get_active_tasks()
        super().add_to_msg("\n\n")
        for task in all_tasks:
            delete_url = f"{self.base_url}/tasks/{task['id']}"
            requests.delete(url=delete_url, headers=self.headers)
            super().add_to_msg(
                f"Active tasks deleted from todoist. ID: {task['id']}"
            )
        super().add_to_msg("\n\n")

        super().add_to_msg("Yesterday's task were deleted...")
