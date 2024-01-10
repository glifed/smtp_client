import uvicorn
from fastapi import FastAPI, Form, HTTPException, Request, status, Security, Depends, HTTPException
import smtplib
from email.message import EmailMessage
import os
import logging
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.openapi.models import APIKey
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader, APIKeyCookie

load_dotenv()

logging.basicConfig(filename='example.log', format='%(asctime)s %(levelname)s:%(message)s', filemode='w',
                    encoding='utf-8', level=logging.DEBUG)


api_key_query = APIKeyQuery(name=str(os.environ.get('API_KEY_NAME')), auto_error=False)
api_key_header = APIKeyHeader(name=str(os.environ.get('API_KEY_NAME')), auto_error=False)
api_key_cookie = APIKeyCookie(name=str(os.environ.get('API_KEY_NAME')), auto_error=False)


async def get_api_key(
        api_key_query: str = Security(api_key_query),
        api_key_header: str = Security(api_key_header),
        api_key_cookie: str = Security(api_key_cookie),
):
    if api_key_query == str(os.environ.get('API_KEY')):
        return api_key_query
    elif api_key_header == str(os.environ.get('API_KEY')):
        return api_key_header
    elif api_key_cookie == str(os.environ.get('API_KEY')):
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Ошибка 403. Нет доступа"
        )


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/submit")
def submit(Email: str = Form(), Subject: str = Form(), Message: str = Form(), api_key: APIKey = Depends(get_api_key)):
    msg = EmailMessage()
    msg['Subject'] = Subject
    msg['From'] = os.environ.get('EMAIL_USER')
    msg['To'] = Email
    msg.set_content(f"""{Message}""")

    with smtplib.SMTP(str(os.environ.get('EMAIL_SERVER')), str(os.environ.get('EMAIL_PORT'))) as smtp:
        smtp.login(str(os.environ.get('EMAIL_USER')), str(os.environ.get('EMAIL_PASS')))
        smtp.send_message(msg)

    logging.info(f"status code: {status.HTTP_200_OK}, detail: Email successfully sent")
    return HTTPException(status_code=status.HTTP_200_OK, detail="Email successfully sent")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
