import itertools
import random
from .prime_field import PrimeFieldElement

def generate_all_sets(num_parties, num_reconstruct):
    return list(itertools.combinations(range(1, num_parties + 1), num_reconstruct))

def get_n_of_n_additive_shares(secret, n):
    shares = []
    running_sum = secret
    for _ in range(n-1):
        rand_val = PrimeFieldElement(random.randint(1, 66))
        shares.append(rand_val)
        running_sum -= rand_val
    shares.append(running_sum)
    return shares

def distribute_shares(secret, all_share_sets):
    replicated_shares_map = dict()
    num_shares = len(all_share_sets)
    shares = get_n_of_n_additive_shares(secret, num_shares)

    for (i, share_set) in enumerate(all_share_sets):
        for share_index in share_set:
            share_to_distribute = shares[i]
            replicated_shares_map.setdefault(share_index, {})[share_set] = share_to_distribute
    return replicated_shares_map

def generate_own_mapping(all_share_sets):
    mapping = {}
    for (share_set_1, share_set_2) in itertools.combinations_with_replacement(all_share_sets, 2):
        intersection = list(set(share_set_1).intersection(set(share_set_2)))
        rand_party_assign = random.randint(0, len(intersection) - 1)
        mapping.setdefault(intersection[rand_party_assign], []).append((share_set_1, share_set_2))
    return mapping

def generate_correction_share_mapping(num_parties, all_share_sets):
    mapping = {}
    for i in range(num_parties):
        while True:
            random_share_set = all_share_sets[random.randint(0, len(all_share_sets) - 1)]
            if (i + 1) in random_share_set:
                mapping[i + 1] = random_share_set
                break
    return mapping