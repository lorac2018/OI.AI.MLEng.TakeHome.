**Scenario**

You are a Machine Learning Engineer for Ocean Infinity working on a marine conversion image classifier. The system could be useful for marine biologists, convervationists and others tracking oceanic species, as well as for performing machine environmental assessments.
This task is designed to evaluate your skills in building a scalable end-to-end image classification service, and in model deployment.

**Goal**
The goal is to create an image classification service that can recognize some classes of marine animals. Taking advantage of the fact that the ImageNet dataset already has some classes pertaining to marine animals, use a model pre-trained on ImageNet (i.e, ResNet) to create an image classification service that accepts an image and returns an ImageNet class.

**My Solution**

I divided the project into three major sections:

main.py: FastAPI app setup
model.py: classification model setup
celery_worker.py: celery configurations for async processing


**RESTful API**

FastAPI to create the RESTful API with endpoint  "/classify":

I opted for FASTAPI because is high-performance and optimized for asynchronous operations, its performance and simplicity make it a good fit for building RESTful APIs, especially in production environments. It supports requests and background tasks which allows us to handle multiple requests efficiently. 


**MODEL PRE-PROCESSING / SETUP**

* ResNet50 is a well known model architecture with a good balance between accuracy and computational efficiency. It is built under a large dataset with a diverse set of pre-trained classes whcih provides a good starting point for this task.

* Pytorch offers an extensive library of pre-trained models and it allows an easy integration for image preprocessing and classifying images.

IMAGE PROCESSING INSIDE THE MODEL

Preprocessing of the image is necessary to match the input requirements of the ResNet 50 which is 224 x 224 pixels. 
CNN like ResNet50 are trained on images with specific characteristics, and if the input images don't match these requirements, the model's performance can suffer, leading to incorrect classifications on predictions. 

Most image processing libraries, such as PIL (Python Imaging Library) provide a straightforward way to resize the images. 
When resizing, the aspect ratio of the image might change, potentially distorting the image if resized without consideration. 

A common preprocessing technique is to resize the image to a slightly larger dimension and then center-crop it to 224 x 224. This ensures that the main subject is in the center and reduces the impact of unwanted borders. 
Models like this are trained on datasets where the pixel values are normalised to have a specific mean and standard deviation, which helps the model converge more effectively during training and perform better during inference. The RGB channels are normalised to:

[Mean]: [0.485, 0.456, 0.406]
[Standard Deviation]: [0.229, 0.224, 0.225]
 
After converting the pixel values to a tensor (values between 0 and 1), we can subtract the mean and divide by the standard deviation for each channel separately, ensuring that the input image is transformed to have the same distribution as the image that the original model was trained on. 

In summary, it ensures that the input image:
* matches the fixed input size of 224 x 224 pixels.
* preserves the subject by using center cropping after the initial resizing. 
* ensures compatibility with the original training data of the model and its architecture. 

LOADING IMAGES FROM URLS

This function supports both urls and local file paths. Images from urls are read into a BytesIO stream, which are converted to PIL images, allowing to handle images directly from the web. 



**RUNNING ASYNC TASKS**

Celery: Handles background tasks.
Redis: Message broker to manage task distribution. 


* celery is a popular asynchronous task queue that works well with distributed systems. It's widely used for background tasks processing and has a robust support for tracking task status and handling retries, which makes it suitable for offloading the classification workload from the main application, allowing fast api to respond quickly and remain responsive. 

* redis is a lightweight and fast in memory data structure store, it is commonly used as a message broker for celery due to its speed and efficiency in managing tasks in real time, fitting well in this setup as it queues tasks for celery to process and keep track of task status. 


**DOCKER COMMANDS**

DOCKER IMAGE


>docker build -t oi_task .

>docker-compose up --build

> Verify if all the services are up
> Test the FastAPI endpoint for the model: localhost:8000 
> Submit a request using curl on the terminal  curl -X POST "http://localhost:8000/classify" -H "Content-Type: application/json" -d '{"image_url": "https://oeco.org.br/wp-content/uploads/oeco-migration/images/stories/out2014/peixe-napoleao.jpg"}'

Or we can use through the SwaggerUI (I usually use this)


> http://localhost:8000/docs

> POST /classify
> json request: {"image_url": "https://oeco.org.br/wp-content/uploads/oeco-migration/images/stories/out2014/peixe-napoleao.jpg"}


Response in the terminal:

oiaimlengtakehome-celery_worker-1  | [2024-11-03 15:53:01,196: WARNING/MainProcess] /usr
/local/lib/python3.9/site-packages/celery/worker/consumer/consumer.py:508: CPendingDepre
cationWarning: The broker_connection_retry configuration setting will no longer determine
oiaimlengtakehome-celery_worker-1  | whether broker connection retries are made during startup in Celery 6.0 and above.
oiaimlengtakehome-celery_worker-1  | If you wish to retain the existing behavior for retrying connections on startup,
oiaimlengtakehome-celery_worker-1  | you should set broker_connection_retry_on_startup to True.
oiaimlengtakehome-celery_worker-1  |   warnings.warn(
oiaimlengtakehome-celery_worker-1  |
oiaimlengtakehome-celery_worker-1  | [2024-11-03 15:53:01,211: INFO/MainProcess] Connected to redis://redis:6379/0
oiaimlengtakehome-celery_worker-1  | [2024-11-03 15:53:01,215: WARNING/MainProcess] /usr
/local/lib/python3.9/site-packages/celery/worker/consumer/consumer.py:508: CPendingDepre
cationWarning: The broker_connection_retry configuration setting will no longer determine
oiaimlengtakehome-celery_worker-1  | whether broker connection retries are made during startup in Celery 6.0 and above.
oiaimlengtakehome-celery_worker-1  | If you wish to retain the existing behavior for retrying connections on startup,
oiaimlengtakehome-celery_worker-1  | you should set broker_connection_retry_on_startup to True.
oiaimlengtakehome-celery_worker-1  |   warnings.warn(
oiaimlengtakehome-celery_worker-1  |
oiaimlengtakehome-celery_worker-1  | [2024-11-03 15:53:01,226: INFO/MainProcess] mingle: searching for neighbors
oiaimlengtakehome-celery_worker-1  | [2024-11-03 15:53:02,245: INFO/MainProcess] mingle: all alone
oiaimlengtakehome-celery_worker-1  | [2024-11-03 15:53:02,302: INFO/MainProcess] celery@b581bc10de53 ready.
marine_model_app                   | INFO:     172.19.0.1:50808 - "GET /docs HTTP/1.1" 200 OK
marine_model_app                   | INFO:     172.19.0.1:50808 - "GET /openapi.json HTTP/1.1" 200 OK
marine_model_app                   | INFO:     172.19.0.1:50814 - "POST /classify HTTP/1.1" 200 OK
oiaimlengtakehome-celery_worker-1  | [2024-11-03 15:54:00,970: INFO/MainProcess] Task celery_worker.classify_images_task[52e1cda3-d7c3-4524-b4a8-b2ea483ddbf2] received

"# OI.AI.MLEng.TakeHome." 
