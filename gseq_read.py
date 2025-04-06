import numpy as np


def gseq_read_res_mat(fname):
    with open(fname, "r") as f:
        header = f.readline()
        if not header.startswith("Given:"):
            raise ValueError(f"header: [{header}] not valid")
        headerwords = header.split()
        categories = headerwords[1:]
        otherLines = f.readlines()
        lineV = {}
        for line in otherLines:
            words = line.split()
            if len(words) < 1:
                continue
            if not words[0] in categories:
                raise ValueError(f"{words[0]} not seen")
            lineV[words[0]] = [float(v) for v in words[1:]]
        mat = np.zeros((len(categories), len(categories))) * np.nan
        for i, tagi in enumerate(categories):
            for j, tagj in enumerate(categories):
                mat[i, j] = lineV[tagi][j]
        return categories, mat


if __name__ == "__main__":
    print(gseq_read_res_mat("gseq_out_0.txt"))
