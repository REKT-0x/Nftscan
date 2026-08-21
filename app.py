import streamlit as st
import json
import os

st.set_page_config(page_title="NFT Sniper Dashboard", page_icon="🛡️")

st.title("🛡️ Personal NFT Watchlist")
st.write("Your active cross-chain tracking dashboard.")

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

watchlist = []
if os.path.exists(WATCHFILE):
    try:
        with open(WATCHFILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "contract" in item:
                        watchlist.append({
                            "name": item.get("name", "Unknown Project"),
                            "network": item.get("network", "Ethereum"),
                            "contract": item.get("contract")
                        })
    except Exception:
        watchlist = []

st.subheader("📋 Add New Contract")

with st.form("add_form", clear_on_submit=True):
    name_input = st.text_input("Project Name (e.g., Bored Ape)")
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
        name = item.get('name', 'Unnamed')
        net = item.get('network', 'Ethereum')
        addr = item.get('contract', '')
        
        # Generate direct explorer links based on the network selected
        net_lower = net.lower()
        if "ape" in net_lower:
            explorer_url = f"https://apescan.io/address/{addr}"
        elif "base" in net_lower:
            explorer_url = f"https://basescan.org/address/{addr}"
        elif "arbitrum" in net_lower:
            explorer_url = f"https://arbiscan.io/address/{addr}"
        elif "polygon" in net_lower:
            explorer_url = f"https://polygonscan.com/address/{addr}"
        else:
            explorer_url = f"https://etherscan.io/address/{addr}"

        with st.container():
            st.markdown(f"### **{name}** `({net})`")
            st.code(addr, language="text")
            
            # Action buttons for each item
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"[🔍 Open on Explorer]({explorer_url})", unsafe_allow_html=True)
            with col2:
                if st.button("🗑️ Delete", key=f"del_{idx}"):
                    watchlist.pop(idx)
                    with open(WATCHFILE, "w") as f:
                        json.dump(watchlist, f, indent=4)
                    st.rerun()
            st.divider()
