"""
Cryptography and Blockchain Fundamentals
Menu-driven console application
"""

import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature


# ─────────────────────────────────────────────
#  Module 1 – SHA-256 Hashing
# ─────────────────────────────────────────────

def sha256_hash(message: str) -> str:
    """Return the SHA-256 hex digest of *message*."""
    return hashlib.sha256(message.encode()).hexdigest()


def handle_hashing():
    print("\n── SHA-256 Hashing ──")
    message = input("Enter message to hash: ").strip()
    if not message:
        print("[!] Message cannot be empty.")
        return
    digest = sha256_hash(message)
    print(f"\nMessage : {message}")
    print(f"SHA-256 : {digest}")


# ─────────────────────────────────────────────
#  Module 2 – Digital Signature
# ─────────────────────────────────────────────

# Key pair is generated once per session and reused
_private_key = None
_public_key  = None


def get_or_generate_keys():
    global _private_key, _public_key
    if _private_key is None:
        print("\n[*] Generating RSA-2048 key pair …")
        _private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        _public_key = _private_key.public_key()
        print("[✓] Key pair generated.")
    return _private_key, _public_key


def sign_message(private_key, message: str) -> bytes:
    return private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )


def verify_signature(public_key, message: str, signature: bytes) -> bool:
    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False


def handle_digital_signature():
    print("\n── Digital Signature ──")
    print("1. Generate key pair & sign a message")
    print("2. Verify a signed message")
    choice = input("Select option (1/2): ").strip()

    if choice == "1":
        private_key, public_key = get_or_generate_keys()
        message = input("Enter message to sign: ").strip()
        if not message:
            print("[!] Message cannot be empty.")
            return
        signature = sign_message(private_key, message)
        # Display public key (PEM)
        pub_pem = public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()
        print(f"\nMessage   : {message}")
        print(f"Signature : {signature.hex()[:64]}…  (truncated for display)")
        print(f"\nPublic Key (PEM):\n{pub_pem}")
        print("[✓] Message signed successfully.")

        # Immediately offer to verify
        verify_now = input("Verify this signature now? (y/n): ").strip().lower()
        if verify_now == "y":
            valid = verify_signature(public_key, message, signature)
            status = "✅ VALID" if valid else "❌ INVALID"
            print(f"Signature status: {status}")

    elif choice == "2":
        private_key, public_key = get_or_generate_keys()
        message = input("Enter the original message: ").strip()
        sig_hex = input("Enter the signature (hex): ").strip()
        try:
            signature = bytes.fromhex(sig_hex)
        except ValueError:
            print("[!] Invalid hex string.")
            return
        valid = verify_signature(public_key, message, signature)
        status = "✅ VALID – signature matches the message." if valid else "❌ INVALID – signature does NOT match."
        print(f"\nVerification result: {status}")
    else:
        print("[!] Invalid option.")


# ─────────────────────────────────────────────
#  Module 3 – Vehicle Registration System
# ─────────────────────────────────────────────

vehicle_registry: dict[str, dict] = {}   # { plate: {owner, model} }


def normalise_plate(plate: str) -> str:
    """Upper-case and strip whitespace for consistent key storage."""
    return plate.upper().strip()


def register_vehicle():
    print("\n── Register Vehicle ──")
    plate = normalise_plate(input("Enter Number Plate : ").strip())
    if not plate:
        print("[!] Number plate cannot be empty.")
        return
    if plate in vehicle_registry:
        print(f"[!] Number plate '{plate}' is already registered. Duplicate plates are not allowed.")
        return

    owner = input("Enter Owner Name   : ").strip()
    if not owner:
        print("[!] Owner name cannot be empty.")
        return

    model = input("Enter Vehicle Model: ").strip()
    if not model:
        print("[!] Vehicle model cannot be empty.")
        return

    vehicle_registry[plate] = {"owner": owner, "model": model}
    print(f"\n[✓] Vehicle registered successfully!")
    print(f"    Plate : {plate}")
    print(f"    Owner : {owner}")
    print(f"    Model : {model}")


def retrieve_vehicle():
    print("\n── Retrieve Vehicle ──")
    plate = normalise_plate(input("Enter Number Plate to search: ").strip())
    if not plate:
        print("[!] Number plate cannot be empty.")
        return

    if plate not in vehicle_registry:
        print(f"[✗] No vehicle found with number plate '{plate}'.")
        return

    info = vehicle_registry[plate]
    print(f"\n  Number Plate : {plate}")
    print(f"  Owner Name   : {info['owner']}")
    print(f"  Model        : {info['model']}")


def list_vehicles():
    print("\n── All Registered Vehicles ──")
    if not vehicle_registry:
        print("  (no vehicles registered yet)")
        return
    print(f"  {'Plate':<15} {'Owner':<25} {'Model'}")
    print("  " + "─" * 55)
    for plate, info in vehicle_registry.items():
        print(f"  {plate:<15} {info['owner']:<25} {info['model']}")


def handle_vehicle_menu():
    print("\n── Vehicle Registration System ──")
    print("  a. Register a vehicle")
    print("  b. Retrieve vehicle by number plate")
    print("  c. List all vehicles")
    sub = input("Select option (a/b/c): ").strip().lower()
    if sub == "a":
        register_vehicle()
    elif sub == "b":
        retrieve_vehicle()
    elif sub == "c":
        list_vehicles()
    else:
        print("[!] Invalid option.")


# ─────────────────────────────────────────────
#  Main Menu Loop
# ─────────────────────────────────────────────

MENU = """
╔══════════════════════════════════════════════╗
║   Cryptography & Blockchain Fundamentals     ║
╠══════════════════════════════════════════════╣
║  1. SHA-256 Hashing                          ║
║  2. Digital Signature (Sign & Verify)        ║
║  3. Vehicle Registration System              ║
║  0. Exit                                     ║
╚══════════════════════════════════════════════╝
"""


def main():
    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            handle_hashing()
        elif choice == "2":
            handle_digital_signature()
        elif choice == "3":
            handle_vehicle_menu()
        elif choice == "0":
            print("\nGoodbye! 👋\n")
            break
        else:
            print("[!] Invalid choice. Please enter 0, 1, 2, or 3.")

        input("\nPress Enter to return to the main menu…")


if __name__ == "__main__":
    main()
