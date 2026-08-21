import streamlit as st
import requests
import json
import os

# Page layout setup
st.set_page_config(page_title="NFT Sniper Dashboard", page_icon="🛡️")

st.title("🛡️ Personal NFT Floor Sniper")
st.write("Manage your watchlist and check live floors without API keys.")

# --- PASSWORD PROTECTION ---
# Set your password here or via GitHub Secrets
DEFAULT_PASSWORD = "mypassword123" 

password_input = st.text_input("Enter App Password:", type="password")

if password_input != DEFAULT_PASSWORD:
    st.warning("⚠️ Please enter the correct password to access your watchlist and sniper settings.")
    st.stop() # Stops the rest of the app from loading if password is wrong

st.success("Access Granted!")
st.divider()

# --- WATCHLIST MANAGER ---
WATCHFILE = "watchlist.json"

# Load current watchlist
if os.path.exists(WATCHFILE):
    with open(WATCHFILE, "r") as f:
        watchlist = json.load(f)
else:
    watchlist = []

st.subheader("📋 Add a New Project to Watch")

with st.form("add_project_form"):
    new_name = st.text_input("Project Name (e.g., Bored Ape)")
    new_slug = st.text_input("CoinGecko ID (e.g., boredapeyachtclub)")
    submit_button = st.form_submit_button(label="Add Project")

    if submit_button and new_name and new_slug:
        watchlist.append({"name": new_name, "coingecko_id": new_slug})
        with open(WATCHFILE, "w") as f:
            json.dump(watchlist, f, indent=4)
        st.success(f"Added {new_name} successfully! (Commit changes to save)")

st.divider()

# --- LIVE FLOOR CHECKER ---
st.subheader("📊 Live Watchlist Prices")

if st.button("Check Floors Now"):
    if not watchlist:
        st.info("Your watchlist is empty. Add a project above!")
    else:
        for project in watchlist:
            name = project["name"]
            cg_id = project["coingecko_id"]
            
            url = f"https://api.coingecko.com/api/v3/nfts/{cg_id}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                floor = data.get("floor_price", {}).get("native_currency", "N/A")
                st.metric(label=name, value=f"{floor} ETH")
            else:
                st.error(f"Could not fetch data for {name}")
else:
    st.info("Click the button above to pull the latest floor prices.")
