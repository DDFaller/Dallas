import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

wine_lexicon = {
    "appearance": {
        "clarity": ["clear", "hazy", "faulty"],
        "intensity": ["pale", "medium", "deep"],
        "colour": {
            "white": ["lemon-green", "lemon", "gold", "amber", "brown"],
            "rosé": ["pink", "salmon", "orange", "onion skin"],
            "red": ["purple", "ruby", "garnet", "tawny", "brown"]
        },
        "other_observations": ["legs", "tears", "deposit", "pétillance", "bubbles"]
    },
    
    "nose": {
        "condition": ["clean", "unclean", "faulty"],
        "intensity": ["light", "medium(-)", "medium", "medium(+)", "pronounced"],
        "aroma_characteristics": ["primary", "secondary", "tertiary"]
    },
    
    "palate": {
        "sweetness": ["dry", "off-dry", "medium-dry", "medium-sweet", "sweet", "luscious"],
        "acidity": ["low", "medium(-)", "medium", "medium(+)", "high"],
        "tannin_level": ["low", "medium(-)", "medium", "medium(+)", "high"],
        "tannin_nature": [
            "ripe", "soft", "unripe", "green", "stalky", "coarse", "fine-grained"
        ],
        "alcohol": ["low", "medium(-)", "medium", "medium(+)", "high"],
        "fortified_wines_alcohol": ["low", "medium", "high"],
        "body": ["light", "medium(-)", "medium", "medium(+)", "full"],
        "flavour_intensity": ["light", "medium(-)", "medium", "medium(+)", "pronounced"],
        "flavour_characteristics": ["primary", "secondary", "tertiary"],
        "other_observations": [
            "steely", "oily", "creamy", "mouthcoating", "pétillance"
        ],
        "finish": ["short", "medium(-)", "medium", "medium(+)", "long"]
    },
    
    "conclusions": {
        "quality": ["faulty", "poor", "acceptable", "good", "very good", "outstanding"],
        "assessment_of_quality": [
            "balance", "integration", "intensity", "finish", "complexity",
            "mousse", "varietal definition", "potential for ageing"
        ]
    },
    
    "readiness_and_ageing": {
        "assessment": [
            "too young", "can drink now", "potential for ageing", 
            "suitable for ageing", "too old"
        ],
        "factors": [
            "concentration", "acidity", "tannin", "development of aroma", 
            "development of flavour characteristics"
        ]
    }
}


matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
for label, words in wine_lexicon.items():
    patterns = [nlp.make_doc(word) for word in words]
    matcher.add(label, patterns)

text = """
This has beautiful aromas of sweet, black cherries,
with raspberry notes and a hint of olive savouriness. 
The palate is ripe but balanced."
"""
doc = nlp(text)

matches = matcher(doc)
extracted = set()
for match_id, start, end in matches:
    label = nlp.vocab.strings[match_id]
    extracted.add(label)

print(extracted)
