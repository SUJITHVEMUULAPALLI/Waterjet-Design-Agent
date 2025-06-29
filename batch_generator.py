import streamlit as st
import json
import os
from src.pipeline_controller import run_pipeline
from src.quotation_generator import create_pdf_quotation

LIBRARY_PATH = "waterjet_prompt_library.json"
OUTPUT_ROOT = "data/outputs"

# Load prompt library
@st.cache_data
def load_library():
    with open(LIBRARY_PATH, "r") as f:
        return json.load(f)

prompt_library = load_library()
prompt_ids = [entry["id"] for entry in prompt_library]

st.title("🧩 Batch Prompt Processor")

# Multi-select prompts
selected_ids = st.multiselect("Select Prompt IDs to Process", prompt_ids)

# Metadata tags
project = st.text_input("Project Name")
client = st.text_input("Client Name")
material = st.text_input("Material")

if st.button("🚀 Run Batch"):
    if not selected_ids:
        st.warning("Please select at least one prompt.")
    else:
        with st.spinner("Generating designs..."):
            for pid in selected_ids:
                entry = next(e for e in prompt_library if e["id"] == pid)
                prompt = entry["prompt_template"]
                folder = os.path.join(OUTPUT_ROOT, project.replace(" ", "_"), pid)
                os.makedirs(folder, exist_ok=True)

                # First, generate the image file from the prompt (replace with actual image generator function)
                image_filename = generate_image_from_prompt(prompt)  # You need to implement or import this function

                # Now run the pipeline with the generated image filename
                result = run_pipeline(image_filename)
                if isinstance(result, dict):
                    image_path = f"data/outputs/{result['image']}"
                    dxf_path = f"data/outputs/{result['dxf']}"
                    pdf_path = os.path.join(folder, result['dxf'].replace(".dxf", "_quote.pdf"))

                    # Move files to organized folder
                    os.rename(image_path, os.path.join(folder, result['image']))
                    os.rename(dxf_path, os.path.join(folder, result['dxf']))

                    # Generate quotation
                    create_pdf_quotation(
                        os.path.join(folder, result['image']),
                        os.path.join(folder, result['dxf']),
                        pdf_path
                    )
                    st.success(f"{pid} generated and saved.")
                else:
                    st.error(f"Failed to generate for {pid}")
