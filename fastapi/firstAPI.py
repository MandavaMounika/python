from fastapi import FastAPI
app = FastAPI()
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
