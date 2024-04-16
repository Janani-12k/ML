import numpy as np

class CandidateElimination:
    def __init__(self, num_attributes):
        self.num_attributes = num_attributes
        self.G = self.initialize_G(num_attributes)
        self.S = self.initialize_S(num_attributes)

    def initialize_G(self, num_attributes):
        G = [(['?'] * num_attributes, ['?'] * num_attributes)]
        return G

    def initialize_S(self, num_attributes):
        S = [(['0'] * num_attributes, ['0'] * num_attributes)]
        return S

    def fit(self, X):
        for x, y in X:
            if y == 'Y':
                self.remove_inconsistent_G(x)
                self.generalize_S(x)
            else:
                self.remove_inconsistent_S(x)
                self.specialize_G(x)

    def remove_inconsistent_G(self, x):
        self.G = [g for g in self.G if not self.is_more_general(x, g[0])]

    def is_more_general(self, x, h):
        for i in range(len(x)):
            if h[i] != '?' and x[i] != h[i]:
                return False
        return True

    def generalize_S(self, x):
        S_new = []
        for s in self.S:
            for i in range(len(s[0])):
                if s[0][i] == '0' and x[i] != '0':
                    s_new = (s[0][:], s[1][:])
                    s_new[0][i] = x[i]
                    S_new.append(s_new)
        self.S = S_new

    def remove_inconsistent_S(self, x):
        self.S = [s for s in self.S if not self.is_more_specific(x, s[0])]

    def is_more_specific(self, x, h):
        for i in range(len(x)):
            if h[i] != '?' and x[i] != h[i]:
                return False
            if h[i] == '0' and x[i] != '0':
                return False
        return True

    def specialize_G(self, x):
        G_new = []
        for g in self.G:
            for i in range(len(g[0])):
                if g[0][i] == '?' and x[i] != '0':
                    g_new = (g[0][:], g[1][:])
                    g_new[0][i] = x[i]
                    g_new[1][i] = '0'
                    G_new.append(g_new)
        self.G += G_new

    def get_hypotheses(self):
        return self.S, self.G

# Example usage
X = [
    (['Sunny', 'Warm', 'Normal', 'Strong', 'Warm', 'Same'], 'Y'),
    (['Sunny', 'Warm', 'High', 'Strong', 'Warm', 'Same'], 'Y'),
    (['Rainy', 'Cold', 'High', 'Strong', 'Warm', 'Change'], 'N'),
    (['Sunny', 'Warm', 'High', 'Strong', 'Cool', 'Change'], 'Y'),
]

ce = CandidateElimination(num_attributes=6)
ce.fit(X)
S_hypotheses, G_hypotheses = ce.get_hypotheses()

print("Final S Hypotheses:")
for s in S_hypotheses:
    print(s)

print("\nFinal G Hypotheses:")
for g in G_hypotheses:
    print(g)
