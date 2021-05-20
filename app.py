from fastapi import FastAPI, File, UploadFile, Request, BackgroundTasks, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from essential import FileDetail
from operation import IndividualVariable
from fasteda import *
import os
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name='static')
templates = Jinja2Templates(directory="template")


@app.get('/')
async def home(requset: Request):
    return templates.TemplateResponse('index.html', context={'request': requset, 'title': 'Home'})


@app.post('/edafileupload')
async def upload(file: UploadFile = File(...), dm=Form(...)):
    filename = f'static/dataset/{str(file.filename)}'
    content = await file.read()
    with open(filename, 'wb') as file: file.write(content)

    try:
        df = pd.read_csv(filename, delimiter=dm)

        global filedetail
        filedetail = FileDetail(filename = filename[15:], 
                            filetype = filename.split('.')[-1], 
                            filesize=f"{os.stat(filename).st_size} bytes", 
                            sysfilepath=filename, 
                            obj=df,
                            missing = df.isna().sum().values.sum(),
                            objcopy = df.copy())
        return {'filename': filedetail.filename, 'filesize': filedetail.filesize, 'filetype': filedetail.filetype, 'verify': "Validated"}
    except Exception as e:
        return {'filename': "Error", 'filesize': "Error", 'filetype': "Error", 'verify': "Validated"}


@app.get('/workspace')
async def eda(request: Request):
    try:
        fasteda = FastEda(filedetail)
        process = IndividualVariable(filedetail)
        process.start()
        return templates.TemplateResponse('FullEda.html', 
                context={'request': request, 'title': 'Workspace', 
                        'fname': filedetail.filename,\
                        'sample': fasteda.file_columns(),\
                        'quick': fasteda.quick_stat(),\
                        'corr': fasteda.correlation(),\
                        'process': process})
    except Exception as e:
        
        return templates.TemplateResponse('Errorhandel.html', context={'request': request, 'error': str(e)})


@app.get('/testing')
async def test(request: Request):
    try:
        df = pd.read_csv("static/dataset/diabetes.csv", delimiter=',')
        fd = FileDetail(
                    filename = 'diabetes.csv',
                    filetype = 'csv',
                    filesize = '500 bytes', 
                    sysfilepath = 'static/dataset/diabetes.csv', 
                    obj = df,
                    missing = df.isna().sum().values.sum(),
                    objcopy = df.copy())

        fasteda = FastEda(fd)
        process = IndividualVariable(fd)
        process.start()
        return templates.TemplateResponse('FullEda.html', 
                context={'request': request, 'title': 'Workspace', 
                        'fname': fd.filename,\
                        'sample': fasteda.file_columns(),\
                        'quick': fasteda.quick_stat(),\
                        'corr': fasteda.correlation(),\
                        'process': process})
    except Exception as e:
        return templates.TemplateResponse('Errorhandel.html', context={'request': request, 'error': str(e)})
