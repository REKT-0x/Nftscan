import streamlit as st
import json
import os
from web3 import Web3

st.set_page_config(page_title="NFT Sniper Dashboard", page_icon="🛡️")

st.title("🛡️ Personal NFT Floor Sniper")
st.write("Cross-chain NFT contract watcher using direct blockchain connections.")

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

if os.path.exists(WATCHFILE):
    with open(WATCHFILE, "r") as f:
        watchlist = json.load(f)
else:
    watchlist = []

st.subheader("📋 Add Collection Contract")

with st.form("add_form"):
    name_input = st.text_input("Project Name (e.g., ApeChain Project)")
    
    # Fully supported networks including ApeChain RPC mapping
    network_input = st.selectbox(
        "Select Network", 
        ["Ethereum", "Base", "ApeChain", "Arbitrum", "Polygon"]
    )
    
    contract_input = st.text_input("Contract Address (0x...)")
    submit = st.form_submit_button("Add to Watchlist")

    if submit and name_input and contract_input:
        watchlist.append({
            "name": name_input,
            "network": network_input,
            "contract": contract_input.strip()
        })
        with open(WATCHFILE, "w") as f:
            json.dump(watchlist, f, indent=4)
        st.success(f"Added {name_input}! (Commit changes to GitHub to save permanently)")

st.divider()

st.subheader("📊 Watchlist Status")

# Public RPC endpoints for direct chain connection (No API keys needed)
RPC_URLS = {
    "Ethereum": "https://cloudflare-eth.com",
    "Base": "https://mainnet.base.org",
    "ApeChain": "https://rpc.apechain.com/http",
    "Arbitrum": "https://arb1.arbitrum.io/rpc",
    "Polygon": "https://polygon-rpc.com"
}

if st.button("Verify Contracts Now"):
    if not watchlist:
        st.info("Your watchlist is empty.")
    else:
        for item in watchlist:
            net = item["network"]
            addr = item["contract"]
            name = item["name"]
            
            rpc = RPC_URLS.get(net)
            w3 = Web3(Web3.HTTPProvider(rpc))
            
            if w3.is_connected():
                # Verify contract exists on-chain
                code = w3.eth.get_code(Web3.to_checksum_address(addr))
                if len(code) > 2:
                    st.success(f"✅ **{name}** ({net}): Contract verified live on-chain!")
                else:
                    st.error(f"❌ **{name}** ({net}): No smart contract found at this address.")
            else:
                st.error(f"Connection failed for network: {net}")
else:
    st.info("Click the button to ping the blockchains and verify your saved contracts.")
