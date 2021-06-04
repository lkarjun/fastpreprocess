from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from fastpreprocess.process import *
import os

filedetail = None
fastprocess = None
process = None

app = FastAPI()
path = str(__file__)
app.mount("/static", StaticFiles(directory=path[:-11]+'static'), name='static')
templates = Jinja2Templates(directory=path[:-11]+'template')

#____________________________________________________________________________________________________________________________________

@app.get('/')
async def home(requset: Request):
    return process_data(requset)

@app.get('/index')
async def index(request: Request):
    return templates.TemplateResponse('Index.html', context={'request': request, 'title': 'Home'})

@app.get('/advance')
def FullAction(request: Request):
    try:
        return templates.TemplateResponse('action_center.html', 
                            context={'request':request, 'sample': fastprocess.sample(new=True)})
    except Exception as e:
        return templates.TemplateResponse('error_file.html', context={'request': request, 'error': str(e)})


@app.get('/view')
def view_new_ds(request: Request):
    try:
        return templates.TemplateResponse('ViewNewDataset.html', 
                        context={'request': request,
                                 'sample': fastprocess.sample(new=True),
                                 'head_tail': fastprocess.get_head_tail_()})
    except Exception as e:
        return templates.TemplateResponse('error_file.html', context={'request': request, 'error': str(e)})


@app.get('/testing')
async def home(requset: Request):
    filename = path[:-11]+'static/car_sample.csv'
    # filename = 'fastpreprocess/static/car_sample.csv'
    set_global_filedetail(filename, dm = ',', lowmem=False)
    return process_data(requset)


@app.get('/log')
def log(request: Request):
    try:
        return templates.TemplateResponse('log.html', context={'request': request, 'values': fastprocess.log})
    except Exception as e:
        return templates.TemplateResponse('error_file.html', context={'request': request, 'error': str(e)})
#____________________________________________________________________________________________________________________________________

@app.get('/info')
async def info(column):
    return fastprocess.get_info_(column)

@app.get('/drop')
def dropna(data):
    print("Okag", data)
    fastprocess.dropna()
    print('finished')
    return "droped missing values from all columns"

@app.get('/replace')
def replace(rep, value, to, reg):
    reg = True if reg == 'true' else False
    print(rep, value, to, reg)
    return 'Okay'

@app.get('/action')
def tester(column, action):
    print(column, action)
    if action == 'drop': return fastprocess.drop_column_(column)
    elif action == 'get_dummy': return fastprocess.get_dummy_(column)
    elif action[:11] == 'fillmissing': return fastprocess.missing_(column, action[12:])
    elif action in ['set_numeric', 'set_categorical']: return fastprocess.convert_(column, action[4:])
    elif action == 'label_encode': return fastprocess.label_encode_(column)
    elif action[:6] == 'scalar': return fastprocess.scaler_(column, action[7:])
    else: return "Cool"


@app.get('/save')
def save_file():
    from fastapi.responses import FileResponse
    fastprocess.copy.to_csv('processed.csv', index = False)
    return FileResponse('processed.csv', filename='processed.csv')

@app.get('/savejson')
def save_json():
    from fastapi.responses import FileResponse
    fastprocess.save_params()
    return FileResponse('params.json', filename='params.json')

def process_data(request: Request):
    try:
        temp = templates.TemplateResponse('Fastprocess.html', 
                context={'request': request, 'title': 'Workspace', 'file': filedetail,\
                        'sample': fastprocess.sample(), 'quick': fastprocess.quick_stat(),\
                        'corr': fastprocess.correlation(), 'process': fastprocess.process})
        return temp

    except Exception as e:
        
        return templates.TemplateResponse('error_file.html', context={'request': request, 'error': str(e)})



@app.get('/objcopyAnalysis')
async def copy_analysis(request: Request):
    try:
        fastprocess.get_new()

        return templates.TemplateResponse('Fastprocess.html', 
                context={'request': request, 'title': 'Workspace', 'file': filedetail, 'sample': fastprocess.sample(),\
                        'quick': fastprocess.quick_stat(), 'corr': fastprocess.correlation(new=True),\
                        'process': fastprocess.process})

    except Exception as e:
        
        return templates.TemplateResponse('error_file.html', context={'request': request, 'error': str(e)})


@app.post('/edafileupload')
async def upload(file: UploadFile = File(...), dm=Form(...), lowmem=Form(...)):
    lowmem = True if lowmem == 'True' else False

    filename = file.filename
    content = await file.read()
    with open(filename, 'wb') as file: file.write(content)

    try:
        set_global_filedetail(filename=filename, dm=dm, lowmem=lowmem)
        try:
            os.remove(filename)
        except:
            print("Can't delete, file is in current directory...")
        
        return {'filename': filedetail.filename, 'filetype': filedetail.filetype, 'verify': "Validated"}

    except Exception as e:
        return {'filename': "Error", 'filetype': "Error", 'verify': str(e)}




def set_global_filedetail(filename, dm, lowmem):
    df = pd.read_csv(filename, delimiter=dm, low_memory=lowmem)
    print("Global Filedetail Processing")
    global filedetail
    filedetail = FileDetail(filename = filename, filetype = filename.split('.')[-1], 
                            sysfilepath=filename, obj=df, objcopy = df.copy())
    
    global fastprocess
    fastprocess = FastPreProcess(filedetail)

    global process
    process = fastprocess.process
    print("Global Filedetail Fixed")



def run_from_local():
    '''Entry point for console script
        args: -fn = Filename, -dm = delimiter, -p = Port, -c = Cloud console.
    '''
    arg = process_arg()
    low_memory = True if arg.lowmemory.lower() in ('True', 'true', 't') else False
    cloud_console = True if arg.cloudconsole.lower() in ('True', 'true', 't') else False
    port = int(arg.port)

    if cloud_console:
        start_from_cloud(arg.filename, arg.delimiter, port, low_memory)
    else:
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


def start_from_cloud(filename: Union[str, None] = None, dm=',', port=8000, lowmem=True):

    from pyngrok import ngrok
    try:
        ngrok_tunnel = ngrok.connect(port)
        
        if filename is None: print(f'\n\033[93mVisit: {ngrok_tunnel.public_url}/index\033[0m\n')
        else:
            print(f'\n\033[93mVisit: {ngrok_tunnel.public_url}\033[0m\n')
            set_global_filedetail(filename=filename, dm=dm, lowmem=lowmem)
            

        uvicorn.run(app, port=port)
    
    except Exception as e:
        
        print(e)


def run_from_notebook():
    '''if the server is starting from jupyter notebook, 
        user must call run_from_notebook() function befor calling start() | start_from_colab() function
    '''
    import nest_asyncio
    nest_asyncio.apply()



