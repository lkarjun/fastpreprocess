from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import pkgutil
from fastprocess.process import *


filedetail = None
fastprocess = None
process = None

app = FastAPI()

path = str(__file__)

app.mount("/static", StaticFiles(directory=path[:-11]+'static'), name='static')
templates = Jinja2Templates(directory=path[:-11]+'template')



@app.get('/')
async def home(requset: Request):
    return process_data(requset)

@app.get('/view')
def view_new_ds(request: Request):
    try:
        return templates.TemplateResponse('ViewNewDataset.html', 
                        context={'request': request,
                                 'sample': fastprocess.sample(new=True)})
    except Exception as e:
        return templates.TemplateResponse('error_file.html', context={'request': request, 'error': str(e)})


#----------------------------------------------------------------------------------------------
@app.get('/testing')
async def home(requset: Request):
    filename = path[:-11]+'static/car_sample.csv'
    dm = ','
    set_global_filedetail(filename, dm, lowmem=False)
    return process_data(requset)

#----------------------------------------------------------------------------------------------

@app.get('/action')
def tester(column, action):
    print(column, action)
    if action == 'drop': return drop_column(column)
    elif action == 'get_dummy': return get_dummy(column)
    elif action[:11] == 'fillmissing': return missing(column, action[12:])
    elif action in ['set_numeric', 'set_categorical']: return convert(column, action[4:])
    elif action == 'label_encode': return label_encode(column)
    else: return "Cool"

@app.get('/drop')
def dropna(data):
    print("Okag", data)
    filedetail.objcopy = filedetail.objcopy.dropna()
    filedetail.obj = filedetail.obj.dropna()
    filedetail.missing = filedetail.obj.isna().sum().values.sum()
    fastprocess = FastPreProcess(filedetail)
    global process
    process = fastprocess.process

    print('finished')
    return "droped missing values from all columns"




def process_data(request: Request):
    try:
    
        return templates.TemplateResponse('Fastprocess.html', 
                context={'request': request, 'title': 'Workspace', 
                        'file': filedetail,\
                        'sample': fastprocess.sample(),\
                        'quick': fastprocess.quick_stat(),\
                        'corr': fastprocess.correlation(),\
                        'process': process})

    except Exception as e:
        
        return templates.TemplateResponse('error_file.html', context={'request': request, 'error': str(e)})


@app.get('/index')
async def index(request: Request):
    return templates.TemplateResponse('Index.html', context={'request': request, 'title': 'Home'})

@app.get('/objcopyAnalysis')
async def copy_analysis(request: Request):
    fd_obj = filedetail.copy()
    fd_obj.filename = fd_obj.filename+'(Processed)'
    fd_obj.obj = filedetail.objcopy
    fd_obj.missing = fd_obj.obj.isna().sum().values.sum()

    try:
        fastprocess_copy = FastPreProcess(fd_obj)
        process_copy = fastprocess_copy.process

        return templates.TemplateResponse('Fastprocess.html', 
                context={'request': request, 'title': 'Workspace', 'file': fd_obj, 'sample': fastprocess_copy.sample(),\
                        'quick': fastprocess_copy.quick_stat(), 'corr': fastprocess_copy.correlation(),\
                        'process': process_copy})

    except Exception as e:
        
        return templates.TemplateResponse('error_file.html', context={'request': request, 'error': str(e)})


@app.post('/edafileupload')
async def upload(file: UploadFile = File(...), dm=Form(...)):
    
    filename = file.filename
    content = await file.read()
    with open(filename, 'wb') as file: file.write(content)

    try:
        set_global_filedetail(filename=filename, dm=dm, lowmem=True)

        return {'filename': filedetail.filename, 'filesize': filedetail.filesize, 'filetype': filedetail.filetype, 'verify': "Validated"}

    except Exception as e:
        return {'filename': "Error", 'filesize': "Error", 'filetype': "Error", 'verify': str(e)}

@app.get('/save')
def save_file():
    from fastapi.responses import FileResponse
    filedetail.objcopy.to_csv('processed.csv')
    return FileResponse('processed.csv', filename='processed.csv')

