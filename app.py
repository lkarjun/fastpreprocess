from fastapi import FastAPI, File, UploadFile, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name='static')
templates = Jinja2Templates(directory="template")


@app.get('/')
async def home(requset: Request):
    return templates.TemplateResponse('index.html', context={'request': requset})


@app.post('/edafileupload')
async def upload(reqest: Request, file: UploadFile = File(...)):
    filename = f'static/dataset/{str(file.filename)}'
    content = await file.read()
    with open(filename, 'wb') as file: file.write(content)
    return {'filename': filename[15:], 'filesize': f'{os.stat(filename).st_size} byte', 'filetype': str(filename).split('.')[-1]}