# The Handwashing Tragedy

### A data story about the deadly cost of ignoring evidence

---

## The Mystery

Vienna, 1840s. Two maternity clinics, side by side in the same hospital. Same building, same conditions, same city. Yet women were **three times more likely to die** in one clinic than the other.

Mothers knew. They begged on their knees not to be admitted to Clinic 1. Some chose to give birth in the streets rather than enter those doors. The doctors couldn't explain it. Miasma? Cosmic forces? Divine punishment?

A young Hungarian physician named Ignaz Semmelweis noticed something the others missed.

## The Discovery

Doctors in Clinic 1 performed autopsies in the morning, then delivered babies in the afternoon. Without washing their hands.

Midwives in Clinic 2 didn't perform autopsies.

Semmelweis proposed something radical: wash your hands with chlorine solution between the morgue and the maternity ward. His colleagues mocked him. The idea that *gentlemen's hands* could transmit disease was offensive.

But the data told a different story.

## The Data

This interactive visualization explores the mortality records from both clinics between 1841 and 1849. You'll see the moment handwashing was introduced in mid-1847, and what happened next.

The numbers are stark. The implications are profound. And the lessons remain urgent today.

**[→ Explore the Live Application](#)** *(link will be added after deployment)*

---

## What You'll Find

🧼 **Big picture metrics** showing the human cost of unwashed hands  
📊 **Interactive visualizations** revealing the mortality patterns  
🔬 **Side by side comparisons** between the two clinics  
💡 **Historical context** connecting past to present  

The application uses preattentive design principles to make the tragedy immediately visible: color coding for danger and safety, visual hierarchy that guides your eye to what matters, and formatting that lets you grasp the story at a glance.

---

## Tech Stack

**Built with:**
- **Streamlit** for the interactive web application
- **Pandas** for data manipulation and analysis  
- **Plotly** for dynamic, responsive visualizations

**Why these tools?** Streamlit makes data stories accessible to everyone, not just data scientists. The goal was to create something that would make you *feel* the weight of the evidence, not just see it.

---

## Run It Yourself

```bash
# Clone the repository
git clone https://github.com/wmoore012/Smash.git
cd Smash/handwashing-visualization

# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## Why This Matters

Semmelweis was right. The data proved it. Yet he was rejected by the medical establishment, lost his job, and died in an asylum at age 47.

Meanwhile, thousands of mothers continued to die from preventable infections.

This isn't just history. It's a reminder that evidence doesn't speak for itself. It needs to be seen, understood, and acted upon. Good data visualization can save lives by making the invisible visible.

---

## The Data Source

The dataset contains yearly records from Vienna General Hospital's two maternity clinics (1841-1849), tracking births, deaths, and calculated mortality rates. It's a small dataset with an enormous story.

---

## About This Project

Created as an exploration of how visual design and narrative can transform historical data into something that moves people to think differently about evidence, science, and the human cost of ignorance.

If you're a recruiter or hiring manager reading this: I believe data work should be meaningful. Numbers represent real lives, real decisions, real consequences. This project reflects my commitment to clarity, empathy, and impact in data storytelling.

---

*In memory of Dr. Ignaz Semmelweis (1818-1865) and the thousands of mothers whose deaths could have been prevented.*

🧼 **Wash your hands. Trust the science. Save lives.**

