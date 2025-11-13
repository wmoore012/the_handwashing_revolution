import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="The Handwashing Tragedy",
    page_icon="🧼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better visual hierarchy
st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        font-weight: bold;
        color: #d62728;
    }
    .medium-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .highlight-red {
        background-color: #ffebee;
        padding: 20px;
        border-left: 5px solid #d62728;
        margin: 10px 0;
    }
    .highlight-green {
        background-color: #e8f5e9;
        padding: 20px;
        border-left: 5px solid #2ca02c;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('yearly_deaths_by_clinic.csv')
    df['mortality_rate'] = (df['Deaths'] / df['Birth'] * 100).round(2)
    return df

df = load_data()

# Header Section
st.markdown("# 🧼 The Deadly Cost of Ignorance: Dr. Semmelweis's Fight for Handwashing")
st.markdown("### *When Simple Hygiene Could Have Saved Thousands of Mothers*")

st.markdown("""
In 1840s Vienna, women were **dying in childbirth at horrifying rates**—not from complications, 
but from **preventable infections** spread by doctors' unwashed hands. Dr. Ignaz Semmelweis discovered 
that **handwashing with chlorine could save lives**, yet his findings were rejected by the medical establishment. 
This is the story of **preventable tragedy** and the power of evidence-based medicine.
""")

st.markdown("---")

# Calculate key metrics
clinic1_before = df[(df['Clinic'] == 'clinic 1') & (df['Year'] < 1847)]
clinic1_after = df[(df['Clinic'] == 'clinic 1') & (df['Year'] >= 1847)]
clinic2_all = df[df['Clinic'] == 'clinic 2']

total_deaths_before = clinic1_before['Deaths'].sum()
total_deaths_after = clinic1_after['Deaths'].sum()
avg_mortality_before = clinic1_before['mortality_rate'].mean()
avg_mortality_after = clinic1_after['mortality_rate'].mean()

# Calculate lives that could have been saved
births_before = clinic1_before['Birth'].sum()
potential_deaths_if_washed = births_before * (avg_mortality_after / 100)
lives_could_have_saved = total_deaths_before - potential_deaths_if_washed

# Big Number Visualizations
st.markdown("## 💔 The Human Cost: Lives Lost to Unwashed Hands")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="⚰️ MOTHERS KILLED (Before Handwashing)",
        value=f"{total_deaths_before:,}",
        delta=None,
        help="Total deaths in Clinic 1 from 1841-1846"
    )

with col2:
    st.metric(
        label="✋ Lives Saved (After Handwashing)",
        value=f"{int(lives_could_have_saved):,}",
        delta=f"-{((avg_mortality_before - avg_mortality_after) / avg_mortality_before * 100):.0f}% mortality",
        delta_color="inverse",
        help="Estimated lives that could have been saved if handwashing was implemented from the start"
    )

with col3:
    st.metric(
        label="📉 Mortality Rate DROP",
        value=f"{avg_mortality_after:.1f}%",
        delta=f"{avg_mortality_after - avg_mortality_before:.1f}%",
        delta_color="inverse",
        help="Average mortality rate after handwashing was introduced in 1847"
    )

with col4:
    st.metric(
        label="🧼 Impact of Handwashing",
        value=f"{((avg_mortality_before - avg_mortality_after) / avg_mortality_before * 100):.0f}%",
        delta="Reduction in deaths",
        help="Percentage reduction in mortality after handwashing"
    )

st.markdown("---")

# Sidebar for interactivity
st.sidebar.markdown("## 🔍 Explore the Data")
st.sidebar.markdown("Use these controls to investigate the tragedy and triumph of handwashing.")

year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=(int(df['Year'].min()), int(df['Year'].max()))
)

show_clinics = st.sidebar.multiselect(
    "Select Clinics to Display",
    options=['clinic 1', 'clinic 2'],
    default=['clinic 1', 'clinic 2']
)

