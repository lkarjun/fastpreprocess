from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import nest_asyncio
import os

from fasteda import *


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name='static')
templates = Jinja2Templates(directory="template")



@app.get('/')
async def home(requset: Request):
    testing()
    return process_data(requset)


@app.get('/drop')
def drop_column(column):
    filedetail.objcopy = filedetail.objcopy.drop(column, axis=1)
    return "okay"

@app.get('/view')
def view_new_ds(request: Request):
    return templates.TemplateResponse('ViewNewDataset.html', 
                        context={'request': request, 'sample': fasteda.sample(new=True)})

@app.get('/get_dummy')
def get_dummy(column):
    filedetail.objcopy = pd.get_dummies(filedetail.obj, columns=[column])
    return "Okay"


@app.get('/testing')
async def home(requset: Request):
    return templates.TemplateResponse('testing.html', context={'request': requset})


def testing():
    filename = 'static/dataset/sample.csv'
    dm = ','
    df = pd.read_csv(filename, delimiter=dm)

    global filedetail
    filedetail = FileDetail(filename = filename[15:],
                        filetype = filename.split('.')[-1], 
                            filesize=f"{os.stat(filename).st_size} bytes", 
                            sysfilepath=filename, 
                            obj=df,
                            missing = df.isna().sum().values.sum(),
                            objcopy = df.copy())
    


def process_data(request: Request):
    try:
        global fasteda
        fasteda = FastEda(filedetail)
        process = fasteda.process
        return templates.TemplateResponse('FastEda.html', 
                context={'request': request, 'title': 'Workspace', 
                        'fname': filedetail.filename,\
                        'sample': fasteda.sample(),\
                        'quick': fasteda.quick_stat(),\
                        'corr': fasteda.correlation(),\
                        'process': process})

    except Exception as e:
        
        return templates.TemplateResponse('error_file.html', context={'request': request, 'error': str(e)})



#-----------------------------------------------------------------------------------------------------------------------


def start(filename: str, dm=',', port = 8000):
    
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
        
        uvicorn.run(app, port=port)
    
    except Exception as e:
        
        print(e)


def start_from_colab(filename: str, dm=',', port=8000):

    from pyngrok import ngrok
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
        
        ngrok_tunnel = ngrok.connect(port)
        print('Public URL:', ngrok_tunnel.public_url)
        uvicorn.run(app, port=port)
    
    except Exception as e:
        
        print(e)


def run_from_notebook():
    '''if the server is starting from jupyter notebook, 
        user must call run_from_notebook() function befor calling start() | start_from_colab() function
    '''
    nest_asyncio.apply()


