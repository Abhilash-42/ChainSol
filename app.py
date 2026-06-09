# app.py
import streamlit as st
import pandas as pd

# --- SELF-CONTAINED SAFE ENTERPRISE GRAPH DATA ---
SUPPLY_CHAIN_GRAPH = {
    "ports": {
        "Port of Rotterdam": {"status": "Operational", "connected_suppliers": ["GlobalTech Semiconductor", "EuroChem Corp"]},
        "Port of Shanghai": {"status": "Operational", "connected_suppliers": ["SinoChips Ltd", "Zhejiang Logistics"]},
        "Port of Kaohsiung": {"status": "Operational", "connected_suppliers": ["Taiwan Micro"]},
    },
    "suppliers": {
        "GlobalTech Semiconductor": {"location": "Netherlands", "components": ["TS-100 Microcontroller"]},
        "EuroChem Corp": {"location": "Germany", "components": ["EC-44 Industrial Catalyst"]},
        "SinoChips Ltd": {"location": "China", "components": ["SC-90 Display Driver"]},
        "Zhejiang Logistics": {"location": "China", "components": ["ZL-Packaging Material"]},
        "Taiwan Micro": {"location": "Taiwan", "components": ["TM-5 Advanced Processor"]},
    },
    "components": {
        "TS-100 Microcontroller": {"impacted_products": ["Titan Laptop Line", "Pro Tablet"]},
        "EC-44 Industrial Catalyst": {"impacted_products": ["Titan Laptop Line"]},
        "SC-90 Display Driver": {"impacted_products": ["Pro Tablet"]},
        "ZL-Packaging Material": {"impacted_products": ["Titan Laptop Line", "Pro Tablet"]},
        "TM-5 Advanced Processor": {"impacted_products": ["Titan Laptop Line"]},
    },
    "products": {
        "Titan Laptop Line": {"business_unit": "Consumer Electronics", "q3_revenue_risk": "$12M"},
        "Pro Tablet": {"business_unit": "Mobile Devices", "q3_revenue_risk": "$5M"},
    }
}

def safe_fabric_iq_lookup(disrupted_port: str):
    """Safely looks up graph dependencies without any risk of KeyErrors"""
    if disrupted_port not in SUPPLY_CHAIN_GRAPH["ports"]:
        return None
    
    impact_report = []
    suppliers = SUPPLY_CHAIN_GRAPH["ports"][disrupted_port]["connected_suppliers"]
    
    for supplier in suppliers:
        if supplier in SUPPLY_CHAIN_GRAPH["suppliers"]:
            components = SUPPLY_CHAIN_GRAPH["suppliers"][supplier]["components"]
            for component in components:
                if component in SUPPLY_CHAIN_GRAPH["components"]:
                    products = SUPPLY_CHAIN_GRAPH["components"][component]["impacted_products"]
                    for prod in products:
                        if prod in SUPPLY_CHAIN_GRAPH["products"]:
                            prod_details = SUPPLY_CHAIN_GRAPH["products"][prod]
                            impact_report.append({
                                "supplier": supplier,
                                "component": component,
                                "product": prod,
                                "unit": prod_details["business_unit"],
                                "risk": prod_details["q3_revenue_risk"]
                            })
    return impact_report

# --- STREAMLIT UI SETUP ---
st.set_page_config(page_title="chainSol: Supply Chain Risk Analyst", layout="wide")

st.title("chainSol")
st.subheader("Reasoning Agent for Global Market Disruption Mapping")
st.caption("Powered by Microsoft Fabric IQ & Foundry Reasoning Layer Simulation")

st.markdown("---")

# --- SIDEBAR: DISRUPTION INPUT ---
st.sidebar.header("Global Disruption Monitor")
st.sidebar.write("Simulate a real-world geopolitical or environmental event affecting global trade.")

selected_port = st.sidebar.selectbox(
    "Select a Disrupted Location:",
    ["Select a port...", "Port of Rotterdam", "Port of Shanghai", "Port of Kaohsiung"]
)

severity = st.sidebar.slider("Estimated Delay Severity (Weeks)", 1, 8, 3)

# --- MAIN DASHBOARD LOGIC ---
if selected_port != "Select a port...":
    st.warning(f"⚠️ **ALERT:** Geopolitical tensions/disruptions reported near **{selected_port}**. Estimating a {severity}-week bottleneck.")
    
    st.info("**Step 1: Fabric IQ Graph Lookup** — Mapping macro location to micro enterprise data...")
    impact_data = safe_fabric_iq_lookup(selected_port)
    
    if impact_data:
        df = pd.DataFrame(impact_data)
        
        # Upper dashboard metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Impacted Suppliers", len(df["supplier"].unique()))
        with col2:
            st.metric("Impacted Product Lines", len(df["product"].unique()))
        with col3:
            st.metric("Total Q3 Revenue at Risk", df["risk"].iloc[0] if len(df) > 0 else "$0")
            
        st.markdown("### Enterprise Blast Radius Data")
        st.dataframe(df, use_container_width=True)
        
        # Premium Premium UI Updates for the Reasoning Agent Layer
        st.markdown("---")
        st.markdown("### chainSol Reasoning Agent Engine")
        
        unique_products = ", ".join(df["product"].unique())
        unique_suppliers = ", ".join(df["supplier"].unique())
        unique_components = ", ".join(df["component"].unique())
        
        # Beautiful Expandable Section for the agent thought process
        with st.expander(" View Agent Multi-Step Thought Process (Foundry Layer)", expanded=True):
            st.code(f"""
1. Identify Pivot: Logistics disruption detected at {selected_port}.
2. Trace Dependencies: Tapping Fabric IQ... Connected to {unique_suppliers} supplying {unique_components}.
3. Assess Core Impact: Overlapping dependencies map to the production of: {unique_products}.
4. Quantify Risk: Cross-referencing inventory buffers. {severity}-week bottleneck creates a severe supply gap.
5. Formulate Mitigation: Activating alternative regional distribution networks and backup suppliers.
            """, language="text")

        with st.spinner("Agent generating executive action report..."):
            st.success("### 📋 Executive Disruption Report")
            
            col_left, col_right = st.columns(2)
            with col_left:
                st.markdown(f"""
                **⚠️ Core Exposure:**
                * **Business Unit:** {df['unit'].iloc[0]}
                * **Disruption Location:** {selected_port}
                * **Estimated Delay:** {severity} Weeks
                """)
            with col_right:
                st.markdown(f"""
                **📉 Financial & Resource Risk:**
                * **Total Q3 Revenue at Risk:** {df['risk'].iloc[0]}
                * **Impacted Components:** {unique_components}
                """)
            
            st.markdown("###  Automated Strategic Mitigation Directives")
            st.info(f"**1. Secondary Sourcing:** Instantly dispatching RFQ protocols to alternative pre-vetted vendors for **{unique_components}** outside the affected region.")
            st.markdown(f"> *Action Taken:* Drafted automated outreach emails to alternate vendors cataloged in the enterprise supplier graph.")
            
            st.info(f"**2. Freight Rerouting:** Recalculating transit paths to divert upcoming cargo shipments to open neighboring maritime hubs.")
            st.markdown(f"> *Action Taken:* Queried available alternative shipping lanes to minimize transit times around the bottleneck zone.")
            
    else:
        st.error("No enterprise data found mapped to this port location.")
else:
    st.info("👈 Select a disrupted port from the sidebar to activate **chainSol** and begin the reasoning analysis.")