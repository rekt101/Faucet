from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        eth_address = request.form["eth_address"]
        tweet_id = request.form["tweet_id"]
        x_user_id = request.form["x_user_id"]
        return f"Success! Transaction initiated for 0.1 MON to {eth_address}. Send your X User ID ({x_user_id}) to @dontgetrekt101 for verification."

    # Use triple quotes for multi-line string, ensure proper indentation
    html = """<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/web3@1.10.0/dist/web3.min.js"></script>
    <style>
        body {
            background-color: #1a1a1a; /* Dark base */
            font-family: 'Orbitron', sans-serif;
            color: #00f7ff; /* Neon blue text */
            text-align: center;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        h1 {
            font-size: 2.5em;
            text-shadow: 0 0 5px #00f7ff; /* Neon blue glow */
            margin-bottom: 20px;
        }
        form {
            background: rgba(0, 0, 0, 0.7); /* Darker overlay */
            padding: 15px;
            border: 1px solid #00f7ff; /* Neon blue border */
            border-radius: 5px;
            display: inline-block;
        }
        label {
            display: block;
            margin: 10px 0 5px;
        }
        input[type="text"] {
            background: #1a1a1a; /* Matches body dark */
            border: 1px solid #00f7ff; /* Neon blue border */
            color: #00f7ff; /* Neon blue text */
            padding: 5px;
            width: 200px;
            border-radius: 3px;
        }
        input[type="submit"] {
            background: #00f7ff; /* Neon blue button */
            border: none;
            padding: 5px 10px;
            color: #1a1a1a; /* Dark text on button */
            margin-top: 10px;
            cursor: pointer;
            border-radius: 3px;
        }
        input[type="submit"]:hover {
            background: #00d4e6; /* Lighter neon blue on hover */
        }
        #metamask-error {
            color: #ff0000; /* Red error text */
            display: none;
        }
    </style>
    <script>
        async function connectMetaMask() {
            if (typeof window.ethereum !== 'undefined') {
                try {
                    await window.ethereum.request({ method: 'eth_requestAccounts' });
                    alert('MetaMask connected! Enter your details and click Claim.');
                } catch (error) {
                    document.getElementById('metamask-error').style.display = 'block';
                    console.error(error);
                }
            } else {
                document.getElementById('metamask-error').style.display = 'block';
            }
        }

        async function sendTransaction(address) {
            const web3 = new Web3(window.ethereum);
            const amount = web3.utils.toWei('0.1', 'ether'); // 0.1 MON
            try {
                const tx = {
                    from: (await web3.eth.getAccounts())[0],
                    to: address,
                    value: amount,
                    gas: 21000,
                    gasPrice: web3.utils.toWei('20', 'gwei')
                };
                const txHash = await window.ethereum.request({
                    method: 'eth_sendTransaction',
                    params: [tx]
                });
                return txHash;
            } catch (error) {
                alert(`Error: ${error.message}`);
                return null;
            }
        }

        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('claimForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const eth_address = document.getElementsByName('eth_address')[0].value;
                const txHash = await sendTransaction(eth_address);
                if (txHash) {
                    fetch('/', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: `eth_address=${encodeURIComponent(eth_address)}&tweet_id=${encodeURIComponent(document.getElementsByName('tweet_id')[0].value)}&x_user_id=${encodeURIComponent(document.getElementsByName('x_user_id')[0].value)}`
                    }).then(response => response.text()).then(result => {
                        alert(result);
                    });
                }
            });
        });
    </script>
</head>
<body>
    <h1>Don't get REKT! Faucet</h1>
    <p id="metamask-error">Please install MetaMask or enable it in your browser!</p>
    <button onclick="connectMetaMask()">Connect MetaMask</button>
    <form id="claimForm" method="post">
        <label>MetaMask Address:</label><input type="text" name="eth_address"><br>
        <label>Tweet ID (your retweet):</label><input type="text" name="tweet_id"><br>
        <label>Your X User ID:</label><input type="text" name="x_user_id"><br>
        <input type="submit" value="Claim 0.1 MON">
    </form>
    <p>Follow me on <a href="https://x.com/dontgetrekt101">@dontgetrekt101</a>, click to follow!</p>
    <p>Retweet <a href="https://x.com/dontgetrekt101/status/your_promotional_tweet_id">this post</a> to qualify!</p>
</body>
</html>
"""
    return render_template_string(html)

if __name__ == "__main__":
    app.run(debug=True)