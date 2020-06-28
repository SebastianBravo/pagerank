from pagerank import transition_model

DAMPING = 0.85
SAMPLES = 10000

corpus = {"1.html": {}, "2.html": {"3.html"}, "3.html": {"2.html"}}
page = "1.html"

print(transition_model(corpus, page, DAMPING))
