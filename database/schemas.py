
def individual_todo(todo):
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"],
        "completed": todo["is_completed"]
    }

def all_tasks(todos):
    return [individual_todo(todo) for todo in todos]