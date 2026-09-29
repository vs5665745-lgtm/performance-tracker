import streamlit as st
import pandas as pd

# -------------------------------------------------
# PERFORMANCE TRACKER
# Employee Performance Tracking Agent
# -------------------------------------------------

st.set_page_config(
    page_title="Performance Tracker",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Performance Tracker")
st.subheader("6-Month Employee Performance Analysis")

st.info(
    "Performance Tracker is a decision-support tool. "
    "It analyzes objective performance data and provides insights for manager review. "
    "It does not make promotion, termination, or disciplinary decisions."
)

# -------------------------------------------------
# SCORING FUNCTION
# -------------------------------------------------

def calculate_score(row):
    """
    Performance score:
    Productivity = 30%
    Quality      = 30%
    SLA          = 20%
    Attendance   = 10%
    Error Score  = 10%
    """

    productivity = float(row["Productivity"])
    quality = float(row["Quality"])
    sla = float(row["SLA"])
    attendance = float(row["Attendance"])
    errors = float(row["Errors"])

    # Convert errors into a positive score.
    # 0 errors = 100
    # 12 or more errors = 0
    error_score = max(0, 100 - (errors / 12 * 100))

    score = (
        productivity * 0.30
        + quality * 0.30
        + sla * 0.20
        + attendance * 0.10
        + error_score * 0.10
    )

    return round(score, 1)


# -------------------------------------------------
# PERFORMANCE BAND
# -------------------------------------------------

def performance_band(score):

    if score >= 90:
        return "🟢 Strong"

    elif score >= 80:
        return "🔵 Solid"

    elif score >= 70:
        return "🟠 Needs Attention"

    else:
        return "🔴 High Attention"


# -------------------------------------------------
# TREND
# -------------------------------------------------

def identify_trend(first_score, latest_score):

    change = latest_score - first_score

    if change >= 5:
        return "📈 Strong Improvement"

    elif change >= 2:
        return "📈 Improving"

    elif change <= -5:
        return "📉 Significant Decline"

    elif change <= -2:
        return "📉 Declining"

    else:
        return "➡️ Stable"


# -------------------------------------------------
# MANAGER RECOMMENDATION
# -------------------------------------------------

def recommendation(band, trend):

    if "Strong" in band:

        return (
            "Consider recognition, additional responsibility, "
            "stretch assignments, or peer-learning opportunities. "
            "Final decisions should remain with the manager."
        )

    elif "Solid" in band:

        return (
            "Maintain current performance and identify one metric "
            "that can be improved further."
        )

    elif "Needs Attention" in band:

        return (
            "Review the declining metrics with the employee and "
            "create a focused coaching or improvement plan."
        )

    else:

        return (
            "Manager review is recommended to understand the root "
            "causes of performance issues and identify appropriate support."
        )


# -------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------

st.header("1️⃣ Upload Employee Data")

uploaded_file = st.file_uploader(
    "Upload your Excel or CSV file",
    type=["xlsx", "xls", "csv"]
)


# -------------------------------------------------
# PROCESS DATA
# -------------------------------------------------

if uploaded_file is not None:

    try:

        # Read CSV
        if uploaded_file.name.lower().endswith(".csv"):

            data = pd.read_csv(uploaded_file)

        # Read Excel
        else:

            data = pd.read_excel(uploaded_file)


        st.success("Employee data uploaded successfully.")

        # -------------------------------------------------
        # REQUIRED COLUMNS
        # -------------------------------------------------

        required_columns = [
            "Employee_ID",
            "Employee_Name",
            "Month",
            "Productivity",
            "Quality",
            "Attendance",
            "Errors",
            "SLA"
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in data.columns
        ]

        if missing_columns:

            st.error(
                "The following required columns are missing: "
                + ", ".join(missing_columns)
            )

            st.stop()


        # -------------------------------------------------
        # CLEAN NUMERIC DATA
        # -------------------------------------------------

        numeric_columns = [
            "Productivity",
            "Quality",
            "Attendance",
            "Errors",
            "SLA"
        ]

        for column in numeric_columns:

            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )


        if data[numeric_columns].isna().any().any():

            st.error(
                "Some performance values are not valid numbers. "
                "Please check your Excel/CSV file."
            )

            st.stop()


        # -------------------------------------------------
        # CALCULATE SCORE
        # -------------------------------------------------

        data["Performance_Score"] = data.apply(
            calculate_score,
            axis=1
        )


        # -------------------------------------------------
        # DASHBOARD
        # -------------------------------------------------

        st.header("2️⃣ Performance Dashboard")

        employee_count = data["Employee_ID"].nunique()

        average_score = round(
            data["Performance_Score"].mean(),
            1
        )

        latest_month = data["Month"].iloc[-1]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Employees",
            employee_count
        )

        col2.metric(
            "Average Performance",
            str(average_score) + "%"
        )

        col3.metric(
            "Records Analyzed",
            len(data)
        )


        # -------------------------------------------------
        # EMPLOYEE ANALYSIS
        # -------------------------------------------------

        st.header("3️⃣ Six-Month Employee Analysis")

        summaries = []


        for employee_id, employee_data in data.groupby(
            "Employee_ID"
        ):

            employee_data = employee_data.copy()

            employee_name = employee_data[
                "Employee_Name"
            ].iloc[0]


            # Sort based on order in uploaded data
            employee_data = employee_data.reset_index(
                drop=True
            )


            first_score = employee_data[
                "Performance_Score"
            ].iloc[0]

            latest_score = employee_data[
                "Performance_Score"
            ].iloc[-1]


            average_employee_score = round(
                employee_data[
                    "Performance_Score"
                ].mean(),
                1
            )


            change = round(
                latest_score - first_score,
                1
            )


            band = performance_band(
                average_employee_score
            )


            trend = identify_trend(
                first_score,
                latest_score
            )


            # Average metrics
            avg_productivity = round(
                employee_data["Productivity"].mean(),
                1
            )

            avg_quality = round(
                employee_data["Quality"].mean(),
                1
            )

            avg_attendance = round(
                employee_data["Attendance"].mean(),
                1
            )

            avg_sla = round(
                employee_data["SLA"].mean(),
                1
            )

            first_errors = employee_data[
                "Errors"
            ].iloc[0]

            latest_errors = employee_data[
                "Errors"
            ].iloc[-1]


            # Strengths
            strengths = []

            if avg_productivity >= 95:
                strengths.append(
                    "High productivity"
                )

            if avg_quality >= 95:
                strengths.append(
                    "High quality"
                )

            if avg_attendance >= 98:
                strengths.append(
                    "Excellent attendance"
                )

            if avg_sla >= 95:
                strengths.append(
                    "Strong SLA performance"
                )

            if latest_errors < first_errors:
                strengths.append(
                    "Errors have reduced"
                )


            if not strengths:

                strengths.append(
                    "No major strength threshold detected"
                )


            # Watchouts
            watchouts = []

            if avg_productivity < 90:
                watchouts.append(
                    "Productivity below 90%"
                )

            if avg_quality < 90:
                watchouts.append(
                    "Quality below 90%"
                )

            if avg_sla < 90:
                watchouts.append(
                    "SLA below 90%"
                )

            if latest_errors > first_errors:
                watchouts.append(
                    "Errors have increased"
                )

            if change <= -5:
                watchouts.append(
                    "Significant performance decline"
                )


            if not watchouts:

                watchouts.append(
                    "No major watchout detected"
                )


            manager_action = recommendation(
                band,
                trend
            )


            summaries.append({

                "Employee_ID":
                    employee_id,

                "Employee_Name":
                    employee_name,

                "6M_Average_Score":
                    average_employee_score,

                "First_Month_Score":
                    first_score,

                "Latest_Month_Score":
                    latest_score,

                "6M_Change":
                    change,

                "Trend":
                    trend,

                "Performance_Band":
                    band,

                "Avg_Productivity":
                    avg_productivity,

                "Avg_Quality":
                    avg_quality,

                "Avg_Attendance":
                    avg_attendance,

                "Avg_SLA":
                    avg_sla,

                "Strengths":
                    ", ".join(strengths),

                "Watchouts":
                    ", ".join(watchouts),

                "Manager_Recommendation":
                    manager_action
            })


        summary = pd.DataFrame(
            summaries
        )


        # -------------------------------------------------
        # SUMMARY TABLE
        # -------------------------------------------------

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )


        # -------------------------------------------------
        # EMPLOYEE DETAIL
        # -------------------------------------------------

        st.header("4️⃣ Employee Deep Dive")

        selected_employee = st.selectbox(
            "Select an employee",
            summary["Employee_Name"].tolist()
        )


        employee_summary = summary[
            summary["Employee_Name"]
            == selected_employee
        ].iloc[0]


        employee_rows = data[
            data["Employee_Name"]
            == selected_employee
        ]


        # Metrics
        c1, c2, c3, c4 = st.columns(4)


        c1.metric(
            "6M Score",
            str(
                employee_summary[
                    "6M_Average_Score"
                ]
            ) + "%"
        )


        c2.metric(
            "Latest Score",
            str(
                employee_summary[
                    "Latest_Month_Score"
                ]
            ) + "%"
        )


        c3.metric(
            "6M Change",
            str(
                employee_summary[
                    "6M_Change"
                ]
            ) + "%"
        )


        c4.metric(
            "Performance",
            employee_summary[
                "Performance_Band"
            ]
        )


        # -------------------------------------------------
        # TREND CHART
        # -------------------------------------------------

        st.subheader(
            "Performance Trend"
        )


        chart_data = employee_rows[
            ["Month", "Performance_Score"]
        ].copy()


        chart_data = chart_data.set_index(
            "Month"
        )


        st.line_chart(
            chart_data
        )


        # -------------------------------------------------
        # METRIC CHART
        # -------------------------------------------------

        st.subheader(
            "Performance Metrics"
        )


        metric_chart = employee_rows[
            [
                "Month",
                "Productivity",
                "Quality",
                "Attendance",
                "SLA"
            ]
        ].copy()


        metric_chart = metric_chart.set_index(
            "Month"
        )


        st.line_chart(
            metric_chart
        )


        # -------------------------------------------------
        # AI-STYLE INSIGHT
        # -------------------------------------------------

        st.subheader(
            "Performance Tracker Insight"
        )


        st.write(
            f"**Employee:** {selected_employee}"
        )


        st.write(
            f"**Overall trend:** "
            f"{employee_summary['Trend']}"
        )


        st.write(
            f"**Performance classification:** "
            f"{employee_summary['Performance_Band']}"
        )


        st.write(
            "**Strengths:** "
            + employee_summary["Strengths"]
        )


        st.write(
            "**Watchouts:** "
            + employee_summary["Watchouts"]
        )


        st.write(
            "**Recommended manager action:** "
            + employee_summary[
                "Manager_Recommendation"
            ]
        )


        # -------------------------------------------------
        # DOWNLOAD RESULTS
        # -------------------------------------------------

        st.header("5️⃣ Export Results")


        csv_summary = summary.to_csv(
            index=False
        )


        csv_scored = data.to_csv(
            index=False
        )


        st.download_button(
            label="⬇️ Download 6-Month Summary",
            data=csv_summary,
            file_name="performance_tracker_summary.csv",
            mime="text/csv"
        )


        st.download_button(
            label="⬇️ Download Scored Employee Data",
            data=csv_scored,
            file_name="performance_tracker_scored_data.csv",
            mime="text/csv"
        )


# -------------------------------------------------
# INSTRUCTIONS WHEN NO FILE
# -------------------------------------------------

else:

    st.header("How Performance Tracker Works")

    st.markdown(
        """
        ### Step 1
        Upload your employee performance Excel/CSV file.

        ### Step 2
        Performance Tracker calculates a weighted score.

        ### Step 3
        It compares employee performance across six months.

        ### Step 4
        It identifies:
        - 📈 Improving employees
        - 📉 Declining employees
        - 🟢 Strong performers
        - 🟠 Employees needing attention
        - ⭐ Strengths
        - ⚠️ Watchouts

        ### Step 5
        It provides a manager-review recommendation.

        **Required Excel columns:**

        `Employee_ID`

        `Employee_Name`

        `Month`

        `Productivity`

        `Quality`

        `Attendance`

        `Errors`

        `SLA`

        Optional:

        `Manager_Feedback`
        """
    )
