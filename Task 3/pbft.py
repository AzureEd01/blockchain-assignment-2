from collections import Counter
import hashlib

def hash_result(result):
    return hashlib.sha256(str(result).encode()).hexdigest()

def pbft_consensus(results):
    """
    `results` is a list of values returned from nodes.
    This returns the agreed result if consensus reached, otherwise None.
    """
    hashes = [hash_result(r) for r in results]
    counts = Counter(hashes)
    most_common_hash, count = counts.most_common(1)[0]

    if count >= 3:  # 2f + 1, assuming f = 1 for 4 nodes
        agreed_index = hashes.index(most_common_hash)
        return results[agreed_index]
    else:
        return None  # Consensus failed
