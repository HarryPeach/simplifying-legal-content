from typing import Optional
from fastapi import FastAPI

import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"response": "This is an example simplification"}


def main():
    print("Hello world!")
    uvicorn.run("backend.__main__:app", host="127.0.0.1",
                port=8000, reload=True, workers=2)


if __name__ == "__main__":
    main()
