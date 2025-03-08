from flask import Flask, request, render_template_string
from web3 import Web3
import os

app = Flask(__name__)

# Connect to Monad Testnet
MONAD_TESTNET_RPC = "https://testnet-rpc.monad.xyz"
web3 = Web3(Web3.HTTPProvider(MONAD_TESTNET_RPC))

if not web3.is_connected():
    raise Exception("Cannot connect to Monad Testnet!")

# Wallet settings
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "a5a5412f6e045c93c67917ed9bd0c7e0555008d45c5c2257e2e59aa88bd8b70")
SENDER_ADDRESS = "0xFCcf2c16eB1e9111244af8F798b5b20C8a4b483F"

# Promotional tweet settings
EXPECTED_TWEET_ID = "1234567890123456789"  # Replace with your actual promotional tweet ID
PROMOTIONAL_TWEET_URL = f"https://x.com/dontgetrekt101/status/{EXPECTED_TWEET_ID}"

# Function to send MON
def send_mon(recipient_address):
    try:
        account = web3.eth.account.from_key(PRIVATE_KEY)
        if account.address.lower() != SENDER_ADDRESS.lower():
            raise ValueError("Private key does not match sender address!")
        nonce = web3.eth.get_transaction_count(SENDER_ADDRESS)
        amount_in_wei = web3.to_wei(0.1, 'ether')  # 0.1 MON
        gas_price = web3.eth.gas_price
        gas_limit = 21000

        tx = {
            'nonce': nonce,
            'to': recipient_address,
            'value': amount_in_wei,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'chainId': 512  # Monad Testnet Chain ID
        }

        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return web3.to_hex(tx_hash)
    except Exception as e:
        return f"Error sending MON: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    if request.method == "POST":
        eth_address = request.form["eth_address"]
        x_username = request.form["x_username"]
        tweet_id = request.form["tweet_id"]

        if not web3.is_address(eth_address):
            message = "Invalid MetaMask address!"
        elif not x_username.startswith("@"):
            message = "Invalid X username! It must start with @ (e.g., @yourusername)."
        elif not tweet_id.isdigit():
            message = "Invalid Tweet ID! It must be a number. Check the promotional tweet link."
        elif tweet_id != EXPECTED_TWEET_ID:
            message = f"Invalid Tweet ID! You must retweet the promotional tweet (ID: {EXPECTED_TWEET_ID})."
        else:
            # Automatically process the claim if all validations pass
            tx_hash = send_mon(eth_address)
            if "Error" in tx_hash:
                message = tx_hash
            else:
                message = f"Transaction sent! Tx Hash: {tx_hash}. Thank you for following and retweeting!"

    html = """<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/web3@1.10.0/dist/web3.min.js"></script>
    <style>
        body { background-color: #1a1a1a; font-family: 'Orbitron', sans-serif; color: #00f7ff; text-align: center; margin: 0; padding: 20px; min-height: 100vh; display: flex; flex-direction: column; justify-content: center; }
        h1 { font-size: 2.5em; text-shadow: 0 0 5px #00f7ff; margin-bottom: 20px; }
        form { background: rgba(0, 0, 0, 0.7); padding: 15px; border: 1px solid #00f7ff; border-radius: 5px; display: inline-block; }
        label { display: block; margin: 10px 0 5px; }
        input[type="text"] { background: #1a1a1a; border: 1px solid #00f7ff; color: #00f7ff; padding: 5px; width: 200px; border-radius: 3px; }
        input[type="submit"] { background: #00f7ff; border: none; padding: 5px 10px; color: #1a1a1a; margin-top: 10px; cursor: pointer; border-radius: 3px; }
        input[type="submit"]:hover { background: #00d4e6; }
        #metamask-error { color: #ff0000; display: none; }
        .message { margin-top: 20px; color: #ff0000; }
        .instructions { font-size: 0.9em; color: #00d4e6; margin-top: 10px; text-align: left; }
        .instructions a { color: #00f7ff; text-decoration: underline; }
    </style>
    <script>
        async function connectMetaMask() {
            if (typeof window.ethereum !== 'undefined') {
                try {
                    await window.ethereum.request({ method: 'eth_requestAccounts' });
                    const web3 = new Web3(window.ethereum);
                    const accounts = await web3.eth.getAccounts();
                    document.getElementsByName('eth_address')[0].value = accounts[0];
                    alert('MetaMask connected! Enter your details and click Claim.');
                } catch (error) {
                    document.getElementById('metamask-error').style.display = 'block';
                    console.error(error);
                }
            } else {
                document.getElementById('metamask-error').style.display = 'block';
            }
        }
    </script>
</head>
<body>
    <h1>Don't get REKT! Faucet</h1>
    <p id="metamask-error">Please install MetaMask or enable it in your browser!</p>
    <button onclick="connectMetaMask()">Connect MetaMask</button>
    <form id="claimForm" method="post">
        <label>MetaMask Address:</label><input type="text" name="eth_address" required><br>
        <label>Your X Username:</label><input type="text" name="x_username" required placeholder="@yourusername"><br>
        <label>Tweet ID (your retweet):</label><input type="text" name="tweet_id" required><br>
        <div class="instructions">
            <strong>Instructions:</strong><br>
            - <strong>X Username:</strong> Enter your X username starting with @ (e.g., @yourusername).<br>
            - <strong>Tweet ID:</strong> Retweet the promotional tweet below. Copy the number after '/status/' (e.g., 1234567890123456789) from the tweet URL and paste it here.<br>
            - You must follow @dontgetrekt101 and retweet to qualify.<br>
        </div>
        <input type="submit" value="Claim 0.1 MON">
    </form>
    <p>Follow me on <a href="https://x.com/dontgetrekt101" target="_blank" rel="noopener noreferrer">@dontgetrekt101</a> and retweet to qualify!</p>
    <p>Retweet <a href="{{ promotional_tweet_url }}" target="_blank" rel="noopener noreferrer">this post</a> to qualify!</p>
    <p class="message">{{ message }}</p>
</body>
</html>
"""
    return render_template_string(html, message=message, promotional_tweet_url=PROMOTIONAL_TWEET_URL)

if __name__ == "__main__":
    app.run(debug=True)