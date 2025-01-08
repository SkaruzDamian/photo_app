from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
import logging
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os

class AzureStorageService:
    def __init__(self, connection_string, container_name):
        self.connection_string = connection_string
        self.container_name = container_name
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)
        self._ensure_container_exists()

    def _ensure_container_exists(self):
        """Upewnia się, że kontener istnieje"""
        try:
            self.blob_service_client.create_container(self.container_name)
            logging.info(f"Container {self.container_name} created")
        except ResourceExistsError:
            logging.info(f"Container {self.container_name} already exists")

    def upload_file(self, file, user_id):
        """
        Przesyła plik do Azure Blob Storage
        
        Args:
            file: FileStorage object
            user_id: ID użytkownika
            
        Returns:
            tuple: (blob_url, blob_name)
        """
        try:
            # Generuj bezpieczną nazwę pliku
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = secure_filename(file.filename)
            blob_name = f"user_{user_id}/{timestamp}_{filename}"
            
            # Utwórz blob client
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            # Prześlij plik
            file.seek(0)
            blob_client.upload_blob(file)
            
            # Generuj URL
            blob_url = blob_client.url
            
            return blob_url, blob_name
            
        except Exception as e:
            logging.error(f"Error uploading file: {str(e)}")
            raise

    def delete_file(self, blob_name):
        """Usuwa plik z Azure Blob Storage"""
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            blob_client.delete_blob()
            return True
        except ResourceNotFoundError:
            logging.warning(f"Blob {blob_name} not found")
            return False
        except Exception as e:
            logging.error(f"Error deleting blob: {str(e)}")
            raise

    def get_file_url(self, blob_name, expiry_hours=24):
        """Generuje URL z SAS tokenem do pliku"""
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            # Generuj SAS token
            expiry = datetime.utcnow() + timedelta(hours=expiry_hours)
            sas_token = blob_client.generate_shared_access_signature(
                permission='r',
                expiry=expiry
            )
            
            return f"{blob_client.url}?{sas_token}"
            
        except Exception as e:
            logging.error(f"Error generating SAS URL: {str(e)}")
            raise

    def move_file(self, source_blob_name, destination_blob_name):
        """Przenosi plik między kontenerami w Azure Blob Storage"""
        try:
            source_blob = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=source_blob_name
            )
            
            destination_blob = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=destination_blob_name
            )
            
            # Skopiuj blob
            destination_blob.start_copy_from_url(source_blob.url)
            
            # Usuń źródłowy blob
            source_blob.delete_blob()
            
            return destination_blob.url
            
        except Exception as e:
            logging.error(f"Error moving blob: {str(e)}")
            raise