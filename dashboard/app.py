import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="AI Powered SOC Dashboard",
    layout="wide"
)

st.markdown("""
<style>

.main {
    background-color:#0E1117;
}

[data-testid="metric-container"]{
    background-color:#1E1E1E;
    border-radius:12px;
    padding:18px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.4);
}

h1{
    color:#00E5FF;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
# 🛡 AI Powered SOC Dashboard

### Real-Time Security Monitoring & Threat Detection
""")

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3064/3064197.png",
    width=90
)

st.sidebar.title("🛡 SOC Controls")

st.sidebar.markdown("---")


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "final_results.csv"

data = pd.read_csv(DATA_PATH)


st.sidebar.title("Filters")

severity = st.sidebar.multiselect(
    "Select Severity",
    options=data["severity"].unique(),
    default=data["severity"].unique()
)

filtered_data = data[
    data["severity"].isin(severity)
]

Employee = st.sidebar.text_input(
    "🔎 Search Employee ID"
)

if Employee:
    filtered_data = filtered_data[
        filtered_data["entity_id"].str.contains(
            Employee,
            case=False
        )
    ]

st.subheader("Security Events")

st.dataframe(data)

total_events = len(filtered_data)

total_attacks = len(
    filtered_data[filtered_data["label"]=="Attack"]
)

average_risk = round(
    filtered_data["final_risk_score"].mean(),
    2
)

high_alerts = len(
    filtered_data[filtered_data["severity"]=="High"]
)

high_count = len(filtered_data[filtered_data["severity"] == "High"])

if high_count > 0:
    st.error(f"🚨 {high_count} High Severity Alerts Need Immediate Investigation")
else:
    st.success("✅ No High Severity Alerts")

tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard",
    "🚨 Alerts",
    "📜 Logs"
])

st.subheader("📜 Complete Security Logs")

st.dataframe(filtered_data.head(100))

if st.checkbox("Show All Logs"):
    st.dataframe(filtered_data)
with tab1:
    st.write("Charts will be displayed here.")

with tab2:
    st.write("High-risk alerts will be displayed here.")

with tab3:
    st.write("User details will be displayed here.")

with tab2:

    st.subheader("🚨 High Severity Alerts")

    high_alerts_df = filtered_data[
        filtered_data["severity"] == "High"
    ]

    st.dataframe(
    high_alerts_df[
        [
            "timestamp",
            "entity_id",
            "department",
            "attack_type",
            "final_risk_score",
            "severity"
        ]
    ].sort_values("timestamp", ascending=False).head(20)
)

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric("🟢 Total Events",total_events)

with col2:
    st.metric("🔴 Attacks",total_attacks)

with col3:
    st.metric("🟡 Avg Risk",average_risk)

with col4:
    st.metric("🚨 High Alerts",high_alerts)

col1, col2 = st.columns(2)



with col1:

    attack_chart = px.pie(
        filtered_data,
        names="label",
        title="Attack Distribution",
        color="label",
        color_discrete_map={
            "Attack": "red",
            "Normal": "green"
        },
        template="plotly_dark"
    )

    attack_chart.update_traces(
        textinfo="percent+label"
    )

    st.plotly_chart(
        attack_chart,
        use_container_width=True
    )
    

    

with col2:

    severity_counts = (
        filtered_data["severity"]
        .value_counts()
        .reset_index()
    )

    severity_counts.columns = ["severity", "count"]

    severity_chart = px.bar(
        severity_counts,
        x="severity",
        y="count",
        color="severity",
        title="🚨 Severity Distribution",
        template="plotly_dark",
        color_discrete_map={
            "Low": "green",
            "Medium": "orange",
            "High": "red"
        }
    )

    severity_chart.update_layout(
        xaxis_title="Severity Level",
        yaxis_title="Number of Events"
    )

    severity_chart.update_traces(
        textposition="outside",
        texttemplate="%{y}"
    )

    st.plotly_chart(
        severity_chart,
        use_container_width=True
    )
col3, col4 = st.columns(2)

with col3:

    login_chart = px.histogram(
        filtered_data,
        x="login_hour",
        color="label",
        nbins=24,
        title="🕒 Login Activity by Hour",
        template="plotly_dark",
        color_discrete_map={
            "Attack": "red",
            "Normal": "green"
        }
    )

    login_chart.update_layout(
        xaxis_title="Login Hour",
        yaxis_title="Number of Events",
        bargap=0.1
    )

    st.plotly_chart(
        login_chart,
        use_container_width=True
    )

with col4:

    risk_chart = px.histogram(
        filtered_data,
        x="final_risk_score",
        color="severity",
        title="⚠ Risk Score Distribution",
        template="plotly_dark",
        color_discrete_map={
            "Low": "green",
            "Medium": "orange",
            "High": "red"
        }
    )

    risk_chart.update_layout(
        xaxis_title="Risk Score",
        yaxis_title="Number of Events",
        bargap=0.1
    )

    st.plotly_chart(
        risk_chart,
        use_container_width=True
    )

department = st.sidebar.multiselect(
    "Department",
    options=data["department"].unique(),
    default=data["department"].unique()
)

operating_system = st.sidebar.multiselect(
    "Operating System",
    options=data["operating_system"].unique(),
    default=data["operating_system"].unique()
)

browser = st.sidebar.multiselect(
    "Browser",
    options=data["browser"].unique(),
    default=data["browser"].unique()
)


filtered_data = data[
    (data["severity"].isin(severity)) &
    (data["department"].isin(department)) &
    (data["operating_system"].isin(operating_system)) &
    (data["browser"].isin(browser))
]

if Employee:
    filtered_data = filtered_data[
        filtered_data["entity_id"].str.contains(
            Employee,
            case=False,
            na=False
        )
    ]
st.subheader("🚨 High Severity Alerts")

# Filter only High severity alerts
high_alerts = filtered_data[
    filtered_data["severity"] == "High"
]

# Download button
st.download_button(
    label="📥 Download High Risk Alerts",
    data=high_alerts.to_csv(index=False),
    file_name="high_risk_alerts.csv",
    mime="text/csv"
)

# Display only important columns
st.dataframe(
    high_alerts[
        [
            "entity_id",
            "attack_type",
            "severity",
            "final_risk_score",
            "timestamp"
        ]
    ]
)


timeline = (

filtered_data

.groupby("login_hour")

.size()

.reset_index(name="Events")

)

fig = px.line(

timeline,

x="login_hour",

y="Events",

markers=True,

title="Attack Timeline",

template="plotly_dark"

)

st.plotly_chart(fig,use_container_width=True)

st.subheader("👤 Top 10 Risky Employees")
top_users = (

filtered_data

.groupby("entity_id")["final_risk_score"]

.max()

.sort_values(ascending=False)

.head(10)
.reset_index()



)






fig = px.bar(

top_users,

x="final_risk_score",

y="entity_id",

orientation="h",

color="final_risk_score",

title="Top 10 Highest Risk Users",

template="plotly_dark"

)

st.plotly_chart(fig,use_container_width=True)


st.markdown("---")

st.caption(
"AI Powered Anomaly Detection System | Developed using Python, Streamlit, Plotly & Isolation Forest"
)
