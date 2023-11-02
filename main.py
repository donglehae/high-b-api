from fastapi import FastAPI
import uvicorn
from routers import user

app = FastAPI()

routers = [user.router]
for router in routers: app.include_router(router)

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=30180)