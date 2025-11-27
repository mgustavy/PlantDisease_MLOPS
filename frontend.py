import streamlit as st
import requests
from PIL import Image
import os
import pandas as pd

st.set_page_config(page_title="PlantGuard", layout="wide", page_icon="🌿")

API_URL = "http://localhost:8000"

# --- Custom CSS for Modern UI ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        :root {
            --primary: #2E7D32;
            --secondary: #81C784;
            --background: #F8F9FA;
            --surface: #FFFFFF;
            --text: #1F2937;
            --text-light: #6B7280;
        }

        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
            color: var(--text);
            background-color: var(--background);
        }

        /* Card Style */
        .stCard {
            background-color: var(--surface);
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 1.5rem;
            border: 1px solid #E5E7EB;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: var(--surface);
            border-right: 1px solid #E5E7EB;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-weight: 700;
            color: #111827;
            letter-spacing: -0.025em;
        }
        
        h1 { font-size: 2.5rem; }
        h2 { font-size: 1.8rem; }
        h3 { font-size: 1.2rem; }

        /* Custom Button */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary) 0%, #1B5E20 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            letter-spacing: 0.025em;
            transition: all 0.3s ease;
            width: 100%;
            box-shadow: 0 4px 12px rgba(46, 125, 50, 0.2);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(46, 125, 50, 0.3);
        }

        /* Metrics */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
        }
        
        /* File Uploader */
        [data-testid="stFileUploader"] {
            background-color: var(--surface);
            border-radius: 12px;
            padding: 1rem;
            border: 2px dashed #E5E7EB;
        }
        
        /* Navigation Radio */
        .stRadio > label {
            background-color: transparent !important;
            padding: 10px;
            border-radius: 8px;
            transition: background 0.2s;
        }
        .stRadio > label:hover {
            background-color: #F3F4F6 !important;
        }

    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("<div style='text-align: center; margin-bottom: 2rem;'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/628/628283.png", width=80)
    st.markdown("### PlantGuard")
    st.markdown("<p style='color: #6B7280; font-size: 0.9rem;'>Plant Disease Detection</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    page = st.radio("MENU", ["Prediction", "Dashboard", "System Admin"], label_visibility="collapsed")
    st.markdown("---")
    
    st.info(" **Tip:** Ensure image is clear and focused on the leaf.")

# --- Main Content ---

if page == "Prediction":
    st.markdown("<div style='margin-bottom: 2rem;'><h1> Disease Analysis</h1><p style='color: #6B7280; font-size: 1.1rem;'>Upload a plant leaf image to detect potential diseases with high accuracy.</p></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("###  Upload Image")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Preview', use_column_width=True, output_format="PNG")
            
            if st.button("Analyze Leaf", use_container_width=True):
                with st.spinner("Analyzing patterns..."):
                    files = {"file": uploaded_file.getvalue()}
                    try:
                        response = requests.post(f"{API_URL}/predict", files=files)
                        if response.status_code == 200:
                            st.session_state.result = response.json()
                        else:
                            st.error("Analysis failed. Please try again.")
                    except Exception as e:
                        st.error(f"Connection error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if 'result' in st.session_state:
            res = st.session_state.result
            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            st.markdown("### Analysis Results")
            
            # Result Header
            color = "#2E7D32" if res['class'] == "Healthy" else "#D32F2F"
            st.markdown(f"""
                <div style="background-color: {color}15; padding: 1.5rem; border-radius: 12px; border-left: 6px solid {color}; margin-bottom: 1.5rem;">
                    <h2 style="color: {color}; margin:0;">{res['class']}</h2>
                    <p style="margin:0; color: #6B7280;">Confidence Score</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Metrics
            m1, m2 = st.columns(2)
            with m1:
                st.metric("Confidence", f"{res['confidence']:.1%}")
            with m2:
                st.metric("Model Version", "v2.1.0")
                
            st.markdown("#### Recommendations")
            if res['class'] == "Healthy":
                st.success("✅ Plant appears healthy. Continue regular care.")
            elif res['class'] == "Powdery":
                st.warning("⚠️ **Powdery Mildew Detected**\n- Isolate plant immediately.\n- Apply fungicide.\n- Improve air circulation.")
            elif res['class'] == "Rust":
                st.error("🚨 **Rust Detected**\n- Remove infected leaves.\n- Avoid overhead watering.\n- Apply copper-based fungicide.")
                
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Placeholder
            st.markdown("""
                <div class="stCard" style="text-align: center; padding: 4rem 2rem; color: #9CA3AF;">
                    <h3 style="color: #D1D5DB;">No Analysis Yet</h3>
                    <p>Upload an image to see results here</p>
                </div>
            """, unsafe_allow_html=True)

elif page == "Dashboard":
    st.title(" Analytics Dashboard")
    
    # Mock Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Scans", "1,248", "+12%")
    with c2: st.metric("Healthy Rate", "68%", "+5%")
    with c3: st.metric("Disease Rate", "32%", "-2%")
    with c4: st.metric("Avg Confidence", "94.2%", "+0.8%")
    
    st.markdown("### Class Distribution")
    data_dir = "data/train"
    if os.path.exists(data_dir):
        classes = [c for c in os.listdir(data_dir) if not c.startswith('.')]
        counts = {c: len(os.listdir(os.path.join(data_dir, c))) for c in classes}
        df = pd.DataFrame.from_dict(counts, orient='index', columns=['Count'])
        st.bar_chart(df, color="#2E7D32")
    else:
        st.warning("Data directory not found.")

elif page == "System Admin":
    st.title(" System Administration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### System Status")
        try:
            health = requests.get(f"{API_URL}/").json()
            st.success(f" API Online: {health}")
        except:
            st.error(" API Offline")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown("### Model Management")
        if st.button(" Retrain Model"):
            try:
                res = requests.post(f"{API_URL}/retrain")
                st.info(res.json()["message"])
            except:
                st.error("Failed to trigger retraining")
        st.markdown('</div>', unsafe_allow_html=True)
