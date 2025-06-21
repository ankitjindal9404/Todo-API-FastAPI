from fastapi import FastAPI, Depends  # Import FastAPI module
from pydantic import BaseModel  # pydantic helps validate of incoming data
from models import TodoModel
from database import Sessionlocal, engine
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException

app = FastAPI()  # create an instance of FastAPI (object of FastAPI Class). Create an app using FastAPI (like starting the engine of a car)

# todos = []

#create table in database using schema defined TodoModel class, connecting using engine.
TodoModel.metadata.create_all(bind=engine)


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):  # Used for creating a new Todo
    pass

class Todoupdate(TodoBase):  # Used for updating an existing Todo
    pass

class Todoresponse(TodoBase):
    id: int

    class Config: #it is class to define configurations/settings for a pydantic model.
        from_attributes = True  #ensures that Pydantic will automatically map the attributes from the SQLAlchemy model to the Pydantic model when creating a response for validation and serialization.
def get_db():
    db = Sessionlocal() #session creating and handling
    try:
        yield db
    finally:
        db.close()

@app.get("/todos", response_model=list[Todoresponse])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoModel).all()
    return todos

@app.get("/todos/{todo_id}", response_model=Todoresponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    print(todo)
    return todo.first()

@app.post("/todos", response_model=Todoresponse)
def create_todo(todo: TodoBase, db: Session = Depends(get_db)):
    db_todo = TodoModel(title=todo.title, description=todo.description, completed=todo.completed)  # Use TodoCreate here
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
#db.refresh(db_todo) ensures the object in Python is updated with the latest data from the database, including any database-generated values like id.

@app.delete("/todos/{todo_id}", response_model=Todoresponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    db.delete(todo)
    db.commit()
    return todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todoupdate, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.title = update_todo.title
    todo.description = update_todo.description
    todo.completed = update_todo.completed
    
    db.commit()
    db.refresh(todo)
    
    return todo # Use TodoCreate or Todoupdate