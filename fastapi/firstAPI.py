
from fastapi import FastAPI

# Create FastAPI application
app = FastAPI()

# First GET API
@app.get("/")
def home():
    return {"message": "Welcome to FastAPI!"}

@app.get("/about")
def about():
    return {
        "name": "Mounika",
        "role": "Python Developer",
        "framework": "FastAPI"
    }
