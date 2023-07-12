from fastapi import FastAPI, Request

# from fastapi import FastAPI, Form
# from typing import Annotated
import uvicorn

# from pydantic import BaseModel

# class InputData(BaseModel):
#     data: str


async def extract_data(req: Request):
    obj = {}
    keys = [
        "method",
        "url",
        "headers",
        "path_params",
        "query_params",
        "client",
        "cookies",
    ]
    for key in keys:
        obj[key] = getattr(req, key)
    if obj["method"] == "POST" and obj["url"] == "http://127.0.0.1:8000/xss":
        async with req.form() as form:
            obj["form"] = form
    return obj


def main():
    data: dict[int, list[dict]] = {}

    app = FastAPI()

    @app.get("/xss/{pid}")
    async def get_xss(pid: int, req: Request):
        nonlocal data
        arr: list = data.setdefault(pid, [])
        arr.append(await extract_data(req))
        return {"message": 200}

    @app.post("/xss/{pid}")
    async def post_xss(pid: int, req: Request):
        nonlocal data
        arr: list = data.setdefault(pid, [])
        arr.append(await extract_data(req))
        return {"message": 200}

    @app.get("/data/{pid}")
    async def get_data(pid: int):
        nonlocal data
        return {"data": data.get(pid, [])}

    @app.delete("/data")
    async def del_data():
        nonlocal data
        data = {}
        return {"message": "deleted"}

    uvicorn.run(app=app, host="127.0.0.1", port=8000, log_level="critical")


if __name__ == "__main__":
    main()

# Payload we might be using:
#
# <form action="http://127.0.0.1:8000/xss" method="post">
#     <label for="data">Data:</label>
#     <input type="text" id="data" name="data">
#     <input type="submit" value="Submit">
# </form>
