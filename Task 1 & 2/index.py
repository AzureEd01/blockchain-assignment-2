def modinv(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

# Given values for all 4 inventories
inventories = {
    'A': {'p': 1210613765735147311106936311866593978079938707, 'q': 1247842850282035753615951347964437248190231863, 'e': 815459040813953176289801},
    'B': {'p': 787435686772982288169641922308628444877260947, 'q': 1325305233886096053310340418467385397239375379, 'e': 692450682143089563609787},
    'C': {'p': 1014247300991039444864201518275018240361205111, 'q': 904030450302158058469475048755214591704639633, 'e': 1158749422015035388438057},
    'D': {'p': 1287737200891425621338551020762858710281638317, 'q': 1330909125725073469794953234151525201084537607, 'e': 33981230465225879849295979}
}

output_lines = []

# Step 1: Generate key pairs for all inventories
for inv, keys in inventories.items():
    p = keys['p']
    q = keys['q']
    e = keys['e']
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d = modinv(e, phi_n)

    # Store computed values back
    keys['n'] = n
    keys['phi_n'] = phi_n
    keys['d'] = d

    output_lines.append(f"Inventory {inv} RSA Key Setup:")
    output_lines.append(f"  p = {p}")
    output_lines.append(f"  q = {q}")
    output_lines.append(f"  e = {e}")
    output_lines.append(f"  n = {n}")
    output_lines.append(f"  phi(n) = {phi_n}")
    output_lines.append(f"  d = {d}")
    output_lines.append(f"  Public Key = ({e}, {n})")
    output_lines.append(f"  Private Key = ({d}, {n})")
    output_lines.append("-" * 40)

# Step 2: Signing a message by Inventory A
message = 1234567890  # Sample message (as integer)
signer = 'A'
signing_keys = inventories[signer]
signature = pow(message, signing_keys['d'], signing_keys['n'])

output_lines.append(f"\nInventory {signer} signs message: {message}")
output_lines.append(f"Generated Signature: {signature}")

# Step 3: Verification by B, C, D
for verifier in inventories:
    if verifier == signer:
        continue
    verifying_keys = inventories[signer]  # Always use signer’s public key
    e = verifying_keys['e']
    n = verifying_keys['n']
    verified_message = pow(signature, e, n)

    output_lines.append(f"\nInventory {verifier} verifies signature:")
    output_lines.append(f"  Recovered Message = {verified_message}")
    output_lines.append("  ✅ Verified!" if verified_message == message else "  ❌ Verification Failed!")

# Save results to file
with open("rsa_full_verification_output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("RSA key generation and verification completed. Results saved to rsa_full_verification_output.txt.")
