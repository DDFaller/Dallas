import spacy
from spacy.matcher import PhraseMatcher
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

wine_descriptors = {
    "aroma": {
        "fruit": {
            "red": ["cherry", "cherries", "strawberry", "cranberry", "raspberry"],
            "black": ["blackberry", "blackcurrant", "plum", "blueberry", "sloe", "damson"],
            "stone": ["peach", "yellow peach", "apricot", "nectarine"],
            "citrus": ["lemon", "lemon zest", "lime", "mandarin", "grapefruit"],
            "tropical": ["kiwi", "pineapple", "melon", "banana"],
            "other": ["greengage", "pear", "nashi pear", "tinned peach"]
        },
        "floral": ["honeysuckle", "elderflower", "apple blossom", "wild flower"],
        "herbal": ["mint", "thyme", "eucalyptus", "herbs", "leafy", "green"],
        "spice": ["pepper", "black pepper", "clove", "cinnamon", "nutmeg", "spice"],
        "savory": ["olive", "iodine", "saline", "truffle", "earthy", "mushroom", "leather", "nutty", "toasted cashew", "hazelnut"],
        "oak_sweet": ["vanilla", "chocolate", "dark chocolate", "mocha", "coffee", "toast", "smoke", "candied", "honey", "caramel"]
    },
    "palate":{
        "ripe":["ripe"],
        "balanced":["balanced"]
    }
}

# ---- build PhraseMatcher patterns ----
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

def iter_lexicon(node, path):
    """Yield (label, phrase) tuples from nested dict/lists."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from iter_lexicon(v, path + [k])
    elif isinstance(node, list):
        label = "|".join(path)  # e.g., "aroma|fruit|red"
        for phrase in node:
            yield (label, phrase)

# Group phrases by label to add in batches
label_to_docs = defaultdict(list)
for label, phrase in iter_lexicon(wine_descriptors, []):
    # Use make_doc (faster; no pipeline)
    label_to_docs[label].append(nlp.make_doc(phrase))

for label, docs in label_to_docs.items():
    matcher.add(label, docs)

# ---- test ----
text = """This has beautiful aromas of sweet, black cherries,
with raspberry notes and a hint of olive savouriness.
The palate is ripe but balanced."""
text2 = """
Flinty notes on the nose with lots of fruit - yellow peach, melon, nashi pear.
Concentrated with lovely nutty complexity and lemony acid persistence
"""

doc = nlp(text2)

matches = matcher(doc)
spans = []
for match_id, start, end in matches:
    label = nlp.vocab.strings[match_id]
    span = doc[start:end]
    spans.append((label, span.text))

print(text2)
print("Matches:")
for label, span_text in spans:
    print(f"{label:25s} -> {span_text}")
