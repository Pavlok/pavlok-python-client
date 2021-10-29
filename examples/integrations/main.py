# Author: Third Musketeer
# -*- coding: utf-8 -*-
import uvicorn

from core.database import Base, engine
from app import app
from clickup.router import router as clickup_router
from pav_todoist.router import router as todoist_router

app.include_router(prefix="/clickup", router=clickup_router, tags=["clickup"])
app.include_router(prefix="/todoist", router=todoist_router, tags=["todoist"])

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app="app:app", port=8000, reload=True)
