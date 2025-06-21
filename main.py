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
    # for index, todo in enumerate(todos):
    #     if todo.id == todo_id:
    #         return todo
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    print(todo)
    return todo.first()

@app.post("/todos", response_model=Todoresponse)
# def create_todo(todo: TodoBase):
#     todos.append(todo)
#     return todos[-1]
def create_todo(todo: TodoBase, db: Session = Depends(get_db)):
    db_todo = TodoModel(title=todo.title, description=todo.description, completed=todo.completed)  # Use TodoCreate here
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}", response_model=Todoresponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    # for index, todo in enumerate(todos):
    #     if todo.id == todo_id:
    #         todos.remove(todo)
    #         return {"Message": "Deleted successfully"}
    # raise HTTPException(status_code=404, detail="Not Found")
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    db.delete(todo)
    db.commit()
    return todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: TodoCreate):  # Use TodoCreate or Todoupdate
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos[index] = updated_todo.dict()
            return {"message": "Todo updated successfully", "todo": todos[index]}
    return {"error": "Todo not found"}
