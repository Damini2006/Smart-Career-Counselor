from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import joblib
import pymongo
from llm_response import get_motivation_feedback

model = joblib.load("model.pkl")
le_interest = joblib.load("interest_encoder.pkl")
le_career = joblib.load("career_encoder.pkl")

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["career_db"]
collection = db["students"]

app = FastAPI()

class Student(BaseModel):
    name: str
    math: int
    science: int
    english: int
    coding: int
    drawing: int
    speaking: int
    interest: str

@app.post("/predict")
def predict_career(student: Student):
    try:
        interest_encoded = le_interest.transform([student.interest])[0]
    except ValueError:
        return {"error": f"Interest '{student.interest}' was not seen during training."}

    features = [[
        student.math, student.science, student.english,
        student.coding, student.drawing, student.speaking,
        interest_encoded
    ]]

    prediction = model.predict(features)[0]

    try:
        career = le_career.inverse_transform([prediction])[0]
    except ValueError:
        return {"error": f"Predicted label '{prediction}' is not a known career label."}

    skills = {
        "Math": student.math,
        "Science": student.science,
        "English": student.english,
        "Coding": student.coding,
        "Drawing": student.drawing,
        "Speaking": student.speaking,
        "Interest": student.interest
    }

    feedback = get_motivation_feedback(student.name, career, skills)

    data = student.dict()
    data["predicted_career"] = career
    data["feedback"] = feedback
    collection.insert_one(data)

    return {"predicted_career": career, "feedback": feedback}
