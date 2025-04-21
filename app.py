import streamlit as st

# Title and description
st.title("🧠 Mental Health Risk Assessment")
st.markdown("""
This questionnaire helps assess risk levels for **Depression**, **Anxiety**, and **Stress** among students. 
Please answer all questions based on how you feel.
""")

# Questions and categories
questions = [
    ("I feel like I have too many responsibilities and not enough time to relax.", ["Stress", "Depression"]),
    ("I often feel anxious about the future, like grades or my career.", ["Anxiety", "Stress"]),
    ("I feel like I'm not good enough, no matter how hard I try.", ["Depression", "Anxiety"]),
    ("I find it difficult to balance schoolwork and other activities like hobbies or social time.", ["Stress", "Depression"]),
    ("I get nervous or avoid situations where I might be judged, like public speaking.", ["Anxiety", "Stress"]),
    ("I've lost interest in things I used to enjoy, like sports or hobbies.", ["Depression", "Stress"]),
    ("I get stressed when my parents or teachers expect me to achieve high marks.", ["Stress", "Anxiety"]),
    ("I feel like I'm constantly thinking about what others think of me.", ["Anxiety", "Depression"]),
    ("I find it hard to focus on schoolwork because of constant worrying or sadness.", ["Depression", "Anxiety"]),
    ("I often feel like something bad is about to happen, even when things are okay.", ["Anxiety", "Depression"]),
    ("I feel overwhelmed by deadlines, tests, or homework.", ["Stress", "Anxiety"]),
    ("I often feel like I'm just going through the motions—tired, numb, or disconnected.", ["Depression", "Stress"]),
    ("I avoid asking questions in class because I'm afraid I'll sound dumb or be judged.", ["Anxiety", "Depression"]),
    ("I feel physically tired or get headaches when I'm under pressure.", ["Stress", "Anxiety"]),
    ("I sometimes feel like I don't belong at school or even at home.", ["Depression", "Anxiety"]),
    ("I overthink small problems and blow them up.", ["Anxiety", "Stress"]),
    ("I feel isolated even when I'm around people.", ["Depression", "Anxiety"]),
    ("I often feel like there's no time to relax, and I'm always under pressure.", ["Stress", "Depression"])
]

# Initialize session state for storing responses
if "responses" not in st.session_state:
    st.session_state.responses = {}

# Custom CSS for styling
st.markdown("""
<style>
    /* Style the radio buttons as circles */
    .stRadio > div {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    
    .stRadio > div > label {
        padding: 0 !important;
        margin: 0 !important;
        color: transparent;
        width: 40px !important;
        height: 40px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stRadio > div > label:nth-child(1) {
        border: 2px solid #2e8b57 !important;
    }
    
    .stRadio > div > label:nth-child(2) {
        border: 2px solid #5bab81 !important;
    }
    
    .stRadio > div > label:nth-child(3) {
        border: 2px solid #89cb9c !important;
    }
    
    .stRadio > div > label:nth-child(4) {
        border: 2px solid #cccccc !important;
    }
    
    .stRadio > div > label:nth-child(5) {
        border: 2px solid #b59cc8 !important;
    }
    
    .stRadio > div > label:nth-child(6) {
        border: 2px solid #9c7cb1 !important;
    }
    
    .stRadio > div > label:nth-child(7) {
        border: 2px solid #8b5d9e !important;
    }
    
    .stRadio > div > label > div {
        visibility: hidden;
    }
    
    /* Make selected option darker */
    .stRadio > div > label:has(input:checked) {
        background-color: rgba(0,0,0,0.3) !important;
    }
    
    /* Hide the inner dot of the radio button */
    .stRadio > div > label > div > div {
        display: none;
    }
    
    /* Style the agree/disagree labels */
    .scale-labels {
        display: flex;
        justify-content: space-between;
        margin-top: 5px;
        margin-bottom: 0;
        font-weight: 500;
    }
    
    .agree-label {
        color: #2e8b57;
    }
    
    .disagree-label {
        color: #8b5d9e;
    }
    
    /* Style the question container */
    .question-container {
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Scoring map - 7-point scale with values from 3 to -3
score_values = [3, 2, 1, 0, -1, -2, -3]  # Maps to: Strongly Agree to Strongly Disagree

# Progress bar
progress = st.progress(0)

# Display questions
for idx, (question_text, categories) in enumerate(questions):
    key = f"q_{idx}"
    
    # Question container
    st.markdown(f"<div class='question-container'>", unsafe_allow_html=True)
    
    # Display question text
    st.markdown(f"### {question_text}")
    
    # Display scale labels
    st.markdown("""
    <div class="scale-labels">
        <div class="agree-label">Agree</div>
        <div class="disagree-label">Disagree</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create radio buttons that will be styled as circles
    options = ["1", "2", "3", "4", "5", "6", "7"]  # Using numbers to avoid label text showing
    
    # Remove default selection
    default_index = None
    response = st.radio(
        "Select an option",
        options,
        index=default_index,
        key=key,
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Store response
    if response:
        st.session_state.responses[key] = options.index(response)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Update progress bar
    progress.progress(len(st.session_state.responses) / len(questions))

# Risk interpretation logic
def interpret_risk(score, category):
    # Adjusted thresholds for the new scoring system
    if category == "Depression":
        if score < -12:
            return "Low"
        elif score < 6:
            return "Moderate"
        else:
            return "High"
    elif category == "Anxiety":
        if score < -10:
            return "Low"
        elif score < 8:
            return "Moderate"
        else:
            return "High"
    elif category == "Stress":
        if score < -8:
            return "Low"
        elif score < 8:
            return "Moderate"
        else:
            return "High"

# Calculate scores and show results
if st.button("Calculate My Risk Levels"):
    if len(st.session_state.responses) < len(questions):
        st.warning(f"Please answer all questions. You've completed {len(st.session_state.responses)} out of {len(questions)}.")
    else:
        # Calculate scores for each category
        scores = {"Depression": 0, "Anxiety": 0, "Stress": 0}
        
        for idx, (_, categories) in enumerate(questions):
            key = f"q_{idx}"
            response_idx = st.session_state.responses[key]
            score = score_values[response_idx]
            
            for cat in categories:
                scores[cat] += score
        
        # Display results
        st.markdown("## 🧾 Results:")
        
        for condition, score in scores.items():
            risk_level = interpret_risk(score, condition)
            st.write(f"**{condition} Score**: {score} → **{risk_level} Risk**")
        
        # Recommendations based on risk levels
        st.markdown("## 📋 Recommendations:")
        
        has_high_risk = any(interpret_risk(score, cat) == "High" for cat, score in scores.items())
        
        if has_high_risk:
            st.markdown("""
            ### ⚠️ Please Consider:
            - Talking to a trusted adult, school counselor, or mental health professional
            - Taking breaks and practicing self-care activities
            - Seeking support from friends or family members
            """)
        else:
            st.markdown("""
            ### 👍 Suggestions:
            - Continue practicing healthy coping strategies
            - Maintain a balanced lifestyle with adequate sleep and exercise
            - Reach out for help if you notice your feelings changing
            """)

# Reset button to clear all responses
if st.button("Reset Questionnaire"):
    st.session_state.responses = {}
    st.rerun()  # Updated from st.experimental_rerun()