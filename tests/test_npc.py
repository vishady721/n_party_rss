from npc_computation.npc import ReplicatedShareMap
from npc_computation.prime_field import PrimeFieldElement
import unittest
import itertools
import random

class FivePCTesting(unittest.TestCase):
    num_parties = 5
    num_reconstruct = 3

    def test_distributing_shares(self):
        secret = PrimeFieldElement(random.randint(0, 84294719))
        shares = ReplicatedShareMap.from_secret(secret, self.num_parties, self.num_reconstruct)
        shares_to_reconstruct = random.choice(list(itertools.combinations(range(1, self.num_parties + 1), self.num_reconstruct)))
        reconstructed_secret = shares.reconstruct_secret(shares_to_reconstruct)
        assert(reconstructed_secret == secret)
    
    def test_reconstruction_for_any_geq_k(self):
        secret = PrimeFieldElement(random.randint(0, 84294719))
        shares = ReplicatedShareMap.from_secret(secret, self.num_parties, self.num_reconstruct)
        for k in range(self.num_reconstruct, self.num_parties + 1):
            all_combinations = list(itertools.combinations(range(1, self.num_parties + 1), k))
            for comb in all_combinations:
                reconstructed_secret = shares.reconstruct_secret(comb)
                assert(reconstructed_secret == secret)
    
    def test_add(self):
        secret_1 = PrimeFieldElement(random.randint(0, 84294719))
        secret_2 = PrimeFieldElement(random.randint(0, 84294719))
        shares_1 = ReplicatedShareMap.from_secret(secret_1, self.num_parties, self.num_reconstruct)
        shares_2 = ReplicatedShareMap.from_secret(secret_2, self.num_parties, self.num_reconstruct)
        added_shares = shares_1 + shares_2
        shares_to_reconstruct = random.choice(list(itertools.combinations(range(1, self.num_parties + 1), self.num_reconstruct)))
        assert(added_shares.reconstruct_secret(shares_to_reconstruct) == secret_1 + secret_2)
    
    def test_scalar_mul(self):
        secret = PrimeFieldElement(random.randint(0, 84294719))
        constant = PrimeFieldElement(random.randint(0, 84294719))
        shares = ReplicatedShareMap.from_secret(secret, self.num_parties, self.num_reconstruct)
        scaled_shares = shares * constant
        shares_to_reconstruct = random.choice(list(itertools.combinations(range(1, self.num_parties + 1), self.num_reconstruct)))
        assert(scaled_shares.reconstruct_secret(shares_to_reconstruct) == secret * constant)
    
    def test_add_constant(self):
        secret = PrimeFieldElement(random.randint(0, 84294719))
        constant = PrimeFieldElement(random.randint(0, 84294719))
        shares = ReplicatedShareMap.from_secret(secret, self.num_parties, self.num_reconstruct)
        scaled_shares = shares + constant
        shares_to_reconstruct = random.choice(list(itertools.combinations(range(1, self.num_parties + 1), self.num_reconstruct)))
        assert(scaled_shares.reconstruct_secret(shares_to_reconstruct) == secret + constant)
    
    def test_mul_shares(self):
        secret_1 = PrimeFieldElement(random.randint(0, 84294719))
        secret_2 = PrimeFieldElement(random.randint(0, 84294719))
        shares_1 = ReplicatedShareMap.from_secret(secret_1, self.num_parties, self.num_reconstruct)
        shares_2 = ReplicatedShareMap.from_secret(secret_2, self.num_parties, self.num_reconstruct)
        added_shares = shares_1 * shares_2
        shares_to_reconstruct = random.choice(list(itertools.combinations(range(1, self.num_parties + 1), self.num_reconstruct)))
        assert(added_shares.reconstruct_secret(shares_to_reconstruct) == secret_1 * secret_2)

if __name__ == "__main__":
    unittest.main()