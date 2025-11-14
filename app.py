import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# The Handwashing Revolution - Data Visualization
# Vienna General Hospital Mortality Data (1841-1849)

# Page configuration
st.set_page_config(
    page_title="The Handwashing Revolution",
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
    .highlight-impact {
        background-color: #e3f2fd;
        padding: 30px;
        border-left: 8px solid #1976d2;
        margin: 20px 0;
        text-align: center;
    }
    .huge-number {
        font-size: 80px !important;
        font-weight: bold;
        color: #1976d2;
        line-height: 1;
        margin: 10px 0;
    }
    .impact-label {
        font-size: 24px !important;
        font-weight: bold;
        color: #333;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file in the same directory
    csv_path = os.path.join(script_dir, 'yearly_deaths_by_clinic.csv')
    df = pd.read_csv(csv_path)
    df['mortality_rate'] = (df['Deaths'] / df['Birth'] * 100).round(2)
    return df

df = load_data()

# Header Section
st.markdown("# 💔 When Unwashed Hands Killed More Mothers Than Disease")
st.markdown("### The Deadly Cost of Ignoring Evidence")

st.markdown("📍 **Location: Vienna, 1847.**")
st.markdown("")

st.markdown("""
Mothers are dying in childbirth at horrifying rates. Not from complications—from infections spread by doctors'
unwashed hands. One physician, Dr. Ignaz Semmelweis, has the data: **handwashing reduces deaths by 80%**. The medical establishment's
response? Mockery. Rejection. Outrage at the suggestion that *gentlemen's hands* could kill.

**Thousands of preventable deaths.** Clear evidence ignored. Institutional pride over human lives.

**This dashboard shows what happened** when one clinic finally started washing hands in 1847—and what it cost to wait.
The pattern repeats today: healthcare infections kill thousands annually while evidence sits unused.
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
st.markdown("## 💔 The Evidence: What the Data Revealed (1841-1849)")

# Highlight the most important statistic - 81% reduction
reduction_pct = ((avg_mortality_before - avg_mortality_after) / avg_mortality_before * 100)
st.markdown(f"""
<div class="highlight-impact">
    <div style="font-size: 20px; color: #666; margin-bottom: 10px;">🧼 Impact of Handwashing</div>
    <div class="huge-number">{reduction_pct:.0f}%</div>
    <div class="impact-label">Reduction in Deaths</div>
    <div style="font-size: 16px; color: #666; margin-top: 15px;">
        When doctors started washing their hands with chlorine solution in mid-1847,<br>
        the mortality rate dropped by more than four-fifths.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# Two key statistics with improved formatting
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 60px; font-weight: bold; color: #d62728; line-height: 1;">{total_deaths_before:,}</div>
        <div style="font-size: 18px; font-weight: bold; color: #333; margin-top: 10px;">⚰️ MOTHERS KILLED</div>
        <div style="font-size: 14px; color: #666; margin-top: 5px;">(Before Handwashing, 1841-1846)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 60px; font-weight: bold; color: #2ca02c; line-height: 1;">{int(lives_could_have_saved):,}</div>
        <div style="font-size: 18px; font-weight: bold; color: #333; margin-top: 10px;">✋ LIVES COULD HAVE BEEN SAVED</div>
        <div style="font-size: 14px; color: #666; margin-top: 5px;">(If handwashing started in 1841)</div>
    </div>
    """, unsafe_allow_html=True)

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
**Doctors' unwashed hands after autopsies caused 16% mortality.** Midwives (no autopsies): 2%.
After handwashing started in mid-1847, the death rate collapsed. The evidence was undeniable.
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

# New comparison visualization section
st.markdown("---")
st.markdown("## 🔄 Side-by-Side Comparison: Doctors vs Midwives")
st.markdown("""
This visualization makes the stark difference between the two clinics impossible to miss.
**Notice:** Clinic 1 (Doctors) shows deadly mortality rates before 1847, while Clinic 2 (Midwives) remained consistently safer.
""")

# Back-to-back horizontal bar chart
st.markdown("### 📊 Back-to-Back Mortality Comparison")

# Prepare data for back-to-back chart
comparison_df = filtered_df.copy()

# Add safety status for color coding
def categorize_mortality(rate):
    if rate < 3:
        return "✅ Safe"
    elif rate < 7:
        return "⚠️ Concerning"
    else:
        return "🔴 DEADLY"

comparison_df['Safety Status'] = comparison_df['mortality_rate'].apply(categorize_mortality)

# Create separate dataframes for each clinic
clinic1_data = comparison_df[comparison_df['Clinic'] == 'clinic 1'].sort_values('Year')
clinic2_data = comparison_df[comparison_df['Clinic'] == 'clinic 2'].sort_values('Year')

# Create the back-to-back bar chart
fig_comparison = go.Figure()

# Define colors for safety status
color_map = {
    "✅ Safe": "#2ca02c",
    "⚠️ Concerning": "#ff7f0e",
    "🔴 DEADLY": "#d62728"
}

# Add Clinic 1 bars (extending to the left - negative values)
for status in ["🔴 DEADLY", "⚠️ Concerning", "✅ Safe"]:
    clinic1_subset = clinic1_data[clinic1_data['Safety Status'] == status]
    if not clinic1_subset.empty:
        fig_comparison.add_trace(go.Bar(
            name=f'Clinic 1 - {status}',
            y=clinic1_subset['Year'],
            x=-clinic1_subset['mortality_rate'],  # Negative for left side
            orientation='h',
            marker=dict(color=color_map[status]),
            text=clinic1_subset['mortality_rate'].apply(lambda x: f'{x:.1f}%'),
            textposition='inside',
            hovertemplate='<b>Clinic 1 (Doctors)</b><br>Year: %{y}<br>Mortality: %{text}<extra></extra>',
            showlegend=True
        ))

# Add Clinic 2 bars (extending to the right - positive values)
for status in ["🔴 DEADLY", "⚠️ Concerning", "✅ Safe"]:
    clinic2_subset = clinic2_data[clinic2_data['Safety Status'] == status]
    if not clinic2_subset.empty:
        fig_comparison.add_trace(go.Bar(
            name=f'Clinic 2 - {status}',
            y=clinic2_subset['Year'],
            x=clinic2_subset['mortality_rate'],  # Positive for right side
            orientation='h',
            marker=dict(color=color_map[status]),
            text=clinic2_subset['mortality_rate'].apply(lambda x: f'{x:.1f}%'),
            textposition='inside',
            hovertemplate='<b>Clinic 2 (Midwives)</b><br>Year: %{y}<br>Mortality: %{text}<extra></extra>',
            showlegend=True
        ))

# Add a vertical line at x=0 (center axis)
fig_comparison.add_vline(x=0, line_width=2, line_color="black")

# Add horizontal line at 1847 to mark handwashing introduction
fig_comparison.add_hline(
    y=1847,
    line_dash="dash",
    line_color="green",
    line_width=3,
    annotation_text="🧼 Handwashing Introduced (Clinic 1)",
    annotation_position="right"
)

# Update layout
fig_comparison.update_layout(
    title="Mortality Rate Comparison: Doctors (Left) vs Midwives (Right)",
    xaxis_title="← Clinic 1 (Doctors) | Mortality Rate (%) | Clinic 2 (Midwives) →",
    yaxis_title="Year",
    barmode='overlay',
    height=600,
    template="plotly_white",
    xaxis=dict(
        tickvals=[-20, -15, -10, -5, 0, 5, 10, 15, 20],
        ticktext=['20%', '15%', '10%', '5%', '0%', '5%', '10%', '15%', '20%'],
        range=[-20, 20]
    ),
    yaxis=dict(
        dtick=1,
        autorange='reversed'  # Years from top to bottom
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)

st.plotly_chart(fig_comparison, use_container_width=True)

# Parallel tables comparison
st.markdown("### 📋 Detailed Data: Side-by-Side Tables")
st.markdown("""
The tables below show the complete data for both clinics. Notice how the **Safety Status** columns meet in the middle,
making it easy to compare the safety of each clinic year by year.
""")

# Prepare data for parallel tables
table_df = filtered_df.copy()
table_df['Safety Status'] = table_df['mortality_rate'].apply(categorize_mortality)
table_df['Era'] = table_df.apply(
    lambda row: '🧼 After' if row['Year'] >= 1847 and row['Clinic'] == 'clinic 1' else 'Before',
    axis=1
)

# Split into two clinics
clinic1_table = table_df[table_df['Clinic'] == 'clinic 1'].sort_values('Year')
clinic2_table = table_df[table_df['Clinic'] == 'clinic 2'].sort_values('Year')

# Create the two tables side by side
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### 👨‍⚕️ Clinic 1 (Doctors)")
    # Prepare Clinic 1 table with specific column order
    clinic1_display = clinic1_table[['Year', 'mortality_rate', 'Era', 'Safety Status']].copy()
    clinic1_display.columns = ['Year', 'Mortality Rate (%)', 'Era', 'Safety Status']
    clinic1_display['Mortality Rate (%)'] = clinic1_display['Mortality Rate (%)'].round(1)

    st.dataframe(
        clinic1_display,
        use_container_width=True,
        hide_index=True,
        height=400
    )

with col_right:
    st.markdown("#### 👩‍⚕️ Clinic 2 (Midwives)")
    # Prepare Clinic 2 table with REVERSED column order (mirror effect)
    clinic2_display = clinic2_table[['Safety Status', 'Era', 'mortality_rate', 'Year']].copy()
    clinic2_display.columns = ['Safety Status', 'Era', 'Mortality Rate (%)', 'Year']
    clinic2_display['Mortality Rate (%)'] = clinic2_display['Mortality Rate (%)'].round(1)

    st.dataframe(
        clinic2_display,
        use_container_width=True,
        hide_index=True,
        height=400
    )

# Year-by-year breakdown
st.markdown("---")
st.markdown("## 📋 Year-by-Year Breakdown: The Complete Record")
st.markdown("""
**🧼 Key Milestone:** Handwashing with chlorine solution was introduced in **mid-1847** at Clinic 1.
Notice the dramatic drop in mortality rate for Clinic 1 starting in 1847.
""")

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

# Add a marker column to highlight when handwashing started
display_df['Handwashing Era'] = display_df.apply(
    lambda row: '🧼 After Handwashing' if row['Year'] >= 1847 and row['Clinic'] == 'clinic 1' else 'Before Handwashing',
    axis=1
)

display_df = display_df[['Year', 'Clinic', 'Birth', 'Deaths', 'Mortality Rate (%)', 'Status', 'Handwashing Era']]
display_df.columns = ['Year', 'Clinic', 'Births', 'Deaths', 'Mortality Rate (%)', 'Safety Status', 'Era']

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
His career was destroyed, and he died in an asylum at age 47—**before his ideas were accepted**. Meanwhile, **thousands continued to die**
from preventable infections for decades.

**Why did this injustice happen?** The medical establishment's rejection wasn't based on science—it was driven by human biases and institutional failures:

- **Pride & Ego:** Doctors couldn't accept that their "gentlemen's hands" could kill. Admitting the truth meant admitting they had been killing patients.
- **Status Quo Bias:** The medical establishment had always done things a certain way. Change threatened their authority and expertise.
- **Authority Bias:** Senior physicians rejected the evidence because it came from a younger, less prestigious doctor. Hierarchy mattered more than data.
- **Cognitive Dissonance:** Accepting handwashing meant confronting the horrifying reality that they had caused thousands of preventable deaths.
- **Institutional Inertia:** Medical schools, hospitals, and professional societies resisted change to protect their reputations and avoid accountability.

These weren't evil people—they were smart, educated professionals trapped by the same mental biases we all face.

### 🤔 **Reflective Questions: Protect Yourself from These Biases**

Ask yourself these questions to avoid repeating history:

1. **Am I rejecting evidence because it threatens my identity or expertise?**
   *When data contradicts what I believe or how I've always done things, do I examine the evidence objectively—or do I defend my position?*

2. **Am I dismissing ideas based on who presents them rather than their merit?**
   *Do I give less weight to insights from people who are younger, less credentialed, or outside my "tribe"—even when their data is solid?*

3. **Am I prioritizing institutional loyalty or personal comfort over truth and impact?**
   *When I see evidence of harm or inefficiency, do I speak up and push for change—or do I stay silent to avoid conflict or protect the status quo?*

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

