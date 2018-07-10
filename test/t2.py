import pandas as pd

letter = ['B', 'A', 'C', 'D', 'A', 'C', 'D', 'A']

df = pd.Series(letter)
ct = df.value_counts()
print(ct.index)
for k, v in ct.items():
    # print(k, v)
    pass
print("B", ct["B"])

print("B" in ct.index)
