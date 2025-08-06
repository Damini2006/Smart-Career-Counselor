import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import joblib

df = pd.read_csv("career_dataset.csv")

le_interest = LabelEncoder()
le_career = LabelEncoder()

df["Interest"] = le_interest.fit_transform(df["Interest"])
df["Career"] = le_career.fit_transform(df["Career"])

X = df.drop("Career", axis=1)
y = df["Career"]

model = DecisionTreeClassifier()
model.fit(X, y)

joblib.dump(model, "model.pkl")
joblib.dump(le_interest, "interest_encoder.pkl")
joblib.dump(le_career, "career_encoder.pkl")
