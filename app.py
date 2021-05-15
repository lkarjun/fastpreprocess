from fastapi import FastAPI, File, UploadFile, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from essential import FileDetail
from fasteda import *
import os
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name='static')
templates = Jinja2Templates(directory="template")

@app.get('/')
async def home(requset: Request):
    return templates.TemplateResponse('index.html', context={'request': requset, 'title': 'Home'})


@app.post('/edafileupload')
async def upload(reqest: Request, file: UploadFile = File(...)):
    filename = f'static/dataset/{str(file.filename)}'
    content = await file.read()
    with open(filename, 'wb') as file: file.write(content)

    global filedetail
    filedetail = FileDetail(filename[15:], filename.split('.')[-1], filesize=f"{os.stat(filename).st_size} bytes", sysfilepath=filename)

    return {'filename': filedetail.filename, 'filesize': filedetail.filesize, 'filetype': filedetail.filetype}



@app.get('/workspace')
async def eda(request: Request):

    fd = FileDetail(
                    'bank_data_processed.csv',
                    'csv', 
                    '500 bytes', 'static/dataset/bank_data_processed.csv', 
                     pd.read_csv('static/dataset/bank_data_processed.csv'))

    fasteda = FastEda(fd)

    return templates.TemplateResponse('FullEda.html', 
                context={'request': request, 'title': 'Workspace', 
                        'fname': fd.filename,\
                        'sample': fasteda.file_columns(),\
                        'quick': fasteda.quick_stat()})


