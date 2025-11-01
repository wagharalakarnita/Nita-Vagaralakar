import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = df = pd.read_excel("students_data.csv.xlsx")


dates = pd.date_range(end=pd.Timestamp.today(), periods=10)
attendance_records = []

for _, row in df.iterrows():
    for date in dates:
        attendance_records.append({
            "Student_ID": row["Student_ID"],
            "Name": row["Name"],
            "Date": date,
            "Attendance (%)": np.clip(np.random.normal(row["Attendance (%)"], 5), 50, 100)
        })

attendance_df = pd.DataFrame(attendance_records)

st.title("Student Performance Dashboard")
st.header(" Filters")

st.sidebar.header("Filter Options")

course_filter = st.sidebar.selectbox("Select Course", options=["All"] + sorted(df['Course'].unique().tolist()))
city_filter = st.sidebar.multiselect("Select City", options=sorted(df['City'].unique().tolist()), default=[])
min_marks = st.sidebar.slider("Minimum Marks", 
                              min_value=int(df['Marks'].min()), 
                              max_value=int(df['Marks'].max()), 
                              value=int(df['Marks'].min()))
gender_filter = st.sidebar.radio("Select Gender", options=["All", "Male", "Female"])

filtered_df = df.copy()

if course_filter != "All":
    filtered_df = filtered_df[filtered_df["Course"] == course_filter]

if city_filter:
    filtered_df = filtered_df[filtered_df["City"].isin(city_filter)]

filtered_df = filtered_df[filtered_df["Marks"] >= min_marks]

if gender_filter != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender_filter]

st.subheader(" Filtered Data")
st.dataframe(filtered_df)

st.header(" Summary Statistics")

avg_marks = round(filtered_df["Marks"].mean(), 2)
avg_attendance = round(filtered_df["Attendance (%)"].mean(), 2)
total_students = len(filtered_df)

col1, col2, col3 = st.columns(3)
col1.metric("Average Marks", avg_marks)
col2.metric("Average Attendance (%)", avg_attendance)
col3.metric("Total Students", total_students)

st.header(" Search Student")
search_name = st.text_input("Enter student name:")
if search_name:
    result = df[df["Name"].str.contains(search_name, case=False, na=False)]
    st.write(result if not result.empty else "No student found.")

st.header(" Actions")

if st.button("Show Top Performers"):
    top_students = df[df["Marks"] > 90]
    st.subheader("Top Performers (Marks > 90)")
    st.dataframe(top_students)

if st.button("Show All Data"):
    st.subheader("All Student Data")
    st.dataframe(df)

st.header("Charts")

st.subheader("Marks by Student")
st.bar_chart(filtered_df.set_index("Name")["Marks"])

st.subheader("Attendance Trend (Last 10 Days)")
selected_students = filtered_df["Name"].unique().tolist()
trend_data = attendance_df[attendance_df["Name"].isin(selected_students)]

if not trend_data.empty:
    trend_pivot = trend_data.pivot_table(
        index="Date", columns="Name", values="Attendance (%)", aggfunc="mean"
    )
    st.line_chart(trend_pivot)
else:
    st.info("No attendance data available for the selected filters.")

fig, ax = plt.subplots()
ax.hist(filtered_df["Marks"], bins=10)
ax.set_title("Distribution of Marks")
ax.set_xlabel("Marks")
ax.set_ylabel("Number of Students")
st.pyplot(fig)

st.header("🧠 Performance Feedback")

if avg_marks > 85:
    st.success("Excellent performance! ")
elif avg_marks >= 70:
    st.info("Good performance. Keep it up!")
else:
    st.warning("Needs improvement. Consider reviewing weak areas.")

st.image("c:\\Users\\Nikki\\Downloads\\kosako.jpg", caption="Powered by Streamlit", use_container_width=True)

