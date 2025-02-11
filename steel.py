import streamlit as st
import pandas as pd

def calculate_materials(final_cast, rebar_comp, ferroalloys, steel_comp):
    results = {}
    required_masses = {"Rebar": 0, "FeMn": 0, "FeSi": 0, "FeCr": 0, "FeMo": 0, "Cu": 0, "Ni": 0, "Graphite": 0}
    
    rebar_mass = final_cast * 0.95
    required_masses["Rebar"] = rebar_mass
    
    Mn_from_rebar = rebar_mass * rebar_comp["Mn"] / 100
    Si_from_rebar = rebar_mass * rebar_comp["Si"] / 100
    C_from_rebar = rebar_mass * rebar_comp["C"] / 100
    
    Mn_needed = (final_cast * steel_comp["Mn"] / 100) - Mn_from_rebar
    Si_needed = (final_cast * steel_comp["Si"] / 100) - Si_from_rebar
    C_needed = (final_cast * steel_comp["C"] / 100) - C_from_rebar
    Cr_needed = (final_cast * steel_comp["Cr"] / 100)
    Mo_needed = (final_cast * steel_comp["Mo"] / 100)
    Cu_needed = (final_cast * steel_comp["Cu"] / 100)
    Ni_needed = (final_cast * steel_comp["Ni"] / 100)
    
    if Mn_needed > 0:
        required_masses["FeMn"] = Mn_needed / (ferroalloys["FeMn"]["Mn"] / 100)
        C_from_FeMn = required_masses["FeMn"] * (ferroalloys["FeMn"]["C"] / 100)
        Si_from_FeMn = required_masses["FeMn"] * (ferroalloys["FeMn"]["Si"] / 100)
        C_needed -= C_from_FeMn
        Si_needed -= Si_from_FeMn
    
    if Si_needed > 0:
        required_masses["FeSi"] = Si_needed / (ferroalloys["FeSi"]["Si"] / 100)
    if Cr_needed > 0:
        required_masses["FeCr"] = Cr_needed / (ferroalloys["FeCr"]["Cr"] / 100)
    if Mo_needed > 0:
        required_masses["FeMo"] = Mo_needed / (ferroalloys["FeMo"]["Mo"] / 100)
    if Cu_needed > 0:
        required_masses["Cu"] = Cu_needed
    if Ni_needed > 0:
        required_masses["Ni"] = Ni_needed
    if C_needed > 0:
        required_masses["Graphite"] = C_needed / 1.0  # Assuming pure graphite (100% carbon)
    
    return {k: round(v, 6) for k, v in required_masses.items()}  # Ensures small values are not rounded to zero

st.title("Steel Composition Calculator")

final_cast = st.number_input("Final Cast Requirement (kg)", min_value=1, value=10)

st.subheader("Enter Rebar Composition (% by weight)")
rebar_comp = {
    "C": st.number_input("Carbon in Rebar", value=0.25),
    "Mn": st.number_input("Manganese in Rebar", value=0.7),
    "Si": st.number_input("Silicon in Rebar", value=0.2),
    "P": st.number_input("Phosphorus in Rebar", value=0.023),
    "Al": st.number_input("Aluminum in Rebar", value=0.0015),
}

st.subheader("Enter Ferroalloy Compositions (% by weight)")
ferroalloys = {
    "FeMn": {
        "Mn": st.number_input("Mn in FeMn", value=78.0),
        "C": st.number_input("C in FeMn", value=0.5),
        "Si": st.number_input("Si in FeMn", value=1.35),
    },
    "FeSi": {"Si": st.number_input("Si in FeSi", value=70.16)},
    "FeCr": {"Cr": st.number_input("Cr in FeCr", value=60.0)},
    "FeMo": {"Mo": st.number_input("Mo in FeMo", value=59.56)},
}

st.subheader("Enter Required Steel Composition (% by weight)")
steel_comp = {
    "C": st.number_input("Carbon in Steel", value=0.22),
    "Mn": st.number_input("Manganese in Steel", value=1.4),
    "Si": st.number_input("Silicon in Steel", value=0.4),
    "P": st.number_input("Phosphorus in Steel", value=0.02),
    "Cr": st.number_input("Chromium in Steel", value=0.7),
    "Mo": st.number_input("Molybdenum in Steel", value=0.5),
    "Ni": st.number_input("Nickel in Steel", value=0.9),
    "Cu": st.number_input("Copper in Steel", value=0.5),
}

if st.button("Calculate Required Materials"):
    results = calculate_materials(final_cast, rebar_comp, ferroalloys, steel_comp)
    df = pd.DataFrame(results.items(), columns=["Material", "Required Mass (kg)"])
    st.write(df)
