import asyncio
import models.user
from database import create_tables

asyncio.run(create_tables())