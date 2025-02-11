import streamlit as st
import pandas as pd

def calculate_materials(final_cast, alloys):
    results = {"Rebar": 0, "FeMn": 0, "FeSi": 0, "FeCr": 0, "FeMo": 0, "Cu": 0, "Graphite": 0}
    
    # Composition of rebar
    rebar_composition = {"C": 0.2, "Mn": 0.7, "Si": 0.2, "Fe": "Balance"}
    
    # Calculate initial rebar mass
    rebar_mass = final_cast * 0.98  # Approximate Fe contribution
    results["Rebar"] = rebar_mass
    
    # Mn, C, and Si from rebar
    Mn_from_rebar = rebar_mass * rebar_composition["Mn"] / 100
    Si_from_rebar = rebar_mass * rebar_composition["Si"] / 100
    
    # Required elements
    Mn_needed = (final_cast * alloys["Mn"] / 100) - Mn_from_rebar
    Si_needed = (final_cast * alloys["Si"] / 100) - Si_from_rebar
    C_needed = final_cast * alloys["C"] / 100  # No C in rebar, so full addition needed
    
    # Calculate FeMn first
    if Mn_needed > 0:
        FeMn_mass = Mn_needed / (78 / 100)  # FeMn is 78% Mn
        results["FeMn"] = FeMn_mass
        
        # Carbon and Si contributions from FeMn
        C_from_FeMn = FeMn_mass * 0.5 / 100
        Si_from_FeMn = FeMn_mass * 1.35 / 100
        C_needed -= C_from_FeMn
        Si_needed -= Si_from_FeMn
    
    # Adjust Carbon using Graphite if needed
    if C_needed > 0:
        results["Graphite"] = C_needed / (100 / 100)  # Pure Graphite assumed
    
    # Adjust Silicon using FeSi if needed
    if Si_needed > 0:
        results["FeSi"] = Si_needed / (70.16 / 100)
    
    # Calculate FeCr, FeMo, and Cu
    results["FeCr"] = (final_cast * alloys["Cr"] / 100) / (60 / 100)
    results["FeMo"] = (final_cast * alloys["Mo"] / 100) / (59.56 / 100)
    results["Cu"] = final_cast * alloys["Cu"] / 100
    
    return results

# Streamlit UI
st.title("Steel Melt Material Calculator")
final_cast = st.number_input("Enter Final Cast Requirement (kg)", min_value=1.0, value=10.0)

def_input = {"C": 0.22, "Mn": 1.4, "Si": 0.4, "Cr": 0.7, "Mo": 0.5, "Cu": 0.5}
alloy_compositions = {}
for element, default in def_input.items():
    alloy_compositions[element] = st.number_input(f"{element} (%)", min_value=0.0, value=default)

if st.button("Calculate"):
    result = calculate_materials(final_cast, alloy_compositions)
    df = pd.DataFrame(result.items(), columns=["Material", "Required Mass (kg)"])
    st.table(df)
