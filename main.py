from fastapi import FastAPI
from typing import Any, List

from services.json_to_object import JSONToDartObject as jp

app = FastAPI()


@app.get("/")
def root():
    return "Home"


@app.get("/getApiData")
def getApiData():
    return someRandomJson


@app.post("/json")
def jsonParserForDict(className: str, json: dict, isList: bool = False):
    jsonToObject = jp(className, json)
    generatedCode = jsonToObject.generate(isList)
    print(generatedCode)
    return generatedCode


onlyTypesJson = {"name": "Nitin", "age": 21, "email": "nitin@gmail.com"}

someRandomJson = {
    "House": {
        "People": [
            {"name": "Nitin", "email": "nitin@gmail.com"},
            {"name": "Nitin2", "email": "nitin2@gmail.com"},
        ],
        "area": "Bhayandar",
        "landmark": "police station",
    }
}
