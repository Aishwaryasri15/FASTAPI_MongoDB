from fastapi import FastAPI , APIRouter, HTTPException
from configrations import collection
from datetime import datetime
from database.schemas import all_tasks
from database.models import Todo
from bson import ObjectId

app = FastAPI()
router = APIRouter()

@router.get("/")
async  def get_all_todos():
    data = collection.find({"is_deleted": False})
    return all_tasks(data)

@router.post("/add")
async def create_task(new_task: Todo):
    try:
        response = collection.insert_one(dict(new_task))
        return {"message": "Task created successfully", "id": str(response.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred while creating the task: {str(e)}")
    
@router.put("/update/{task_id}")
async def update_task(task_id: str, updated_task: Todo):
    try:
        id = ObjectId(task_id)
        existing_task = collection.find_one({"_id": id, "is_deleted": False})
        if not existing_task:
            return HTTPException(status_code=404, detail="Task not found")
        updated_task.updated_at = int(datetime.timestamp(datetime.now()))   
        response = collection.update_one({"_id": id}, {"$set": dict(updated_task)})
        return {"status": "success", "message": "Task updated successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred while updating the task: {str(e)}")

@router.delete("/delete/{task_id}")
async def delete_task(task_id: str):
    try:
        id = ObjectId(task_id)
        existing_task = collection.find_one({"_id": id, "is_deleted": False})
        if not existing_task:
            return HTTPException(status_code=404, detail="Task not found")
        response = collection.update_one({"_id": id}, {"$set": {"is_deleted": True}})
        return {"status": "success", "message": "Task deleted successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred while deleting the task: {str(e)}")
        

app.include_router(router)

