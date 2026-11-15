import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Student Performance Predictor", page_icon="📚", layout="wide"
)

st.title("🎓 Student Performance Predictor Dashboard")
st.markdown(
    "Enter your study habits and marks for all 7 subjects (**DS, DBMS, PAI, PSM, OOPS, CN, COA**) to analyze your performance, find weak spots, and get personalized suggestions!"
)

# Sidebar for Daily Habits
st.sidebar.header("🕒 Daily Habits & Lifestyle")
study_hours = st.sidebar.slider(
    "Daily Study Hours", min_value=1.0, max_value=16.0, value=4.0, step=0.5
)
sleep_hours = st.sidebar.slider(
    "Daily Sleep Hours", min_value=3.0, max_value=12.0, value=7.0, step=0.5
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Subjects Tracked:**")
st.sidebar.text(
    "• DS (Data Structures)\n• DBMS (Database Systems)\n• PAI (Python AI/ML)\n• PSM (Prob. & Stats/Math)\n• OOPS (Object-Oriented)\n• CN (Computer Networks)\n• COA (Computer Org.)"
)

# Main Form for Marks Input
st.subheader("📝 Enter Your Subject Marks (Out of 100)")
st.markdown(
    "Provide your **Past Marks** (previous exam) and **Present Marks** (current exam/mid-term)."
)

subjects = ["DS", "DBMS", "PAI", "PSM", "OOPS", "CN", "COA"]

past_marks = {}
present_marks = {}

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Past Semester / Exam Marks")
    for subj in subjects:
        past_marks[subj] = st.number_input(
            f"{subj} - Past",
            min_value=0.0,
            max_value=100.0,
            value=65.0,
            key=f"past_{subj}",
        )

with col2:
    st.markdown("### 📈 Present Semester / Exam Marks")
    for subj in subjects:
        present_marks[subj] = st.number_input(
            f"{subj} - Present",
            min_value=0.0,
            max_value=100.0,
            value=70.0,
            key=f"present_{subj}",
        )

# Calculate button
if st.button("🚀 Analyze Performance", type="primary"):
    # Calculations
    past_total = sum(past_marks.values())
    present_total = sum(present_marks.values())
    max_total = len(subjects) * 100

    past_percentage = (past_total / max_total) * 100
    present_percentage = (present_total / max_total) * 100


    # Grade calculation function
    def get_grade(percentage):
        if percentage >= 85:
            return "A+ (Outstanding)"
        elif percentage >= 75:
            return "A (Excellent)"
        elif percentage >= 65:
            return "B+ (Good)"
        elif percentage >= 55:
            return "B (Above Average)"
        elif percentage >= 45:
            return "C (Pass)"
        else:
            return "F (Needs Improvement)"


    past_grade = get_grade(past_percentage)
    present_grade = get_grade(present_percentage)

    # Display Metrics
    st.markdown("---")
    st.subheader("🏆 Overall Performance Summary")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Past Percentage", f"{past_percentage:.2f}%", f"{past_grade.split()[0]}")
    m2.metric(
        "Present Percentage",
        f"{present_percentage:.2f}%",
        f"{present_percentage - past_percentage:+.2f}%",
        delta_color="normal",
    )
    m3.metric("Overall Grade", f"{present_grade.split()[0]}")
    m4.metric("Study / Sleep Ratio", f"{study_hours}h / {sleep_hours}h")

    # Prepare DataFrame for Plotting
    chart_data = []
    for subj in subjects:
        chart_data.append(
            {"Subject": subj, "Exam": "Past", "Marks": past_marks[subj]}
        )
        chart_data.append(
            {"Subject": subj, "Exam": "Present", "Marks": present_marks[subj]}
        )

    df_chart = pd.DataFrame(chart_data)

    # Plotly Bar Chart
    st.markdown("---")
    st.subheader("📊 Subject-wise Comparison Graph")
    fig = px.bar(
        df_chart,
        x="Subject",
        y="Marks",
        color="Exam",
        barmode="group",
        text="Marks",
        title="Past vs Present Marks across All Subjects",
        color_discrete_map={"Past": "#636EFA", "Present": "#00CC96"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis_range=[0, 105])
    st.plotly_chart(fig, use_container_width=True)

    # Weak Spots Detection
    st.markdown("---")
    st.subheader("⚠️ Weak Spot Analysis")
    weak_spots = [subj for subj in subjects if present_marks[subj] < 60]
    declining_subjects = [
        subj for subj in subjects if present_marks[subj] < past_marks[subj]
    ]

    if weak_spots:
        st.warning(
            f"**Low Score Alert (Below 60%):** You need extra focus on: **{', '.join(weak_spots)}**"
        )
    else:
        st.success(
            "🎉 Great job! All your subjects are scoring 60% or above in the present exam."
        )

    if declining_subjects:
        st.info(
            f"📉 **Marks Dropped Compared to Past:** {', '.join(declining_subjects)}. Try reviewing previous assignments or clearing doubts."
        )

    # Personalized Suggestions
    st.markdown("---")
    st.subheader("💡 Personalized Study Suggestions")

    suggestions = []
    if study_hours < 4.0:
        suggestions.append(
            "• **Increase Study Hours:** Aim for at least 4.5 to 6 focused hours daily, especially for technical subjects like DS and OOPS."
        )
    elif study_hours > 10.0:
        suggestions.append(
            "• **Watch Out for Burnout:** You are studying over 10 hours daily. Make sure to take short 10-minute breaks every hour."
        )
    else:
        suggestions.append(
            "• **Balanced Routine:** Your study schedule is well-balanced. Focus on active coding practice and problem-solving."
        )

    if sleep_hours < 6.0:
        suggestions.append(
            "• **Improve Sleep:** You are getting less than 6 hours of sleep. Adequate rest (7–8 hours) is vital for memory consolidation and coding logic."
        )
    else:
        suggestions.append(
            "• **Good Sleep Routine:** Maintaining adequate sleep helps cognitive sharpness during exams."
        )

    if weak_spots:
        suggestions.append(
            f"• **Targeted Practice:** Dedicate extra weekly hours specifically to weak subjects like **{', '.join(weak_spots)}** by solving previous years' question papers."
        )

    for suggestion in suggestions:
        st.markdown(suggestion)
else:
    st.info(
        "👆 Adjust your study/sleep habits in the sidebar, input your marks above, and click **'Analyze Performance'** to generate your report!"
    )