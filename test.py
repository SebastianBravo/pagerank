from pagerank import transition_model, sample_pagerank
import random

DAMPING = 0.85
SAMPLES = 100

corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
ranks = sample_pagerank(corpus, DAMPING, SAMPLES)

print(f"PageRank Results from Sampling (n = {SAMPLES})")
for page in sorted(ranks):
	print(f"  {page}: {ranks[page]:.4f}")

print(list(range(9)))