from fastapi import  FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import uvicorn
from sqlalchemy import create_engine

from typing_extensions import Annotated

template = Jinja2Templates(directory="templates")

# db_connection = create_engine("mysql://root:1234@127.0.0.1:3306/test?charset=utf8mb4")
# query= db_connection.execute('select * from  player')
# result = query.fetchall()

# for data in result:
#     print(data)

app = FastAPI()
@app.get("/")
def hello():
    return "안녕하세요"

# html 렌더링
@app.get("/test")
def test(request : Request):
    print(request)
    return template.TemplateResponse("test.html",context={"request":request,"a":2})

@app.get("/test/{name}/{gender}")
def get_arg_print(request: Request, name:str, gender:str):
    print(name,gender)
    return name , gender

# html 렌더링
@app.post("/test_post")
def test_post(name: Annotated[str, Form()], pwd: Annotated[int,Form()]):
    return (name, pwd)


@app.get("/test_get")
def test_get(request:Request):
    return template.TemplateResponse("post_test.html",{"request":request})


@app.get("/mysqltest")
def test_get(request:Request):
    db_connection = create_engine("mysql://root:1234@127.0.0.1:3306/test?charset=utf8mb4")
    query= db_connection.execute('select * from  player')
    result = query.fetchall()
    resultlist = []
    for data in result : 
        # print(data[0])
        temp = {'player_id':data[0], "player_name":data[1]}
        resultlist.append(temp)

    return template.TemplateResponse("sqltest.html",{"request":request,'result_table':resultlist})


@app.get("/detail")
def test_get(request:Request, id:str):
    print("detail")
    print(id)
    db_connection = create_engine("mysql://root:1234@127.0.0.1:3306/test?charset=utf8mb4")
    print('select * from  player where player_id = {}'.format(id))
    query= db_connection.execute('select * from  player where player_id = {}'.format(id))
    result = query.fetchall()
    print(result)

    return template.TemplateResponse("detail.html",{"request":request,'result_table':result})


if __name__  == "__main__":
    uvicorn.run(app, host= "localhost",port = 1113)