from fastapi import FastAPI, File, UploadFile, Request, BackgroundTasks
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
async def upload(reqest: Request, file: UploadFile = File(...)):
    filename = f'static/dataset/{str(file.filename)}'
    content = await file.read()
    with open(filename, 'wb') as file: file.write(content)

    global filedetail
    filedetail = FileDetail(filename[15:], 
                            filename.split('.')[-1], 
                            filesize=f"{os.stat(filename).st_size} bytes", 
                            sysfilepath=filename, obj=pd.read_csv(filename))

    return {'filename': filedetail.filename, 'filesize': filedetail.filesize, 'filetype': filedetail.filetype}



@app.get('/workspace')
async def eda(request: Request):

    df = pd.read_csv('static/dataset/cars.csv', delimiter=',')
    sub_df = df[[' time-to-60', ' year']]
    fd = FileDetail(
                    'cars.csv',
                    'csv', 
                    '500 bytes', 'static/dataset/cars.csv', 
                     sub_df)

    fasteda = FastEda(fd)
    process = IndividualVariable(fd)
    process.start()
    sample2 = process.full_variables.Variables[0].boxplot_json()
    print(sample2)

    return templates.TemplateResponse('FullEda.html', 
                context={'request': request, 'title': 'Workspace', 
                        'fname': fd.filename,\
                        'sample': fasteda.file_columns(),\
                        'quick': fasteda.quick_stat(),\
                        'corr': fasteda.correlation().json(),\
                        'bplot': sample2})


