import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="NFT Sniper Dashboard", page_icon="🛡️")

st.title("🛡️ Personal NFT Floor Sniper")
st.write("Manage your cross-chain watchlist using raw contract addresses.")

# --- PASSWORD PROTECTION ---
DEFAULT_PASSWORD = "mypassword123" 
password_input = st.text_input("Enter App Password:", type="password")

if password_input != DEFAULT_PASSWORD:
    st.warning("⚠️ Please enter the correct password to access your watchlist.")
    st.stop()

st.success("Access Granted!")
st.divider()

# --- WATCHLIST MANAGER ---
WATCHFILE = "watchlist.json"

if os.path.exists(WATCHFILE):
    with open("watchlist.json", "r") as f:
        watchlist = json.load(f)
else:
    watchlist = []

st.subheader("📋 Add by Contract Address (Any Network)")

with st.form("add_contract_form"):
    new_name = st.text_input("Project Name (e.g., Cool Collection)")
    
    # Expanded dropdown for Ethereum and popular L2 layers
    chain_input = st.selectbox(
        "Select Blockchain Network", 
        ["ethereum", "base", "apechain", "arbitrum", "polygon", "optimism", "blast"]
    )
    
    contract_input = st.text_input("Contract Address (e.g., 0x...)")
    submit_button = st.form_submit_button(label="Add Project")

    if submit_button and new_name and contract_input:
        watchlist.append({
            "name": new_name, 
            "chain": chain_input.lower(), 
            "contract": contract_input.strip()
        })
        with open(WATCHFILE, "w") as f:
            json.dump(watchlist, f, indent=4)
        st.success(f"Added {new_name}! (Commit changes to save)")

st.divider()

# --- LIVE FLOOR CHECKER ---
st.subheader("📊 Live Watchlist Prices")

if st.button("Check Floors Now"):
    if not watchlist:
        st.info("Your watchlist is empty. Add a project above!")
    else:
        for project in watchlist:
            name = project["name"]
            chain = project.get("chain", "ethereum")
            contract = project["contract"]
            
            # Query the multi-chain contract endpoint
            url = f"https://api.coingecko.com/api/v3/nfts/{chain}/contract/{contract}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                cg_id = data.get("id")
                if cg_id:
                    floor_url = f"https://api.coingecko.com/api/v3/nfts/{cg_id}"
                    floor_resp = requests.get(floor_url)
                    if floor_resp.status_code == 200:
                        floor_data = floor_resp.json()
                        floor = floor_data.get("floor_price", {}).get("native_currency", "N/A")
                        st.metric(label=f"{name} ({chain.upper()})", value=f"{floor} ETH")
                    else:
                        st.error(f"Found contract for {name}, but couldn't fetch floor price.")
                else:
                    st.error(f"Collection mapping not found for contract {contract}")
            else:
                st.error(f"Could not find contract for {name} on {chain}. Double check the address.")
else:
    st.info("Click the button above to pull the latest floor prices.")
