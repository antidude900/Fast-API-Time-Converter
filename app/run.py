import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()  # Load variables from .env file

host = os.getenv("APP_HOST", "127.0.0.1")
port = int(os.getenv("APP_PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
