from azure.servicebus import ServiceBusClient, ServiceBusMessage
import json
import logging
from datetime import datetime

class AzureQueueService:
    def __init__(self, connection_string, queue_name):
        self.connection_string = connection_string
        self.queue_name = queue_name
        self.servicebus_client = ServiceBusClient.from_connection_string(
            conn_str=connection_string,
            logging_enable=True
        )

    def send_message(self, image_id, user_id, action="review"):
        """
        Wysyła wiadomość do kolejki Azure Service Bus
        
        Args:
            image_id: ID zdjęcia
            user_id: ID użytkownika
            action: Akcja do wykonania (domyślnie "review")
        """
        try:
            # Przygotuj dane wiadomości
            message_data = {
                "image_id": image_id,
                "user_id": user_id,
                "action": action,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Utwórz wiadomość
            message = ServiceBusMessage(
                body=json.dumps(message_data).encode('utf-8'),
                content_type='application/json',
                time_to_live=timedelta(days=1)
            )
            
            # Wyślij wiadomość
            with self.servicebus_client.get_queue_sender(self.queue_name) as sender:
                sender.send_messages(message)
                
            logging.info(f"Message sent to queue: {message_data}")
            
        except Exception as e:
            logging.error(f"Error sending message to queue: {str(e)}")
            raise

    def receive_messages(self, max_messages=10):
        """
        Odbiera wiadomości z kolejki
        
        Args:
            max_messages: Maksymalna liczba wiadomości do odebrania
            
        Returns:
            list: Lista odebranych wiadomości
        """
        try:
            messages = []
            with self.servicebus_client.get_queue_receiver(self.queue_name) as receiver:
                received_messages = receiver.receive_messages(
                    max_message_count=max_messages,
                    max_wait_time=5
                )
                
                for msg in received_messages:
                    try:
                        # Parsuj wiadomość
                        message_body = json.loads(msg.body.decode('utf-8'))
                        messages.append(message_body)
                        
                        # Potwierdź otrzymanie wiadomości
                        receiver.complete_message(msg)
                        
                    except json.JSONDecodeError:
                        logging.error(f"Error decoding message: {msg.body}")
                        receiver.dead_letter_message(msg)
                        
            return messages
            
        except Exception as e:
            logging.error(f"Error receiving messages: {str(e)}")
            raise

    def peek_messages(self, max_messages=10):
        """
        Podgląda wiadomości w kolejce bez ich usuwania
        
        Args:
            max_messages: Maksymalna liczba wiadomości do podejrzenia
            
        Returns:
            list: Lista podejrzanych wiadomości
        """
        try:
            messages = []
            with self.servicebus_client.get_queue_receiver(self.queue_name) as receiver:
                peeked_messages = receiver.peek_messages(max_message_count=max_messages)
                
                for msg in peeked_messages:
                    try:
                        message_body = json.loads(msg.body.decode('utf-8'))
                        messages.append(message_body)
                    except json.JSONDecodeError:
                        logging.error(f"Error decoding peeked message: {msg.body}")
                        
            return messages
            
        except Exception as e:
            logging.error(f"Error peeking messages: {str(e)}")
            raise

    def clear_queue(self):
        """Czyści wszystkie wiadomości z kolejki"""
        try:
            with self.servicebus_client.get_queue_receiver(self.queue_name) as receiver:
                while True:
                    messages = receiver.receive_messages(max_message_count=10, max_wait_time=1)
                    if not messages:
                        break
                    for msg in messages:
                        receiver.complete_message(msg)
                        
            logging.info(f"Queue {self.queue_name} cleared")
            
        except Exception as e:
            logging.error(f"Error clearing queue: {str(e)}")
            raise