from celery import Celery
from model import classify_images

celery = Celery(__name__, broker='redis://redis:6379/0')


@celery.task
def classify_images_task(image_url):
    return classify_images(image_url)