# Filter data based on selections
filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) & (df['Clinic'].isin(show_clinics))]

# Main visualizations
st.markdown("## 📊 The Evidence: Data That Should Have Changed Everything")

# Mortality Rate Over Time
st.markdown("### 🔴 Preventable Deaths: Mortality Rates Before and After Handwashing")
st.markdown("""
**The red zone shows the tragedy**: In Clinic 1 (staffed by doctors), mothers died at rates **up to 16%**—
while Clinic 2 (staffed by midwives with better hygiene) had rates as low as 2%. 
**The green zone shows the miracle**: After handwashing was introduced in mid-1847, deaths plummeted.
""")

fig_mortality = go.Figure()

for clinic in filtered_df['Clinic'].unique():
    clinic_data = filtered_df[filtered_df['Clinic'] == clinic]
    color = '#d62728' if clinic == 'clinic 1' else '#ff7f0e'
    
    fig_mortality.add_trace(go.Scatter(
        x=clinic_data['Year'],
        y=clinic_data['mortality_rate'],
        name=clinic.title(),
        mode='lines+markers',
        line=dict(width=3, color=color),
        marker=dict(size=10)
    ))

# Add vertical line for handwashing introduction
fig_mortality.add_vline(
    x=1847, 
    line_dash="dash", 
    line_color="green", 
    line_width=3,
    annotation_text="🧼 Handwashing Introduced",
    annotation_position="top"
)

fig_mortality.update_layout(
    title="Mortality Rate by Clinic (%)",
    xaxis_title="Year",
    yaxis_title="Mortality Rate (%)",
    hovermode='x unified',
    height=500,
    template="plotly_white"
)

st.plotly_chart(fig_mortality, use_container_width=True)

# Absolute Deaths Comparison
st.markdown("---")
st.markdown("### ⚰️ The Body Count: Absolute Deaths Tell a Horrifying Story")
st.markdown("""
Each bar represents **real mothers** who died giving birth. Notice the **shocking spike in 1842 and 1846**
in Clinic 1—over 500 mothers died in a single year. These deaths were **preventable**.
""")

fig_deaths = go.Figure()

for clinic in filtered_df['Clinic'].unique():
    clinic_data = filtered_df[filtered_df['Clinic'] == clinic]
    color = '#d62728' if clinic == 'clinic 1' else '#ff7f0e'

    fig_deaths.add_trace(go.Bar(
        x=clinic_data['Year'],
        y=clinic_data['Deaths'],
        name=clinic.title(),
        marker_color=color,
        text=clinic_data['Deaths'],
        textposition='outside'
    ))

# Add vertical line for handwashing introduction
fig_deaths.add_vline(
    x=1847,
    line_dash="dash",
    line_color="green",
    line_width=3,
    annotation_text="🧼 Handwashing Introduced",
    annotation_position="top"
)

fig_deaths.update_layout(
    title="Total Deaths by Year and Clinic",
    xaxis_title="Year",
    yaxis_title="Number of Deaths",
    barmode='group',
    hovermode='x unified',
    height=500,
    template="plotly_white"
)

st.plotly_chart(fig_deaths, use_container_width=True)

