import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Subject Performance Tracker", layout="wide")
st.title('Subject-Wise Performance Tracker')

subjects = ['OOPS', 'DS', 'DBMS', 'PAI', 'CN', 'COA']
st.sidebar.header('Enter Subject Marks (%)')

data_list = []
for subject in subjects:
    st.sidebar.subheader(f'{subject}')
    past = st.sidebar.number_input(f'Past Mark - {subject}', min_value=0.0, max_value=100.0, value=75.0, step=1.0)
    present = st.sidebar.number_input(f'Present Mark - {subject}', min_value=0.0, max_value=100.0, value=70.0, step=1.0)
    data_list.append({
        'Subject': subject,
        'Past_Percentage': past,
        'Present_Percentage': present,
        'Difference': present - past
    })

data = pd.DataFrame(data_list)

avg_past = data['Past_Percentage'].mean()
avg_present = data['Present_Percentage'].mean()

def get_grade(score):
    if score >= 90: return 'A+'
    elif score >= 80: return 'A'
    elif score >= 70: return 'B'
    elif score >= 60: return 'C'
    else: return 'F'

col1, col2, col3 = st.columns(3)
col1.metric("Present Average", f"{avg_present:.2f}%", delta=f"{avg_present - avg_past:.2f}%")
col2.metric("Predicted Grade", get_grade(avg_present))
col3.metric("Past Average", f"{avg_past:.2f}%")

st.markdown("---")

weak_subjects = data[data['Difference'] < 0]['Subject'].tolist()
critical_subjects = data[data['Present_Percentage'] < 50]['Subject'].tolist()

if weak_subjects:
    st.warning(f"⚠️ **Weak Spots (Drop in performance):** {', '.join(weak_subjects)}")
if critical_subjects:
    st.error(f"🚨 **Critical Attention Needed (< 50%):** {', '.join(critical_subjects)}")
if not weak_subjects and not critical_subjects:
    st.success("🎉 **Great job!** You are maintaining or improving your performance across all subjects.")

st.markdown("---")

st.subheader("💡 Tailored Study Suggestions")
with st.container():
    if not weak_subjects and not critical_subjects:
        st.info("Your performance is solid! Keep up your current revision routine and practice past exam papers to maintain these grades.")
    else:
        suggestions = []
        if 'OOPS' in weak_subjects or 'OOPS' in critical_subjects:
            suggestions.append("Focus on core concepts like polymorphism and inheritance by writing more code examples.")
        if 'DS' in weak_subjects or 'DS' in critical_subjects:
            suggestions.append("Spend extra time tracing algorithms and practicing tree or graph traversal implementations.")
        if 'DBMS' in weak_subjects or 'DBMS' in critical_subjects:
            suggestions.append("Practice writing complex SQL queries and normalizing database tables.")
        if 'PAI' in weak_subjects or 'PAI' in critical_subjects:
            suggestions.append("Review fundamental Python libraries and work on small practical AI projects.")
        if 'CN' in weak_subjects or 'CN' in critical_subjects:
            suggestions.append("Revise networking protocols, IP addressing, and OSI layer functions.")
        if 'COA' in weak_subjects or 'COA' in critical_subjects:
            suggestions.append("Practice computer architecture pipeline concepts and logic gate evaluations.")
        
        for suggestion in suggestions:
            st.markdown(f"- {suggestion}")