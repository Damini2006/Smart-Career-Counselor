import streamlit as st
import requests
import random
import google.generativeai as genai
from resources import get_video_link


genai.configure(api_key="ur api key")
chat_model = genai.GenerativeModel(model_name="gemini-2.0-flash")
chat_session = chat_model.start_chat(history=[])
st.set_page_config(page_title="🎓 Smart Career Counselor", layout="wide")

icons = {
    "home": "🏠",
    "predict": "🧮",
    "quiz": "📝",
    "result": "📊",
    "career": "🎯",
    "ai": "🤖",
    "resource": "📚",
    "chat": "💬"
}

st.title(f"{icons['career']} Smart Career Counselor")
st.markdown("Empowering students with data-driven career guidance using AI!")

tabs = st.tabs([
    f"{icons['home']} Home", 
    f"{icons['predict']} Career Predictor", 
    f"{icons['quiz']} Career Suitability Quiz", 
    f"{icons['result']} Result & Suggestions",
    f"{icons['chat']} Career Chatbot"
])

with tabs[0]:
    st.header(f"{icons['home']} Welcome!")
    st.markdown("""
    Welcome to **Smart Career Counselor** – an AI-powered platform to help you find the best-suited career path.

    Steps:
    1. Provide your academic and interest scores.
    2. Get your predicted career.
    3. Take an AI-generated quiz to assess your suitability.
    4. Receive personalized resources or encouragement.
    5. Ask questions to our LLM-powered chatbot!
    """)

with tabs[1]:
    st.header(f"{icons['predict']} Step 1: Predict Your Career")

    name = st.text_input("Enter your name")

    st.subheader("📘 Academic & Skill Scores (0 to 100)")
    math = st.slider("Mathematics", 0, 100, 50)
    science = st.slider("Science", 0, 100, 50)
    english = st.slider("English", 0, 100, 50)
    coding = st.slider("Coding / Programming", 0, 100, 50)
    drawing = st.slider("Drawing / Designing", 0, 100, 50)
    speaking = st.slider("Public Speaking", 0, 100, 50)

    st.subheader("🎯 Area of Interest")
    interest = st.selectbox("Choose your interest", [
        "technology", "art", "science", "business", "education", "health", "law", "social work"
    ])

    if st.button("🔮 Get Career Suggestion"):
        if name == "":
            st.warning("Please enter your name.")
        else:
            data = {
                "name": name,
                "math": math,
                "science": science,
                "english": english,
                "coding": coding,
                "drawing": drawing,
                "speaking": speaking,
                "interest": interest
            }
            response = requests.post("http://localhost:8000/predict", json=data)

            if response.status_code == 200:
                result = response.json()
                st.success(f"🌟 Predicted Career Path: **{result['predicted_career']}**")
                st.session_state['career'] = result['predicted_career']
                st.session_state['feedback'] = result['feedback']
            else:
                st.error(f"❌ Something went wrong. {response.text}")

with tabs[2]:
    st.header(f"{icons['quiz']} Step 2: Suitability Quiz")

    def generate_quiz_questions(career):
        return [
            f"Do you enjoy tasks typically involved in {career}?",
            f"Would you be excited to pursue a full-time career in {career}?",
            f"Do you have skills needed for a {career} professional?",
            f"Are you willing to upskill for a better career in {career}?",
            f"Do you often explore more about {career}-related topics?"
        ]

    if 'career' in st.session_state:
        questions = generate_quiz_questions(st.session_state['career'])
        st.markdown(f"### 🧪 Quiz for: **{st.session_state['career']}**")

        scores = []
        for i, q in enumerate(questions):
            score = st.slider(f"Q{i+1}. {q}", 0, 100, 50)
            scores.append(score)

        if st.button("✅ Submit Quiz"):
            avg_score = sum(scores) / len(scores)
            st.session_state['quiz_score'] = avg_score
            st.success(f"Your suitability score: **{avg_score:.2f}**")
    else:
        st.info("Please complete Career Prediction first.")

with tabs[3]:
    st.header(f"{icons['result']} Final Report")

    if 'career' in st.session_state and 'quiz_score' in st.session_state:
        career = st.session_state['career']
        score = st.session_state['quiz_score']
        st.subheader("🎥 Watch a Motivational Video for Your Career")
        video_url = get_video_link(career)
        st.video(video_url)


        st.subheader("🎯 Career Recommendation")
        st.success(f"**{career}**")

        st.subheader("📈 Suitability Score")
        st.info(f"Your suitability score is: **{score:.2f}/100**")

        st.subheader("💡 Feedback & Suggestions")
        if score > 70:
            st.success("🎉 You are highly suitable for this career! Keep exploring opportunities.")
        else:
            st.warning("⚠️ You may need more preparation for this path.")
            st.markdown(f"### {icons['resource']} Recommended Resources for {career}")
            st.markdown("- [Coursera](https://www.coursera.org/)")
            st.markdown("- [edX](https://www.edx.org/)")
            st.markdown("- [Khan Academy](https://www.khanacademy.org/)")
    else:
        st.info("Please complete previous steps.")

with tabs[4]:
    st.header(f" CareerBot – Ask Your Questions")
    st.markdown("Ask anything about careers, learning paths, or improving your skills.")

    user_query = st.text_input("💬 Ask CareerBot")

    if st.button("📨 Ask"):
        if user_query.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                response = chat_session.send_message(user_query)
                st.success("🤖 CareerBot says:")

                st.write(response.text)
