# 🚀 Waterjet Design Agent - Setup & Run Guide

## 📦 Prerequisites

### 1. Python Environment
```powershell
# Check Python version (3.8+ required)
python --version

# Create virtual environment (recommended)
python -m venv waterjet_env
waterjet_env\Scripts\activate
```

### 2. Required Software
- **Python 3.8+**
- **Inkscape** (for DXF conversion) - Download from: https://inkscape.org/
- **OpenAI API Key** - Get from: https://platform.openai.com/

## 🔧 Installation Steps

### Step 1: Install Dependencies
```powershell
# Navigate to project directory
cd "c:\Users\vemul\Downloads\waterjet_design_agent"

# Install required packages
pip install -r requirements.txt

# If streamlit is missing, install it
pip install streamlit
```

### Step 2: Environment Configuration
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 3: Verify Project Structure
```
waterjet_design_agent/
├── app.py                     # Main Streamlit app
├── .env                       # Your OpenAI API key
├── requirements.txt           # Dependencies
├── data/
│   ├── catalogue.json         # Shape catalog (✅ Updated)
│   └── outputs/               # Generated files (create if missing)
└── src/
    ├── catalogue_matcher.py   # Design matching (✅ Updated)
    ├── prompt_processor.py    # Prompt parsing (✅ Updated)
    ├── design_browser.py      # Catalog browser (✅ New)
    ├── image_generator.py
    ├── dxf_converter.py
    ├── dxf_validator.py
    ├── dxf_cost_estimator.py
    ├── quotation_generator.py
    └── pipeline_controller.py
```

## ▶️ Running the Application

### Quick Start
```powershell
# From project directory
streamlit run app.py
```

### Expected Output
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

## 🧪 Testing the New Features

### 1. Browse Available Designs
```powershell
# Run the design browser
python src/design_browser.py
```

### 2. Test Shape Selection
- Open http://localhost:8501
- Try different combinations:
  - Basic Shapes → Circle → Small (50mm)
  - Decorative → Star → Large 8-point
  - Functional → Washer → M12 Washer

### 3. Verify Material Compatibility
- Select different materials and see compatible designs
- Check that size specifications update automatically

## 🔍 Troubleshooting

### Common Issues

#### 1. Missing Dependencies
```powershell
pip install streamlit openai Pillow ezdxf python-dotenv requests
```

#### 2. OpenAI API Key Error
- Check `.env` file exists and contains valid key
- Verify no extra spaces or quotes in the key

#### 3. Inkscape Not Found
- Install Inkscape and add to system PATH
- Test: `inkscape --version`

#### 4. Port Already in Use
```powershell
streamlit run app.py --server.port 8502
```

#### 5. File Permissions
```powershell
# Create outputs directory if missing
mkdir data\outputs
```

## 📊 Testing Checklist

- [ ] Streamlit app loads without errors
- [ ] All 14 shapes appear in dropdown
- [ ] Size selection updates dimension display
- [ ] Material compatibility works
- [ ] Design specifications show in sidebar
- [ ] Prompt generation works with selections
- [ ] Design browser utility runs successfully

## 🎯 What's New in This Version

### ✅ Enhanced Catalog
- **14 shapes** across 6 categories
- **Standard sizes** for each shape
- **Material compatibility** matrix
- **Thickness recommendations**

### ✅ Improved UI
- **Dynamic dropdowns** from catalog
- **Size selection** with specifications
- **Material filtering**
- **Design preview** information

### ✅ Better Backend
- **Smart catalog matching**
- **Enhanced prompt processing**
- **Fallback logic** for design selection

## 🚀 Next Steps

1. **Test basic functionality** - Generate a simple circle
2. **Try complex designs** - Mughal medallion with marble
3. **Test functional shapes** - Washers and brackets
4. **Verify DXF generation** - Download and inspect files
5. **Check cost estimation** - Compare different sizes

## 📞 Support

If you encounter issues:
1. Check the terminal for error messages
2. Verify all dependencies are installed
3. Ensure `.env` file is properly configured
4. Run `python src/design_browser.py` to test catalog loading
5. Check file permissions in `data/outputs/` directory

---

**Ready to create precision waterjet designs! 🏭✨**
