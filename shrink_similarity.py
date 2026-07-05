import pickle
import numpy as np

similarity = pickle.load(open('similarity.pkl', 'rb'))
print("Before:", similarity.dtype, similarity.nbytes / 1_000_000, "MB")

similarity = similarity.astype(np.float32)

with open('similarity.pkl', 'wb') as f:
    pickle.dump(similarity, f)

print("After:", similarity.dtype, similarity.nbytes / 1_000_000, "MB")