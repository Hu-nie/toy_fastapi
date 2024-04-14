from fastapi import FastAPI
from routers import stats
import uvicorn
import logging
import time
import asyncio

logging.basicConfig(filename='app.log', level=logging.INFO)
app = FastAPI()

@app.get("/async")
async def asyncs():
    print("시작")
    await asyncio.sleep(3)
    print("끝")

@app.get("/sync")
def sync():
    print("시작")
    time.sleep(3)
    print("끝")

app.include_router(stats.router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8080) 