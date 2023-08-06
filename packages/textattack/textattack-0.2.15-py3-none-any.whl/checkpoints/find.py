import sys
import pickle
import os

target_recipe = sys.argv[1]
target_model = sys.argv[2]
print(target_recipe, target_model)
files = [f for f in os.listdir(".") if f.endswith('.ta.chkpt')]
checkpoints = []
for f in files:
    with open(f, 'rb') as fh:
        fh.seek(0)
        checkpoints.append(pickle.load(fh))

matching = []
for i in range(len(checkpoints)):
    c = checkpoints[i]
    if c.args.recipe == target_recipe and c.args.model == target_model:
        matching.append(files[i])

matching = [int(m.replace(".ta.chkpt", "")) for m in matching]
latest = max(matching)
matching.sort(reverse=True)
print("Latest: ", str(latest) + ".ta.chkpt")
print("Matching: ", [str(m) + ".ta.chkpt" for m in matching])

with open(str(latest) + ".ta.chkpt", 'rb') as f:
    print(pickle.load(f))