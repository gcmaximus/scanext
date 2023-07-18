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
    data: dict[int, dict[int, list[dict]]] = {}

    app = FastAPI()

    @app.get("/xss/{id}/{payload_no}")
    async def get_xss(id: int, payload_no: int, req: Request):
        nonlocal data
        data_list: list = data.setdefault(id, {}).setdefault(payload_no, [])
        data_list.append(await extract_data(req))
        return {"message": "OK"}

    @app.post("/xss/{id}/{payload_no}")
    async def post_xss(id: int, payload_no: int, req: Request):
        nonlocal data
        data_list: list = data.setdefault(id, {}).setdefault(payload_no, [])
        data_list.append(await extract_data(req))
        return {"message": "OK"}

    @app.get("/data/{id}/{payload_no}")
    async def get_data(id: int, payload_no: int):
        nonlocal data
        return {"data": data.get(id, {}).get(payload_no, [])}

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
