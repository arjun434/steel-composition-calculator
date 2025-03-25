import streamlit as st

# Function to calculate alloy additions
def calculate_alloy_addition(target_weight, final_composition, base_composition, alloy_compositions):
    alloy_addition = {}
    base_weight = target_weight * 0.95  # Assuming base metal contributes 95%
    
    for element, target_pct in final_composition.items():
        target_amount = (target_pct / 100) * target_weight
        base_amount = (base_composition.get(element, 0) / 100) * base_weight
        required_addition = target_amount - base_amount
        
        if required_addition > 0 and element in alloy_compositions:
            alloy_info = alloy_compositions[element]
            alloy_pct = alloy_info["percentage"] / 100
            alloy_addition[alloy_info["alloy"]] = required_addition / alloy_pct
    
    return alloy_addition

# Streamlit UI with a funky design
st.set_page_config(page_title="Alloy Addition Calculator", page_icon="🔥", layout="centered")
st.markdown("""
    <style>
        body {
            background-color: #1e1e2e;
            color: #f8f8f2;
            font-family: 'Comic Sans MS', cursive, sans-serif;
        }
        .stApp {
            background-color: #1e1e2e;
        }
        h1 {
            text-align: center;
            color: #ff79c6;
            font-size: 40px;
        }
        .stButton>button {
            background-color: #50fa7b;
            color: #282a36;
            font-size: 18px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔥 Alloy Addition Calculator 🔥")

# User Inputs
target_weight = st.number_input("💎 Enter total cast weight (grams):", min_value=0.0, value=5000.0, step=100.0)
copper_content = st.number_input("🛠 Enter desired Cu composition (%):", min_value=0.0, max_value=10.0, value=0.4, step=0.1)

# Fixed Rebar Composition
rebar_composition = {
    "C": 0.2,
    "Mn": 0.7,
    "Si": 0.2
}

final_composition = {
    "C": 0.22,
    "Mn": 1.4,
    "Si": 0.4,
    "Cr": 0.7,
    "Mo": 0.5,
    "Ni": 0.9,
    "Cu": copper_content,
    "Fe": 95.48 - (copper_content - 0.4)  # Adjusting Fe composition dynamically
}

alloy_compositions = {
    "C": {"alloy": "C (Graphite)", "percentage": 100},
    "Mn": {"alloy": "Fe-Mn", "percentage": 78},
    "Si": {"alloy": "Fe-Si", "percentage": 70.16},
    "Cr": {"alloy": "Fe-Cr", "percentage": 60},
    "Mo": {"alloy": "Fe-Mo", "percentage": 59.56},
    "Ni": {"alloy": "Ni", "percentage": 100},
    "Cu": {"alloy": "Cu", "percentage": 100}
}

# Perform Calculation
alloy_addition = calculate_alloy_addition(target_weight, final_composition, rebar_composition, alloy_compositions)

total_alloy_weight = sum(alloy_addition.values())
base_metal_weight = target_weight - total_alloy_weight

# Display Results
st.markdown("### 🎯 Alloy additions required (grams):")
for alloy, amount in alloy_addition.items():
    st.success(f"{alloy}: {amount:.2f}g")

st.markdown(f"### ⚡ Total rebar addition: **{base_metal_weight:.2f}g**")

st.markdown("---")
st.markdown("👨‍🔬 Built using Streamlit by Arjun Rai")
