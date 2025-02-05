import aio_pika
import asyncio
import logging
from app.database import Database
from app.utils.API_Exception import APIException

logging.basicConfig(level=logging.DEBUG)

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        parts = message.body.decode().split()
        username = parts[1] if parts[0] == "Username:" else None
        user_id = parts[3] if parts[2] == "id:" else None

        logging.info(f"Получено сообщение: {message.body.decode()}")

        Database.add_user(username, user_id)

def callback(message: aio_pika.IncomingMessage):
    asyncio.create_task(process_message(message))

async def consume():
    try:
        connection = await aio_pika.connect_robust("amqp://test:test@localhost:5672/my_vhost")

        async with connection:
            channel = await connection.channel()

            queue = await channel.declare_queue('hello', durable=True)

            await queue.consume(callback, no_ack=False)

            await asyncio.Future()

    except Exception as e:
        raise APIException(status_code=500, message="RabbitMQ connection error")
