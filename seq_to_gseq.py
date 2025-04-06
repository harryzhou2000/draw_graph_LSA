import pandas as pd

behavior_set = ["CE", "AA", "AQ", "RR", "CG", "PT", "CN", "QM", "OE", "PR", "TL", "OC"]
behavior_set = set(behavior_set)
print(behavior_set)

# Read an Excel file
df = pd.read_excel("data0.xlsx", header=None)


def number_to_column_letter(n):
    result = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result


# Print the first few rows
for i, row in df.iterrows():
    seq = []
    for j, v in enumerate(row):
        if isinstance(v, str) and len(v) == 2:
            if not v in behavior_set:
                raise ValueError(
                    f"{v} of row [{i}] index [{number_to_column_letter(j + 1)}] invalid"
                )
            seq.append(v)
    print(f"%Group#{i+1}")
    print((" ".join(seq) + " ")  * 3)
