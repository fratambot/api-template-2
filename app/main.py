import os
import secrets

from fastapi import Depends, FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# custom modules
from models.algebra import array


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# Basic Auth
security = HTTPBasic()

def get_current_username(
    credentials: HTTPBasicCredentials = Depends(security),
):
    correct_username = secrets.compare_digest(
        credentials.username, os.environ.get("API_USERNAME", "username")
    )
    correct_password = secrets.compare_digest(
        credentials.password, os.environ.get("API_PASSWORD", "password")
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


###################
# status endpoint #
###################

@app.get("/")
def status():
    return {"status": "Ok"}

##################
# docs endpoints #
##################


@app.get("/docs", include_in_schema=False)
def get_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/openapi.json", include_in_schema=False)
def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title="FastAPI", version="0.1.0", routes=app.routes)

###################
# other endpoints #
###################

@app.get("/array")
def get_array(
    username: str = Depends(get_current_username)
):
    try:
        result = array.get_random().tolist()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"{type(e).__name__}: {str(e)}"
        )
    return {"result": result}

