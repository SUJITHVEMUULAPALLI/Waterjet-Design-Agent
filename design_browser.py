import streamlit as st
import os
import json

OUTPUT_DIR = "data/outputs"
LIBRARY_PATH = "waterjet_prompt_library.json"

# Load prompt library
@st.cache_data
def load_library():
    if not os.path.exists(LIBRARY_PATH):
        return []
    with open(LIBRARY_PATH, "r") as f:
        return json.load(f)

library = load_library()
prompt_dict = {entry["id"]: entry for entry in library}

st.title("🖼️ Generated Design Browser")

# Get all folders in outputs
projects = sorted([d for d in os.listdir(OUTPUT_DIR) if os.path.isdir(os.path.join(OUTPUT_DIR, d))])
selected_project = st.selectbox("Select Project", projects)

if selected_project:
    project_path = os.path.join(OUTPUT_DIR, selected_project)
    prompt_dirs = sorted([d for d in os.listdir(project_path) if os.path.isdir(os.path.join(project_path, d))])

    selected_prompts = st.multiselect("Filter by Prompt ID", prompt_dirs, default=prompt_dirs)

    for pid in selected_prompts:
        full_path = os.path.join(project_path, pid)
        image_file = next((f for f in os.listdir(full_path) if f.endswith(".png")), None)
        dxf_file = next((f for f in os.listdir(full_path) if f.endswith(".dxf")), None)
        pdf_file = next((f for f in os.listdir(full_path) if f.endswith(".pdf")), None)

        st.subheader(f"{pid} – {prompt_dict.get(pid, {}).get('style', 'Unknown')}")

        cols = st.columns([1, 2])
        if image_file:
            with cols[0]:
                st.image(os.path.join(full_path, image_file), use_column_width=True)
        with cols[1]:
            st.markdown(f"**Category**: {prompt_dict.get(pid, {}).get('category', '-')}")
            st.markdown(f"**Material**: {prompt_dict.get(pid, {}).get('material', '-')}")
            st.markdown(f"**Client**: {prompt_dict.get(pid, {}).get('client', '-')}")
            st.markdown(f"**Project**: {prompt_dict.get(pid, {}).get('project', '-')}")
            if dxf_file:
                st.download_button("⬇️ Download DXF", open(os.path.join(full_path, dxf_file), "rb").read(), file_name=dxf_file)
            if pdf_file:
                st.download_button("📄 Download Quotation PDF", open(os.path.join(full_path, pdf_file), "rb").read(), file_name=pdf_file)
