import streamlit as st
import json
import os

st.set_page_config(page_title="NFT Sniper Dashboard", page_icon="🛡️")

st.title("🛡️ Personal NFT Watchlist")
st.write("Manage your cross-chain tracking cleanly and securely.")

# --- PASSWORD ---
DEFAULT_PASSWORD = "mypassword123"
password_input = st.text_input("Enter App Password:", type="password")

if password_input != DEFAULT_PASSWORD:
    st.warning("⚠️ Enter the correct password to continue.")
    st.stop()

st.success("Access Granted!")
st.divider()

# --- WATCHLIST FILE ---
WATCHFILE = "watchlist.json"

# Safe loading with error handling for old/corrupted formats
watchlist = []
if os.path.exists(WATCHFILE):
    try:
        with open(WATCHFILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    # Ensure all required keys exist to prevent KeyErrors
                    if isinstance(item, dict) and "contract" in item:
                        watchlist.append({
                            "name": item.get("name", "Unknown Project"),
                            "network": item.get("network", item.get("chain", "Ethereum")),
                            "contract": item.get("contract")
                        })
    except Exception:
        watchlist = []

st.subheader("📋 Add to Watchlist")

with st.form("add_form", clear_on_submit=True):
    name_input = st.text_input("Project Name (e.g., Cool Ape Project)")
    network_input = st.selectbox(
        "Select Network", 
        ["ApeChain", "Ethereum", "Base", "Arbitrum", "Polygon"]
    )
    contract_input = st.text_input("Contract Address (0x...)")
    submit = st.form_submit_button("Save Project")

    if submit and name_input and contract_input:
        watchlist.append({
            "name": name_input,
            "network": network_input,
            "contract": contract_input.strip()
        })
        with open(WATCHFILE, "w") as f:
            json.dump(watchlist, f, indent=4)
        st.success(f"Added {name_input} successfully!")
        st.rerun()

st.divider()

st.subheader("📊 Your Saved Watchlist")

if not watchlist:
    st.info("Your watchlist is currently empty.")
else:
    for idx, item in enumerate(watchlist):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{item.get('name', 'Unnamed')}** ({item.get('network', 'Ethereum')})")
            st.caption(f"`{item.get('contract', '')}`")
        with col2:
            if st.button("Delete", key=f"del_{idx}"):
                watchlist.pop(idx)
                with open(WATCHFILE, "w") as f:
                    json.dump(watchlist, f, indent=4)
                st.rerun()