#---------------------------------------------------------------------------------------------------------------------
#helper function


def set_global_filedetail(filename, dm, lowmem):
    df = pd.read_csv(filename, delimiter=dm, low_memory=lowmem)
    print("Global Filedetail Processing")
    global filedetail
    filedetail = FileDetail(filename = filename, filetype = 'None', filesize="None", 
                            sysfilepath="None", obj=df, missing = df.isna().sum().values.sum(), objcopy = df.copy())
    
    global fastprocess
    fastprocess = FastPreProcess(filedetail)

    global process
    process = fastprocess.process
    print("Global Filedetail Fixed")


def get_dummy(column):
    try:
        filedetail.objcopy = pd.get_dummies(filedetail.obj, columns=[column])
        return f"get dummy for {column} is done."
    except Exception as e:
        return f"get dummy for {column} is failed. due to {e}"


def drop_column(column):
    try:
        filedetail.objcopy = filedetail.objcopy.drop(column, axis=1)
        return f"drop column {column} is done."
    except Exception as e:
        return f"drop colum {column} is failed. due to {e}"


def missing(columns, method):
    if method == 'median':
        filedetail.objcopy[columns] = filedetail.objcopy[columns].fillna(filedetail.objcopy[columns].median())
        return f"Filled Missing value with {method}"
    elif method == 'mean':
        filedetail.objcopy[columns] = filedetail.objcopy[columns].fillna(filedetail.objcopy[columns].mean())
        return f"Filled Missing value with {method}"
    elif method == '0':
        filedetail.objcopy[columns] = filedetail.objcopy[columns].fillna(0)
        return f"Filled Missing value with {method}"
    else:
        filedetail.objcopy[columns] = filedetail.objcopy[columns].fillna(filedetail.objcopy[columns].mode()[0])
        return f"Filled Missing value with {method}"


def convert(column, method):
    if method == "categorical":
        filedetail.objcopy[column] = filedetail.objcopy[column].astype("category")
        return f"Converted column {column} astype to category"
    else:
        filedetail.objcopy[column] = pd.to_numeric(filedetail.objcopy[column], errors='coerce')
        return f"\nConverted column {column} to_numeric\n\
                 Note: we handled errors = 'coerce'.\n\
                 So, we're requested to perform 'Fillmissing' Action."

def label_encode(column):
    convert(column, 'categorical')
    d = dict(enumerate(filedetail.objcopy[column].cat.categories))
    filedetail.objcopy[column] = filedetail.objcopy[column].cat.codes
    return f"Label Encoded: {d}"
#-----------------------------------------------------------------------------------------------------------------------

def run_from_local():
    arg = process_arg()
    low_memory = True if arg.lowmemory.lower() in ('True', 'true', 't') else False
    port = int(arg.port)
    start(arg.filename, arg.delimiter, port, low_memory)

def start(filename: Union[str, None] = None, dm=',', port = 8000, lowmem=True):
    try:
        if filename is None: print(f"\n\033[93mVisit: http://127.0.0.1:{port}/index\033[0m\n")
        else: 
            print(f'\n\033[93mVisit: http://127.0.0.1:{port}\033[0m\n')
            set_global_filedetail(filename=filename, dm=dm, lowmem = lowmem)

        uvicorn.run(app, port=port)
    
    except Exception as e:
        
        print(e)


def start_from_cloud(filename: Union[str, None] = None, dm=',', port=8000):

    from pyngrok import ngrok
    try:
        ngrok_tunnel = ngrok.connect(port)
        
        if filename is None: print(f'Visit: {ngrok_tunnel.public_url}/index')
        else: 
            set_global_filedetail(filename=filename, dm=dm)
            print(f'Visit: {ngrok_tunnel.public_url}')

        uvicorn.run(app, port=port)
    
    except Exception as e:
        
        print(e)


def run_from_notebook():
    '''if the server is starting from jupyter notebook, 
        user must call run_from_notebook() function befor calling start() | start_from_colab() function
    '''
    import nest_asyncio
    nest_asyncio.apply()



