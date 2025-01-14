import streamlit as st
import google.generativeai as genai
import time
import os
from dotenv import load_dotenv
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("Google Gemini API key not found. Please configure your environment with 'GOOGLE_API_KEY'.")
    st.stop()

# Configure Google Gemini
genai.configure(api_key=API_KEY)

# Page configuration
st.set_page_config(
    page_title="SerenePsycheAI",
    page_icon="🧠",
    layout="wide"
)

st.title("AI Therapist🧠💬")
st.header("Don't Worry, You Will Be Alright")

# User profiles
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {}

st.sidebar.title("User Profile")
user_name = st.sidebar.text_input("Name", value=st.session_state["user_profile"].get("name", ""))
mood = st.sidebar.selectbox("How are you feeling today?", ["Happy", "Sad", "Stressed", "Angry", "Neutral"], index=4)

if st.sidebar.button("Save Profile"):
    st.session_state["user_profile"] = {"name": user_name, "mood": mood}
    st.sidebar.success("Profile saved successfully!")

# Mood tracking log
if "mood_log" not in st.session_state:
    st.session_state["mood_log"] = []

if st.sidebar.button("Log Mood"):
    st.session_state["mood_log"].append({"name": user_name, "mood": mood, "timestamp": time.ctime()})
    st.sidebar.success("Mood logged successfully!")

# Mood history visualization
if st.sidebar.checkbox("Show Mood History"):
    st.sidebar.write("### Mood History")
    if st.session_state["mood_log"]:
        mood_data = pd.DataFrame(st.session_state["mood_log"])
        st.sidebar.dataframe(mood_data)
        fig, ax = plt.subplots()
        mood_data.groupby("mood").size().plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("Mood Trend")
        st.sidebar.pyplot(fig)
    else:
        st.sidebar.write("No mood logs available.")

# Journaling feature
st.subheader("Daily Journal")
if "journal_entries" not in st.session_state:
    st.session_state["journal_entries"] = []

journal_entry = st.text_area("Write your thoughts and feelings for today:")
if st.button("Save Journal Entry"):
    st.session_state["journal_entries"].append({"timestamp": time.ctime(), "entry": journal_entry})
    st.success("Journal entry saved successfully!")

if st.checkbox("View Past Journal Entries"):
    st.write("### Your Journal Entries")
    for entry in st.session_state["journal_entries"]:
        st.write(f"**{entry['timestamp']}**: {entry['entry']}")

# Blog for mental health tips
st.sidebar.title("Mental Health Blog")
if st.sidebar.button("Show Tips"):
    st.sidebar.write("### Mental Health Tips")
    st.sidebar.markdown("- **Practice mindfulness**: Spend 10 minutes a day focusing on your breath.")
    st.sidebar.markdown("- **Exercise regularly**: Even a 15-minute walk can improve your mood.")
    st.sidebar.markdown("- **Stay connected**: Talk to a friend or loved one regularly.")
    st.sidebar.markdown("- **Set small goals**: Accomplishing small tasks can build confidence.")

# User input for therapy session
st.subheader("Start Your Therapy Session")
user_query = st.text_area(
    "What's on your mind?",
    placeholder="Share your thoughts or ask for advice. The AI therapist is here to help.",
    help="Provide details about your concerns or ask specific questions to receive tailored responses."
)

# Guided exercises
if st.checkbox("Need a guided exercise?"):
    exercise_type = st.radio("Choose an exercise", ["Breathing", "CBT Reframing", "Mindfulness"])
    if exercise_type == "Breathing":
        st.write("### Breathing Exercise")
        st.write("Take a deep breath in for 4 seconds, hold for 4 seconds, and exhale for 4 seconds. Repeat this for 5 minutes.")
    elif exercise_type == "CBT Reframing":
        st.write("### CBT Reframing Exercise")
        st.write("Think about a negative thought you've had recently. Write it down and try to reframe it with a positive or neutral perspective.")
    elif exercise_type == "Mindfulness":
        st.write("### Mindfulness Exercise")
        st.write("Focus on your surroundings. What are five things you can see, four things you can feel, three things you can hear, two things you can smell, and one thing you can taste?")

# Get advice from AI therapist
if st.button("🧠 Get Advice", key="get_advice_button"):
    if not user_query:
        st.warning("Please enter a topic or question for the AI therapist to assist you.")
    else:
        try:
            with st.spinner("Analyzing your input and generating thoughtful insights..."):
                # Generate response using the Gemini API
                response = genai.generate_text(
                    prompt=f"""
                    Act as a compassionate and professional therapist. Analyze the user's input below and provide a thoughtful, empathetic, and actionable response.

                    User Name: {user_name}
                    User Mood: {mood}

                    User Input:
                    {user_query}

                    Ensure the response is supportive and helpful. Include any relevant resources or suggestions for guided exercises.
                    """,
                    model="gemini-1.5-flash",  # Ensure the model is correct for your use case
                    max_output_tokens=512  # Limit the token count for responses
                )
 
            # Display the result
            st.subheader("Therapist's Response")
            st.markdown(response.result)

        except Exception as error:
            st.error(f"An error occurred: {error}")
