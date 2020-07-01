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
    # Initialize an empty dictionary to keep the probability distribution.
    distribution = dict()
    
    # Variables to keep track of number of pages and pages linked.
    N_pages = len(corpus.keys())
    pages_linked = corpus[page]

    # If there isn't page linked, the probability is the same for each
    # page. In other case, it depends on the damping factor and the 
    # number of pages linked.
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
    # Variable to keep track of the current sample, it starts being
    # completely random.
    sample = random.choice(list(corpus.keys()))

    # Initialize a list of samples with the first sample. 
    samples = [sample]

    # Initialize an empty dictionary to keep the rank of each page.
    ranks = dict()

    # Add n-1 samples to the list, each sample is based on a 
    # transition model.
    for sample_n in range(n-1):
        distribution = transition_model(corpus, sample, damping_factor)
        pages_linked = list(distribution.keys())
        probabilities = list(distribution.values())
        sample = numpy.random.choice(pages_linked, p=probabilities)
        samples.append(sample)

    # Calculete the page rank for each page based on the frequency  
    # of each page in the samples list.
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
    # Initialize an empty dictionary to keep the rank of each page.
    ranks = dict()

    # Variable to keep track of the number of pages.
    N_pages = len(corpus.keys())

    # Variable to keep track of whether iterating or not.
    iterate = True

    # Variables to kepp track of the probabilities. 
    probability1 = (1 - damping_factor) / N_pages
    probability2 = 0

    # Initialize an empty list to keep track of the changes of the
    # page rank for each page.
    changes = []

    # ALl the pages starts whith the same page rank 
    for page in corpus.keys():
        ranks[page] = 1 / N_pages

    # Itereate until no PageRank value changes by more than 0.001
    while iterate:
        # Initialize a list to keep new ranks
        new_ranks = []

        # Loop throug all the pages and initialize a list with the 
        # pages that link to each page
        for page in corpus.keys():
            probability2 = 0
            links_in = links_to_page(corpus, page)

            # Calculate the probabilitie of going to the page in
            # each link
            for link in links_in:
                if len(corpus[link]) != 0:
                    num_links = len(corpus[link])
                else:
                    num_links = len(corpus.keys())
                probability2 += ranks[link] / num_links

            probability2 = damping_factor * probability2 

            # Calculate the new page rank
            new_rank = probability1 + probability2

            # Calculate how much the rank changed from the previous rank
            changes.append(abs(new_rank - ranks[page]))

            # Update new ranks list
            new_ranks.append(new_rank)

        # Decides whether to continue iterating or not and update page ranks
        if any(change >= 0.001 for change in changes):
            changes = []
            i = 0
            for page in corpus.keys():
                ranks[page] = new_ranks[i]
                i += 1 
        else:
            iterate = False

    return ranks


def links_to_page(corpus, page):
    """
    Returns a list of pages that link to a certain page.
    If a page has no links it is interpreted as having 
    one link for every page in the corpus (including itself).
    """
    links_to_page = []

    for p in corpus.keys():
        if page in corpus[p] or len(corpus[p]) == 0:
            links_to_page.append(p)

    return links_to_page


if __name__ == "__main__":
    main()
