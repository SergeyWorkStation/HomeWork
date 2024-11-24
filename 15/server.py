from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


app = FastAPI()


DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    deadline = Column(String)


Base.metadata.create_all(bind=engine)


class TaskCreate(BaseModel):
    name: str
    deadline: str


@app.get("/tasks")
def get_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    db.close()
    return tasks


@app.post("/tasks", response_model=TaskCreate)
def create_task(task: TaskCreate):
    db = SessionLocal()
    new_task = Task(name=task.name, deadline=task.deadline)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    db.close()
    return new_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        db.close()
        return {"message": "Task deleted"}
    else:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")