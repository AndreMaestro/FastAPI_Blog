import sys
from pathlib import Path
import asyncio
import uvicorn
sys.path.insert(0, str(Path(__file__).parent / "src"))
from core.config import settings
from app import create_app 
app = create_app()


async def run() -> None:
    config = uvicorn.Config(
        "main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD
    )
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