# Side-by-side comparison
st.markdown("---")
st.markdown("## 🔬 The Smoking Gun: Why Were Doctors Deadlier Than Midwives?")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="highlight-red">', unsafe_allow_html=True)
    st.markdown("### 🩺 Clinic 1: Doctors' Deadly Hands")
    st.markdown(f"""
    - **Staffed by**: Medical students and doctors
    - **Practice**: Performed autopsies, then delivered babies **without washing hands**
    - **Average mortality (before 1847)**: **{avg_mortality_before:.1f}%**
    - **Total deaths (1841-1846)**: **{total_deaths_before:,} mothers**
    - **Peak death rate**: **{clinic1_before['mortality_rate'].max():.1f}%** in {clinic1_before.loc[clinic1_before['mortality_rate'].idxmax(), 'Year']:.0f}
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="highlight-green">', unsafe_allow_html=True)
    st.markdown("### 🤱 Clinic 2: Midwives' Safer Care")
    st.markdown(f"""
    - **Staffed by**: Midwives
    - **Practice**: Did not perform autopsies, better hygiene practices
    - **Average mortality (1841-1846)**: **{clinic2_all[clinic2_all['Year'] < 1847]['mortality_rate'].mean():.1f}%**
    - **Total deaths (1841-1846)**: **{clinic2_all[clinic2_all['Year'] < 1847]['Deaths'].sum():,} mothers**
    - **Peak death rate**: **{clinic2_all['mortality_rate'].max():.1f}%** in {clinic2_all.loc[clinic2_all['mortality_rate'].idxmax(), 'Year']:.0f}
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Scatter plot: Births vs Deaths
st.markdown("---")
st.markdown("### 📈 The Correlation of Death: More Births, More Victims (Before Handwashing)")
st.markdown("""
Before handwashing, **more births meant more deaths** in Clinic 1. After 1847, this deadly pattern was broken.
""")

fig_scatter = px.scatter(
    filtered_df,
    x='Birth',
    y='Deaths',
    color='Clinic',
    size='mortality_rate',
    hover_data=['Year', 'mortality_rate'],
    color_discrete_map={'clinic 1': '#d62728', 'clinic 2': '#ff7f0e'},
    title="Births vs Deaths: The Deadly Relationship"
)

fig_scatter.update_layout(
    height=500,
    template="plotly_white"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# Year-by-year breakdown
st.markdown("---")
st.markdown("## 📋 Year-by-Year Breakdown: The Complete Record")

# Add mortality rate category
def categorize_mortality(rate):
    if rate < 3:
        return "✅ Safe"
    elif rate < 7:
        return "⚠️ Concerning"
    else:
        return "🔴 DEADLY"

display_df = filtered_df.copy()
display_df['Status'] = display_df['mortality_rate'].apply(categorize_mortality)
display_df['Mortality Rate (%)'] = display_df['mortality_rate']
display_df = display_df[['Year', 'Clinic', 'Birth', 'Deaths', 'Mortality Rate (%)', 'Status']]
display_df.columns = ['Year', 'Clinic', 'Births', 'Deaths', 'Mortality Rate (%)', 'Safety Status']

st.dataframe(
    display_df.sort_values(['Year', 'Clinic']),
    use_container_width=True,
    hide_index=True
)

# Call to action and lessons
st.markdown("---")
st.markdown("## 💡 The Lessons: Why This Still Matters Today")

st.markdown("""
### 🧼 **Evidence-Based Medicine Saves Lives**
Dr. Semmelweis proved that handwashing worked, yet he was **ridiculed and rejected** by the medical establishment.
His career was destroyed, and he died in an asylum. Meanwhile, **thousands continued to die** from preventable infections.

### 🔬 **Data Doesn't Lie—But People Ignore It**
The evidence was clear: handwashing reduced mortality by **over 80%**. Yet pride, tradition, and resistance to change
cost countless lives. Today, we face similar challenges with vaccine hesitancy, antibiotic resistance, and public health measures.

### ✊ **Simple Actions Have Massive Impact**
Something as simple as **washing hands** transformed medicine. During COVID-19, we saw this lesson repeated:
basic hygiene, masks, and vaccines save lives when people follow the science.

### 🌍 **The Fight Continues**
Even today, **healthcare-associated infections** kill thousands annually. Proper hand hygiene in hospitals
remains a critical—and sometimes neglected—practice. Semmelweis's fight is not over.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>In Memory of Dr. Ignaz Semmelweis (1818-1865)</strong></p>
    <p>And the thousands of mothers whose deaths could have been prevented</p>
    <p>🧼 Wash your hands. Trust the science. Save lives. 🧼</p>
</div>
""", unsafe_allow_html=True)

