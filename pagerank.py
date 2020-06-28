import os
import random
import re
import sys
import numpy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = {}
    
    N_pages = len(corpus.keys())
    pages_linked = corpus[page]


    if len(pages_linked) == 0:
        probability = 1/N_pages
        for page in corpus.keys():
            distribution[page] = probability
    else:
        for page in corpus.keys():
            distribution[page] = (1 - damping_factor) / N_pages
        for page in pages_linked:
            distribution[page] += damping_factor / len(pages_linked)

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample = random.choice(list(corpus.keys()))
    samples = [sample]

    ranks = {}

    for sample_n in range(n-1):
        distribution = transition_model(corpus, sample, damping_factor)
        pages_linked = list(distribution.keys())
        probabilities = list(distribution.values())

        sample = numpy.random.choice(pages_linked, p=probabilities)

        samples.append(sample)

    for page in corpus.keys():
        page_rank = samples.count(page) / n
        ranks[page] = page_rank

    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {}

    N_pages = len(corpus.keys())
    repeat = True

    probability1 = (1 - damping_factor) / N_pages
    probability2 = 0

    changes = []

    for page in corpus.keys():
        ranks[page] = 1 / N_pages

    while repeat:
        for page in corpus.keys():
            probability2 = 0
            pages_linked = linked(corpus, page)

            for link in pages_linked:
                num_links = len(corpus[link])
                probability2 += ranks[link] / num_links

            probability2 = damping_factor * probability2 

            new_rank = probability1 + probability2
            changes.append(abs(new_rank - ranks[page]))
            ranks[page] = new_rank

        if all(change <= 0.001 for change in changes):
            repeat = False
        else:
            changes = []

    return ranks


def linked(corpus, page):

    if len(corpus[page]) == 0:
        return list(corpus.keys())
    else:
        return [x for x in corpus.keys() if page in corpus[x]]


if __name__ == "__main__":
    main()
