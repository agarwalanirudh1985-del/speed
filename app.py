import streamlit as st
import speedtest
import pandas as pd
import time

# 1. Dashboard Layout Settings
st.set_page_config(page_title="IRL Speed Checker", page_icon="⚡", layout="centered")

st.title("⚡ Real-Time Network Speed Checker")
st.markdown("Test your actual internet connection performance instantly using real server pings.")

# Initialize dynamic session state variables to save test histories
if "history" not in st.session_state:
    st.session_state.history = []

# 2. Trigger Action Button
if st.button("🚀 Start Speed Test", use_container_width=True):
    with st.spinner("Connecting to the closest optimal network server..."):
        try:
            # Initialize the live speedtest connection engine
            st_engine = speedtest.Speedtest()
            st_engine.get_best_server()  # Optimizes path latency mapping
            
            # Progress bar visual anchor placeholders
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step A: Latency / Ping tracking
            status_text.text("Measuring network latency (Ping)...")
            progress_bar.progress(25)
            time.sleep(0.5)
            
            # Step B: Live Download testing
            status_text.text("Testing live download speeds (Downloading sample blocks)...")
            raw_download = st_engine.download()
            download_mbps = round(raw_download / 1_000_000, 2)  # Convert bits to Mbps
            progress_bar.progress(60)
            
            # Step C: Live Upload testing
            status_text.text("Testing live upload speeds (Uploading data streams)...")
            raw_upload = st_engine.upload()
            upload_mbps = round(raw_upload / 1_000_000, 2)  # Convert bits to Mbps
            progress_bar.progress(90)
            
            # Fetch final parsed stats package
            results = st_engine.results.dict()
            ping_ms = round(results["ping"], 1)
            server_name = f"{results['server']['sponsor']} ({results['server']['name']})"
            
            # Clear loaders
            progress_bar.progress(100)
            status_text.empty()
            
            # 3. Present Real-Time Visual Metric Blocks
            st.success(f"Connected successfully via: **{server_name}**")
            
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric(label="Download Speed", value=f"{download_mbps} Mbps")
            m_col2.metric(label="Upload Speed", value=f"{upload_mbps} Mbps")
            m_col3.metric(label="Latency / Ping", value=f"{ping_ms} ms")
            
            # Save history entry snapshot
            st.session_state.history.append({
                "Timestamp": time.strftime("%H:%M:%S"),
                "Download (Mbps)": download_mbps,
                "Upload (Mbps)": upload_mbps,
                "Ping (ms)": ping_ms
            })
            
        except Exception as error_msg:
            st.error(f"Failed to execute speed check. Ensure you are connected to the internet. Details: {error_msg}")

# 4. View Network Test History Records
if st.session_state.history:
    st.markdown("---")
    st.subheader("📈 Session Run History Log")
    history_df = pd.DataFrame(st.session_state.history)
    
    # Display performance progression chart
    st.line_chart(history_df.set_index("Timestamp")[["Download (Mbps)", "Upload (Mbps)"]])
    
    # Display structured summary log table
    st.dataframe(history_df, use_container_width=True, hide_index=True)
    
    if st.button("🗑️ Clear Log History"):
        st.session_state.history = []
        st.rerun()
