import streamlit as st
import google.generativeai as genai

# Set your Gemini API Key here
API_KEY = "AIzaSyDC_0JvqvbhsKvI1YNeeTp_TPjJyMvm2XI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Yoga pose mapping for basic goals
goal_to_poses = {
    "Relaxation": ["Child's Pose", "Legs-Up-The-Wall", "Corpse Pose"],
    "Flexibility": ["Downward Dog", "Seated Forward Bend", "Cobra Pose"],
    "Strength": ["Plank", "Warrior II", "Chair Pose"],
    "Stress Relief": ["Cat-Cow", "Bridge Pose", "Supine Twist"]
}

def generate_yoga_instruction(pose_name):
    prompt = f"""
    Act as a yoga instructor. Explain how to do the yoga pose '{pose_name}' step-by-step.
    Include:
    1. Introduction
    2. Steps to perform
    3. Breathing tips
    4. Duration
    5. Caution or contraindications
    Format it nicely for beginners.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating instructions: {e}"

# Streamlit UI
st.set_page_config(page_title="🧘 ZenPose", page_icon="🧘")
st.title("🧘 Your Personal Yoga Guide")

# Select a goal
goal = st.selectbox("Choose your goal", list(goal_to_poses.keys()))

if goal:
    st.subheader(f"Recommended Poses for {goal}")
    poses = goal_to_poses[goal]
    selected_pose = st.radio("Select a pose to learn", poses)

    if selected_pose:
        if st.button("Show Instructions"):
            with st.spinner("Generating instructions..."):
                result = generate_yoga_instruction(selected_pose)
                st.markdown(result)

# Ask your own yoga-related question
st.markdown("---")
st.subheader("🧠 Ask Your Yoga Question")
user_question = st.text_area("What do you want to ask?", placeholder="e.g., Is it safe to do Plank pose during back pain?")
if st.button("Ask Gemini"):
    if user_question.strip():
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(user_question)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"API Error: {e}")
    else:
        st.warning("Please enter a question.")
