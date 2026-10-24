from fastapi import FastAPI,Depends,status
from pydantic import BaseModel
app = FastAPI()

class Course(BaseModel):
    name: str
    teacher:str
    weekday:str
    time:str

FAKE_DB = [
    {"name":"计算机网络","teacher":"张老师","weekday":"周一","time":"8:00-9:40"},
    {"name":"操作系统","teacher":"李老师","weekday":"周三","time":"10:00-11:40"},
    {"name":"数据结构","teacher":"王老师","weekday":"周五","time":"14:00-15:40"},
]

def get_db():
    return FAKE_DB

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

@app.get("/courses", response_model=list[Course])
def get_courses(weekday:str | None = None, db: list = Depends(get_db)):
    if weekday is None:
        return db
    return [c for c in db if c["weekday"] == weekday]
#post接口
@app.post("/courses",status_code=status.HTTP_201_CREATED)
def create_course(course: Course,db:list=Depends(get_db)):

    db.append(course.model_dump())
    return {"message":"添加成功","course":course}