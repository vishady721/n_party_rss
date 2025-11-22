import random
import copy
from .utils import generate_all_sets, distribute_shares, generate_correction_share_mapping, generate_own_mapping, PRF
from .prime_field import PrimeFieldElement

class ReplicatedShareMap:
    def __init__(self, share_map, num_parties, num_reconstruct, all_share_sets):
        self.num_parties = num_parties
        self.num_reconstruct = num_reconstruct
        self.all_share_sets = all_share_sets
        self.share_map = share_map        
    
    @classmethod
    def from_secret(cls, secret, num_parties, num_reconstruct):
        all_share_sets = generate_all_sets(num_parties, num_reconstruct)
        share_map = distribute_shares(secret, all_share_sets)
        return cls(share_map, num_parties, num_reconstruct, all_share_sets)
    
    def get(self, party, share_set):
        return self.share_map[party][share_set]
    
    def __add__(self, other):
        share_map = copy.deepcopy(self.share_map)
        if type(other) == ReplicatedShareMap:
            assert((self.num_parties, self.num_reconstruct) == (other.num_parties, other.num_reconstruct))
            for (party_idx_1, party_shares_1) in other.share_map.items():
                for (share_1_set, share_1) in party_shares_1.items():
                    share_map[party_idx_1][share_1_set] += share_1
        elif type(other) == PrimeFieldElement:
            set_to_add_constant = self.all_share_sets[random.randint(1, len(self.all_share_sets)) - 1]
            for party in set_to_add_constant:
                share_map[party][set_to_add_constant] += other
        return ReplicatedShareMap(share_map, self.num_parties, self.num_reconstruct, self.all_share_sets)

    def __mul__(self, other):
        share_map = copy.deepcopy(self.share_map)

        if type(other) == ReplicatedShareMap:
            own_mapping = generate_own_mapping(self.all_share_sets)
            correction_mapping = generate_correction_share_mapping(self.num_parties, self.all_share_sets)
            correction_variables = {}
            for shares_owned in share_map.values():
                for share_set in shares_owned:
                    shares_owned[share_set] = PrimeFieldElement(0)
            for (party, owns) in own_mapping.items():
                party_share = PrimeFieldElement(0)
                for (share_set_1, share_set_2) in owns:
                    if share_set_1 != share_set_2:
                        party_share += (self.get(party, share_set_1) * other.get(party, share_set_2))
                        party_share += (self.get(party, share_set_2) * other.get(party, share_set_1))
                    else:
                        share_1 = self.get(party, share_set_1)
                        share_2 = other.get(party, share_set_2)
                        party_share += (share_1 * share_2)
                correction_variables[party] = party_share
            for party_a in share_map:
                party_a_shares = { share_set : PrimeFieldElement(0) for share_set in share_map[party_a] }
                party_a_prfs = { share_set : PRF(share_set) for share_set in share_map[party_a] }
                for party_b in share_map:
                    for party_set_a in share_map[party_a]:
                        if (party_a != party_b) and (party_set_a != correction_mapping[party_b]) and (party_set_a in share_map[party_b]):
                            party_a_shares[party_set_a] += party_a_prfs[party_set_a].next()
                        elif (party_a == party_b) and (party_set_a != correction_mapping[party_a]):
                            val_to_add = party_a_prfs[party_set_a].next()
                            party_a_shares[party_set_a] += val_to_add
                            correction_variables[party_a] -= val_to_add
                share_map[party_a] = party_a_shares
            for party in share_map:
                for party_in_correction_set in correction_mapping[party]:
                    share_map[party_in_correction_set][correction_mapping[party]] += correction_variables[party]

        elif type(other) == PrimeFieldElement:
            for (party_idx, party_shares) in self.share_map.items():
                for share_set in party_shares:
                    share_map[party_idx][share_set] *= other
        return ReplicatedShareMap(share_map, self.num_parties, self.num_reconstruct, self.all_share_sets)
    
    def reconstruct_secret(self, parties):
        secret = PrimeFieldElement(0)
        share_sets_to_add = [elem for elem in self.all_share_sets]
        for party in parties:
            shares_owned_by_party = self.share_map[party]
            for share_set in shares_owned_by_party:
                if share_set in share_sets_to_add:
                    secret += (shares_owned_by_party[share_set]) 
                    share_sets_to_add.remove(share_set)
        if len(share_sets_to_add) != 0:
            return None
        return secret