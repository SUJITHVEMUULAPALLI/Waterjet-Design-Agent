import streamlit as st
import json
import os

LIBRARY_PATH = "waterjet_prompt_library.json"

# Load prompt library
@st.cache_data
def load_library():
    if not os.path.exists(LIBRARY_PATH):
        return []
    with open(LIBRARY_PATH, "r") as f:
        return json.load(f)

def save_library(data):
    with open(LIBRARY_PATH, "w") as f:
        json.dump(data, f, indent=2)

library = load_library()

st.title("🧠 Waterjet Prompt Library")

# Sidebar filters
categories = sorted(list(set(entry['category'] for entry in library)))
styles = sorted(list(set(entry['style'] for entry in library)))
shapes = sorted(list(set(entry['shape'] for entry in library)))

selected_category = st.sidebar.selectbox("Filter by Category", ["All"] + categories)
selected_style = st.sidebar.selectbox("Filter by Style", ["All"] + styles)
selected_shape = st.sidebar.selectbox("Filter by Shape", ["All"] + shapes)

def matches(entry):
    return ((selected_category == "All" or entry['category'] == selected_category) and
            (selected_style == "All" or entry['style'] == selected_style) and
            (selected_shape == "All" or entry['shape'] == selected_shape))

filtered = [entry for entry in library if matches(entry)]

# Session state to pass selected prompt to app
if "selected_prompt" not in st.session_state:
    st.session_state["selected_prompt"] = ""

st.markdown(f"### Showing {len(filtered)} prompt(s)")

# Display prompts
for entry in filtered:
    with st.expander(f"{entry['id']} — {entry['style']} [{entry['category']}]"):
        st.markdown(f"**Shape**: {entry['shape']}")
        st.markdown(f"**Offset**: {entry['default_offset_mm']} mm")
        st.markdown(f"**Material**: {entry.get('material', '-')}")
        st.markdown(f"**Client**: {entry.get('client', '-')}")
        st.markdown(f"**Project**: {entry.get('project', '-')}")
        st.code(entry['prompt_template'], language="markdown")
        col1, col2 = st.columns(2)
        if col1.button(f"🧠 Use This Prompt", key=f"use_{entry['id']}"):
            st.session_state["selected_prompt"] = entry["prompt_template"]
            st.success("Prompt copied! Go to the design app to use it.")
        if col2.button(f"✏️ Edit", key=f"edit_{entry['id']}"):
            st.session_state["edit_entry"] = entry

# New or Edit Form
st.divider()
st.subheader("➕ Create or Edit Prompt Entry")

def reset_form():
    for key in ["new_id", "new_category", "new_shape", "new_style", "new_offset",
                "new_template", "new_material", "new_client", "new_project"]:
        if key in st.session_state:
            del st.session_state[key]

if "edit_entry" in st.session_state:
    entry = st.session_state["edit_entry"]
    st.text_input("ID", value=entry["id"], key="new_id")
    st.text_input("Category", value=entry["category"], key="new_category")
    st.text_input("Shape", value=entry["shape"], key="new_shape")
    st.text_input("Style", value=entry["style"], key="new_style")
    st.number_input("Default Offset (mm)", value=entry["default_offset_mm"], key="new_offset")
    st.text_input("Material", value=entry.get("material", ""), key="new_material")
    st.text_input("Client", value=entry.get("client", ""), key="new_client")
    st.text_input("Project", value=entry.get("project", ""), key="new_project")
    st.text_area("Prompt Template", value=entry["prompt_template"], key="new_template")
else:
    st.text_input("ID", key="new_id")
    st.text_input("Category", key="new_category")
    st.text_input("Shape", key="new_shape")
    st.text_input("Style", key="new_style")
    st.number_input("Default Offset (mm)", key="new_offset")
    st.text_input("Material", key="new_material")
    st.text_input("Client", key="new_client")
    st.text_input("Project", key="new_project")
    st.text_area("Prompt Template", key="new_template")

if st.button("💾 Save Prompt Entry"):
    new_entry = {
        "id": st.session_state["new_id"],
        "category": st.session_state["new_category"],
        "shape": st.session_state["new_shape"],
        "style": st.session_state["new_style"],
        "default_offset_mm": st.session_state["new_offset"],
        "material": st.session_state["new_material"],
        "client": st.session_state["new_client"],
        "project": st.session_state["new_project"],
        "prompt_template": st.session_state["new_template"]
    }

    # Check if ID exists to update or add
    updated = False
    for i, e in enumerate(library):
        if e["id"] == new_entry["id"]:
            library[i] = new_entry
            updated = True
            break
    if not updated:
        library.append(new_entry)

    save_library(library)
    st.success("✅ Prompt entry saved!")
    reset_form()
    st.rerun()
