# Cryptography & Blockchain Fundamentals

A menu-driven Python console application covering three core topics:

| # | Feature | Description |
|---|---------|-------------|
| 1 | **SHA-256 Hashing** | Hash any text message using SHA-256 |
| 2 | **Digital Signature** | Generate an RSA key pair, sign a message, verify the signature |
| 3 | **Vehicle Registration System** | Register and retrieve vehicles by number plate (no duplicates) |

---

## Requirements

- Python 3.10+
- `cryptography` library

## Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/crypto-blockchain.git
cd crypto-blockchain

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py
```

## Project Structure

```
crypto-blockchain/
├── main.py           # All application code
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Usage

When you run `main.py` you will see:

```
╔══════════════════════════════════════════════╗
║   Cryptography & Blockchain Fundamentals     ║
╠══════════════════════════════════════════════╣
║  1. SHA-256 Hashing                          ║
║  2. Digital Signature (Sign & Verify)        ║
║  3. Vehicle Registration System              ║
║  0. Exit                                     ║
╚══════════════════════════════════════════════╝
```

Enter the corresponding number to use each feature. The menu re-appears after every action.

### Feature Highlights

**SHA-256 Hashing**
- Type any message → receive its 64-character hex digest instantly.

**Digital Signature**
- Option 1: generate an RSA-2048 key pair in-session, sign a message, and optionally verify it on the spot.
- Option 2: paste a message + hex signature to verify against the session's public key.

**Vehicle Registration**
- `a` – Register a new vehicle (plate, owner, model). Duplicate plates are rejected.
- `b` – Look up a vehicle by number plate.
- `c` – List all registered vehicles in a table.

## License

MIT
