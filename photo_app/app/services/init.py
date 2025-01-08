from flask import current_app
from .azure_storage import AzureStorageService
from .azure_queue import AzureQueueService

storage_service = None
queue_service = None

def init_app(app):
    global storage_service, queue_service
    
    storage_service = AzureStorageService(
        connection_string=app.config['AZURE_STORAGE_CONNECTION_STRING'],
        container_name=app.config['AZURE_STORAGE_CONTAINER']
    )
    
    queue_service = AzureQueueService(
        connection_string=app.config['AZURE_SERVICE_BUS_CONNECTION_STRING'],
        queue_name=app.config['AZURE_QUEUE_NAME']
    )