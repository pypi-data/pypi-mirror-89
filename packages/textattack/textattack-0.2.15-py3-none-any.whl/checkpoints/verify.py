import sys
import pickle
import os

recipes = ['greedy-wed-med', 'greedyWIR-wed-med', 'mha-wed-med', 'beam4-wed-med', 'beam8-wed-med', 'genetic-wed-med',
            'greedy-wed-strict', 'greedyWIR-wed-strict', 'mha-wed-strict', 'beam4-wed-strict', 'beam8-wed-strict', 'genetic-wed-strict']
models = ['bert-yelp-sentiment', 'lstm-imdb', 'bert-mr', 'bert-snli']

def verify(checkpoint):
    results_set = set()
    for result in checkpoint.log_manager.results:
        results_set.add(result.original_result.tokenized_text)
    if len(results_set) == 1000:
        return (True, None)
    else:
        return (False, len(results_set))

if len(sys.argv) == 2:
    checkpt_file = sys.argv[1]
    with open(checkpt_file, 'rb') as f:
        c = pickle.load(f)
    recipe = c.args.recipe
    model = c.args.model
    print(f'{model} and {recipe}: {verify(c)}')

elif len(sys.argv) == 3:
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
    index = matching.index(latest)

    checkpoint = checkpoints[index]
    print(verify(checkpoint))

else:
    files = [f for f in os.listdir(".") if f.endswith('.ta.chkpt')]
    checkpoints = []
    for f in files:
        with open(f, 'rb') as fh:
            fh.seek(0)
            checkpoints.append(pickle.load(fh))
    for model in models:
        for recipe in recipes:
            matching_names = []
            matching_checkpoints = []
            for i in range(len(checkpoints)):
                c = checkpoints[i]
                if c.args.recipe == recipe and c.args.model == model:
                    matching_names.append(files[i])
                    matching_checkpoints.append(c)

            if not matching_names:
                print(f"No checkpoints for {recipe} and {model}")
                continue
            matching_time = [int(m.replace(".ta.chkpt", "")) for m in matching_names]
            latest = str(max(matching_time)) + ".ta.chkpt"
            index = matching_names.index(latest)
            checkpoint = matching_checkpoints[index]

            result = verify(checkpoint)
            if not result[0]:
                print(f'{recipe} and {model}: {result[1]} ({latest})')
