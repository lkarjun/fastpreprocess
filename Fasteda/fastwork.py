from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os

from Fasteda.fasteda import *


filedetail = None
fasteda_ = None
process = None

app = FastAPI()

app.mount("/static", StaticFiles(directory="Fasteda/static"), name='static')
templates = Jinja2Templates(directory="Fasteda/template")



@app.get('/')
async def home(requset: Request):
    return process_data(requset)

@app.get('/view')
def view_new_ds(request: Request):
    try:
        return templates.TemplateResponse('ViewNewDataset.html', 
                        context={'request': request,
                                 'sample': fasteda_.sample(new=True)})
    except Exception as e:
        return templates.TemplateResponse('error_file.html', context={'request': request, 'error': str(e)})


#----------------------------------------------------------------------------------------------
@app.get('/testing')
async def home(requset: Request):
    filename = 'Fasteda/static/dataset/car_sample.csv'
    dm = ','
    set_global_filedetail(filename, dm)
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
    fasteda_ = FastEda(filedetail)
    global process
    process = fasteda_.process

    print('finished')
    return "droped missing values from all columns"




def process_data(request: Request):
    try:
        global fasteda_
        fasteda_ = FastEda(filedetail)

        global process
        process = fasteda_.process

        return templates.TemplateResponse('FastEda.html', 
                context={'request': request, 'title': 'Workspace', 
                        'file': filedetail,\
                        'sample': fasteda_.sample(),\
                        'quick': fasteda_.quick_stat(),\
                        'corr': fasteda_.correlation(),\
                        'process': process})

    except Exception as e:
        
        return templates.TemplateResponse('error_file.html', context={'request': request, 'error': str(e)})


@app.get('/index')
async def index(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request, 'title': 'Home'})

@app.get('/objcopyAnalysis')
async def copy_analysis(request: Request):
    fd_obj = filedetail.copy()
    fd_obj.filename = fd_obj.filename+'(Processed)'
    fd_obj.obj = filedetail.objcopy
    fd_obj.missing = fd_obj.obj.isna().sum().values.sum()

    try:
        fasteda_copy = FastEda(fd_obj)
        process_copy = fasteda_copy.process

        return templates.TemplateResponse('FastEda.html', 
                context={'request': request, 'title': 'Workspace', 'file': fd_obj, 'sample': fasteda_copy.sample(),\
                        'quick': fasteda_copy.quick_stat(), 'corr': fasteda_copy.correlation(),\
                        'process': process_copy})

    except Exception as e:
        
        return templates.TemplateResponse('error_file.html', context={'request': request, 'error': str(e)})


@app.post('/edafileupload')
async def upload(file: UploadFile = File(...), dm=Form(...)):
    
    filename = file.filename
    content = await file.read()
    with open(filename, 'wb') as file: file.write(content)

    try:
        set_global_filedetail(filename=filename, dm=dm)
    
        os.remove(filename)

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


def set_global_filedetail(filename, dm):
    df = pd.read_csv(filename, delimiter=dm)
    print("Global Filedetail seting")
    global filedetail
    filedetail = FileDetail(filename = filename, filetype = filename.split('.')[-1], filesize=f"{os.stat(filename).st_size} bytes", 
                            sysfilepath=filename, obj=df, missing = df.isna().sum().values.sum(), objcopy = df.copy())
    print("Global Filedetail seted")


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
    from sklearn.preprocessing import LabelEncoder
    encode = LabelEncoder()
    filedetail.objcopy[column] = encode.fit_transform(filedetail.objcopy[column])
    return f"Label Encoded: {encode.classes_}"
#-----------------------------------------------------------------------------------------------------------------------


def start(filename: Union[str, None] = None, dm=',', port = 8000):
    try:
        if filename is None: print('Visit: http://127.0.0.1:8000/index')
        else: 
            print('Visit: http://127.0.0.1:8000')
            set_global_filedetail(filename=filename, dm=dm)

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


