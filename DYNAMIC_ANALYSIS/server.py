from fastapi import FastAPI, Request
# from fastapi import FastAPI, Form
# from typing import Annotated
import uvicorn
# from pydantic import BaseModel

# class InputData(BaseModel):
#     data: str

async def extract_data(req: Request):
    obj = {}
    keys = ["method", "url", "headers", "path_params", "query_params", "client", "cookies"]
    for key in keys:
        obj[key] = getattr(req, key)
    if obj["method"] == "POST" and obj["url"] == "http://127.0.0.1:8000/xss":
        async with req.form() as form:
            obj["form"] = form
    return obj

def main():
    data = []

    app = FastAPI()

    @app.get("/xss")
    async def get_xss(req: Request):
        nonlocal data
        data.append(await extract_data(req))
        return {"message": 200}

    
    @app.post("/xss")
    async def post_xss(req: Request):
        nonlocal data
        data.append(await extract_data(req))
        # Process the data as needed
        return {"message": 200}

    
    @app.get("/data")
    async def get_data():
        nonlocal data
        return {"data": data}
    
    
    @app.delete("/data")
    async def del_data():
        nonlocal data
        data = []
        # for i in alldata:
        #     alldata.pop(i)
        return {"message": "deleted"}


    uvicorn.run(app=app, host="127.0.0.1", port=8000, log_level='critical')

if __name__ == "__main__":
    main()

# Payload we might be using:
# 
# <form action="http://127.0.0.1:8000/xss" method="post">
#     <label for="data">Data:</label>
#     <input type="text" id="data" name="data">
#     <input type="submit" value="Submit">
# </form>
