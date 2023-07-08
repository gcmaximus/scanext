from fastapi import FastAPI, Form
from typing import Annotated
import uvicorn
from pydantic import BaseModel

class InputData(BaseModel):
    data: str

alldata = []

app = FastAPI()
@app.get("/data")
async def index(alldata=alldata):
    print(alldata)
    return {"message": "Hello World"}

@app.post("/data")
async def process_data(data: Annotated[str, Form()]):
    alldata.append(data)
    # Process the data as needed
    return data

@app.delete("/data")
async def process_data(alldata=alldata):
    for i in alldata:
        alldata.pop()
    return {"deleted"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# Payload we might be using:
# 
# <form action="http://127.0.0.1:8000" method="post">
#     <label for="data">Data:</label>
#     <input type="text" id="data" name="data" value="<img src=x onerror=alert(document.cookie)>">
#     <input type="submit" value="Submit">
# </form>