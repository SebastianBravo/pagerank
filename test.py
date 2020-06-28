from pagerank import *
import random

DAMPING = 0.85
SAMPLES = 10000

corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}

ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
print(f"PageRank Results from Sampling (n = {SAMPLES})")
for page in sorted(ranks):
	print(f"  {page}: {ranks[page]:.4f}")
ranks = iterate_pagerank(corpus, DAMPING)
print(f"PageRank Results from Iteration")
for page in sorted(ranks):
	print(f"  {page}: {ranks[page]:.4f}")