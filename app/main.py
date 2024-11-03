from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from model import classify_images
from celery_worker import classify_images_task
from celery.result import AsyncResult

app = FastAPI()
class ImageRequest(BaseModel):
    image_url: str


@app.post("/classify")
async def classify(image_request: ImageRequest, background_tasks: BackgroundTasks):
    task = classify_images_task.delay(image_request.image_url)
    return {"task_id": task.id, "status": "Processing"}


@app.get("/result/{task_id}")
async def get_result(task_id: str):
    result = AsyncResult(task_id)
    if result.state == 'PENDING':
        return {"status": "Processing"}
    elif result.state == 'SUCCESS':
        return {"status": "Completed", "result": result.result}
    elif result.state == 'FAILURE':
        return {"status": "Failed", "error": str(result.info)}
    else:
        return {"status": result.state}