import streamlit as st
import sys
import os

# 1. Manually add the backend directory to the Python path
# This looks at the current file's directory, goes up one level, and adds 'backend'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

if 'scan_history' not in st.session_state:
    st.session_state['scan_history'] = []
# 2. Now you can import your class normally
try:
    from breach_checker import BreachChecker
    checker = BreachChecker()
except ImportError as e:
    st.error(f"Could not find backend file: {e}")
    
# Home Page
st.title('Privacy Risk Profiler')
st.sidebar.title('Navigation')
page = st.sidebar.selectbox('Choose a Page', ['Home', 'Quick Breach Check', 'Full Scan', 'Results', 'History', 'Settings'])

# Quick Breach Check
if page == 'Quick Breach Check':
    st.header('Quick Breach Check')
    email = st.text_input('Enter your email address:')
    if st.button('Check Breach'):
        if email:
            with st.spinner('Scanning databases...'):
                # 2. Call your actual backend method
                raw_data = checker.check_email_breaches(email)

            breaches = raw_data[0] if isinstance(raw_data, list) and len(raw_data) > 0 and isinstance(raw_data[0], list) else raw_data
            result_summary = {
                "email": email,
                "count": len(breaches),
                "status": "Vulnerable" if breaches else "Safe"
            }
            # Save to history
            st.session_state['scan_history'].append(result_summary)
            if breaches:
                st.error(f'⚠️ Found {len(breaches)} breaches for: {email}')
                st.markdown("### **List of Breaches:**")
                # Convert the list into a clean bulleted string
                breach_list_md = ""
                for site in breaches:
                    breach_list_md += f"- {site}\n"
                
                st.markdown(breach_list_md)
            else:
                st.success(f'✅ No breaches found for: {email}')
        else:
            st.warning("Please enter an email address first.")

# Full Scan
# elif page == 'Full Scan':
#     st.header('Full Scan Interface')
#     scan_type = st.selectbox('Select Scan Type', ['Basic Scan', 'Deep Scan'])
#     if st.button('Start Scan'):
#         # Logic for conducting full scan (placeholder)
#         st.success(f'{scan_type} initiated!')

# Results Display
# elif page == 'Results':
#     st.header('Results Display')
#     st.write('Scan results will be displayed here.')

# History
elif page == 'History':
    st.header('📜 Scan History')
    if st.session_state['scan_history']:
        for item in reversed(st.session_state['scan_history']):
            color = "red" if item['status'] == "Vulnerable" else "green"
            st.markdown(f"- **{item['email']}**: :{color}[{item['status']}] ({item['count']} breaches found)")
    else:
        st.write("No scans performed in this session.")

# Settings
elif page == 'Settings':
    st.header('Settings')
    st.write('User settings can be adjusted here.')
    email_notification = st.checkbox('Enable Email Notifications')
    if email_notification:
        st.success('Email Notifications are enabled.')
    else:
        st.warning('Email Notifications are disabled.')
