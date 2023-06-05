from fastapi import FastAPI
from pydantic import BaseModel
from app.schema import HR
from database import engine
from models import student

student.Base.metadata.create_all(bind=engine)

print (HR)

app = FastAPI()


hr = [
    HR(id=1, name="malav", desg="Senior", description="Description 1"),
    HR(id=2, name="sagar", desg="fresher", description="Description 2"),
    HR(id=3, name="rency", desg="junior", description="Description 3"),
]


@app.get("/hr")
def get_all_hr():
    return hr


@app.get("/hr/{hr_id}")
def get_hr(hr_id: int):
    for i in hr:
        if i.id == hr_id:
            return i
    return {"error": "Product not found"}


@app.put("/hr/{hr_id}")
def update_hr(hr_id: int, h_r: HR):
    for index, p in enumerate(hr):
        if p.id == hr_id:
            hr[index] = h_r
            return {"message": "HR updated successfully"}
    return {"error": "HR not found"}


@app.delete("/hr/{hr_id}")
def delete_hr(hr_id: int):
    for index, i in enumerate(hr):
        if i.id == hr_id:
            del hr[index]
            return {"message": "HR deleted successfully"}
    return {"error": "HR not found"}


@app.patch("/hr/{hr_id}")
def update_hr_partial(hr_id: int, h_r: HR):
    for index, p in enumerate(hr):
        if p.id == hr_id:
            updated_product = p.copy(update=h_r.dict(exclude_unset=True))
            hr[index] = updated_product
            return {"message": "HR updated successfully"}
    return {"error": "HR not found"}


@app.post("/hr")
def create_hr(hrs: HR):
    hr.append(hrs)
    return {"message": "Hr created successfully"}
