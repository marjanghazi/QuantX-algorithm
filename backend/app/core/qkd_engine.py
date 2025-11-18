import numpy as np

def run_bb84(n=50, include_eve=False):
    """
    Fully functional BB84 simulation with optional Eve eavesdropping.
    Returns all necessary info for visualization.
    """
    # 1. Alice generates random bits & bases
    alice_bits = np.random.randint(2, size=n).tolist()
    alice_bases = np.random.randint(2, size=n).tolist()  # 0=+, 1=x

    # 2. Bob chooses random bases
    bob_bases = np.random.randint(2, size=n).tolist()
    bob_results = []

    # Optional Eve (can be expanded later)
    eve_bits = None
    if include_eve:
        eve_bits = np.random.randint(2, size=n).tolist()

    # 3. Bob measures
    for i in range(n):
        if alice_bases[i] == bob_bases[i]:
            bob_results.append(alice_bits[i])  # correct
        else:
            bob_results.append(np.random.randint(2))  # random

    # 4. Sifting – indices where bases match
    sifted_key_indices = [i for i in range(n) if alice_bases[i] == bob_bases[i]]
    sifted_key = [alice_bits[i] for i in sifted_key_indices]  # always Alice's bit
    bob_sifted = [bob_results[i] for i in sifted_key_indices]

    # 5. QBER
    if len(sifted_key) > 0:
        mismatches = sum(1 for a,b in zip(sifted_key, bob_sifted) if a!=b)
        qber = mismatches/len(sifted_key)
    else:
        qber = 0

    eavesdropping_detected = qber > 0.11

    # Return everything for frontend
    return {
        "total_bits": n,
        "alice_bits": alice_bits,
        "alice_bases": alice_bases,
        "bob_bases": bob_bases,
        "bob_results": bob_results,
        "sifted_key_indices": sifted_key_indices,  # indices for frontend
        "sifted_key": sifted_key,
        "bob_sifted": bob_sifted,
        "sifted_key_length": len(sifted_key),
        "qber": round(qber, 4),
        "eavesdropping_detected": eavesdropping_detected,
        "eve_bits": eve_bits
    }
