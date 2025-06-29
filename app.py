import streamlit as st
import json
import os
from src.pipeline_controller import run_pipeline
from src.dxf_cost_estimator import estimate_cost

st.title("💧 Waterjet AI Design Generator")

# Load catalog for dynamic options
@st.cache_data
def load_catalog():
    with open("data/catalogue.json", "r") as f:
        return json.load(f)

catalog = load_catalog()

st.sidebar.header("Design Parameters")

# Extract unique options from catalog
categories = list(set([item["category"] for item in catalog]))
styles = list(set([item["style"] for item in catalog]))
shapes = list(set([item["shape"] for item in catalog if "shape" in item]))
all_materials = []
for item in catalog:
    all_materials.extend(item["material"])
materials = list(set(all_materials))

category = st.sidebar.selectbox("Design Category", sorted(categories))
shape = st.sidebar.selectbox("Shape", sorted(shapes))
style = st.sidebar.selectbox("Design Style", sorted(styles))
material = st.sidebar.selectbox("Material", sorted(materials))

# Filter catalog based on selections
matching_designs = [
    item for item in catalog 
    if item.get("category") == category 
    and item.get("shape") == shape 
    and item.get("style") == style
    and material in item.get("material", [])
]

# Show standard sizes if available
if matching_designs and "standard_sizes" in matching_designs[0]:
    sizes = matching_designs[0]["standard_sizes"]
    size_options = [f"{size['name']}" for size in sizes]
    selected_size = st.sidebar.selectbox("Standard Size", size_options)
    
    # Display size details
    size_details = sizes[size_options.index(selected_size)]
    st.sidebar.markdown("**Size Details:**")
    for key, value in size_details.items():
        if key != "name":
            st.sidebar.text(f"{key}: {value}")

rate_per_cm = st.sidebar.number_input("Waterjet Rate (₹/cm of cut)", value=2.5, step=0.1)

# Generate improved prompt based on selection
if matching_designs:
    selected_design = matching_designs[0]
    base_prompt = selected_design["prompt_template"]
    
    if "standard_sizes" in selected_design:
        size_info = selected_design["standard_sizes"][size_options.index(selected_size)]
        # Add size information to prompt
        size_text = ", ".join([f"{k}: {v}" for k, v in size_info.items() if k != "name"])
        enhanced_prompt = f"{base_prompt}, dimensions: {size_text}, material: {material}"
    else:
        enhanced_prompt = f"{base_prompt}, material: {material}"
    
    user_prompt = st.text_area("📝 Design Description:", 
        value=enhanced_prompt, height=100)
else:
    user_prompt = st.text_area("📝 Describe your design:", 
        f"Create a {style} {category} pattern suitable for {material} inlay work")

# Display design specifications
if matching_designs:
    design = matching_designs[0]
    st.sidebar.markdown("**Design Specs:**")
    st.sidebar.text(f"Min thickness: {design['min_thickness_mm']}mm")
    st.sidebar.text(f"Max detail: {design['max_detail_mm']}mm")
    st.sidebar.text(f"Design ID: {design['id']}")

if st.button("Generate Design"):
    with st.spinner("Processing..."):
        result = run_pipeline(user_prompt)
        if isinstance(result, str):
            st.error(result)
        else:
            st.success("Design generated successfully!")
            st.image(f"data/outputs/{result['image']}", caption="AI Generated Design")

            # DXF download
            st.download_button("📥 Download DXF", 
                               data=open(f"data/outputs/{result['dxf']}", "rb").read(),
                               file_name=result['dxf'],
                               mime="application/dxf")

            # DXF validation
            if result["validation"]:
                st.warning("⚠️ DXF Validation Issues:")
                for issue in result["validation"]:
                    st.text(f"• {issue}")
            else:
                st.info("✅ DXF passed all validations.")

            # Cost Estimation
            length_cm, cost = estimate_cost(f"data/outputs/{result['dxf']}", rate_per_cm)
            st.markdown(f"### 💰 Estimated Cutting Cost")
            st.markdown(f"**Cut Length:** {length_cm:.2f} cm")
            st.markdown(f"**Estimated Cost:** ₹{cost:.2f}")
            # Generate Quotation PDF
            from src.quotation_generator import create_pdf_quotation
            pdf_path = f"data/outputs/{result['dxf'].replace('.dxf', '_quote.pdf')}"
            create_pdf_quotation(f"data/outputs/{result['image']}", 
                                 f"data/outputs/{result['dxf']}", 
                                 length_cm, cost, 
                                 pdf_path)
            st.download_button("🧾 Download Quotation PDF", 
                               data=open(pdf_path, "rb").read(), 
                               file_name=os.path.basename(pdf_path),
                               mime="application/pdf")
