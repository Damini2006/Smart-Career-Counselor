import google.generativeai as genai

genai.configure(api_key="AIzaSyDwenD_N4-FX6DA-eDufGsTBT-4XT3ujdE")

def get_motivation_feedback(name, career, skills):
    prompt = f"""
    The student {name} has shown these skill levels:
    {skills}

    Based on their strengths and interest, we predict the most suitable career is: {career}.
    Provide a short, encouraging motivational message for the student to pursue this career.
    """

    try:
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text if response.text else "You're on the right track! Keep learning and growing."
    except Exception as e:
        print("Gemini API Error:", e)
        return "You're on the right track! Keep learning and growing."
