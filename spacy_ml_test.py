import spacy
from spacy.util import minibatch, compounding
from wasabi import Printer
msg = Printer()

nlp = spacy.blank("en")
textcat = nlp.add_pipe("textcat_multilabel", config={"exclusive_classes": False})

labels = ["aroma_red_fruit","aroma_black_fruit","floral","herbal","spice",
          "savory","oak_sweet","acidity","shape_linear","texture_body",
          "tannin","juicy","finish","complexity"]
for lab in labels:
    textcat.add_label(lab)

optimizer = nlp.initialize()
for epoch in range(6):
    losses = {}
    for batch in minibatch(TRAIN_DATA, size=8):
        nlp.update(batch, sgd=optimizer, losses=losses)
    msg.info(f"Epoch {epoch} losses: {losses}")
