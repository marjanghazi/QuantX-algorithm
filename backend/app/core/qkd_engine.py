import numpy as np


def run_bb84(n=50):
    """
    Fully functional BB84 simulation for MVP.
    Generates bits, bases, simulates quantum transmission,
    performs measurement, calculates sifted key and QBER.
    """

    # ------------------------
    # 1. Alice generates random bits & bases
    # ------------------------
    alice_bits = np.random.randint(2, size=n).tolist()
    alice_bases = np.random.randint(2, size=n).tolist()  # 0 = + basis, 1 = x basis

    # ------------------------
    # 2. Bob chooses random bases
    # ------------------------
    bob_bases = np.random.randint(2, size=n).tolist()

    # ------------------------
    # 3. Bob measures photons
    # If bases match → bit received correctly
    # If bases mismatch → random bit
    # ------------------------
    bob_results = []
    for i in range(n):
        if alice_bases[i] == bob_bases[i]:
            bob_results.append(alice_bits[i])   # correct measurement
        else:
            bob_results.append(np.random.randint(2))  # random due to mismatched basis

    # ------------------------
    # 4. Sifting – keep only matching bases
    # ------------------------
    sifted_key_indices = [
        i for i in range(n) if alice_bases[i] == bob_bases[i]
    ]

    sifted_key = [alice_bits[i] for i in sifted_key_indices]
    bob_sifted = [bob_results[i] for i in sifted_key_indices]

    # ------------------------
    # 5. QBER Calculation
    # ------------------------
    if len(sifted_key) > 0:
        mismatches = sum(1 for a, b in zip(sifted_key, bob_sifted) if a != b)
        qber = mismatches / len(sifted_key)
    else:
        qber = 0

    # ------------------------
    # 6. Eavesdropping detection
    # Typical threshold: > 11% QBER = attack detected
    # ------------------------
    eavesdropping_detected = qber > 0.11

    return {
        "total_bits": n,
        "alice_bits": alice_bits,
        "alice_bases": alice_bases,
        "bob_bases": bob_bases,
        "bob_results": bob_results,
        "sifted_key": sifted_key,
        "bob_sifted": bob_sifted,
        "sifted_key_length": len(sifted_key),
        "qber": round(qber, 4),
        "eavesdropping_detected": eavesdropping_detected
    }
