import os
import random
import re
import sys

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
    probability_dist = {}
    num_pages = len(corpus)
    
    # If page has no outgoing links, treat as linking to all pages
    if not corpus[page]:
        for p in corpus:
            probability_dist[p] = 1.0 / num_pages
    else:
        # Probability from random jump
        random_jump = (1 - damping_factor) / num_pages
        # Probability from following links
        link_follow = damping_factor / len(corpus[page])
        
        for p in corpus:
            probability_dist[p] = random_jump
            if p in corpus[page]:
                probability_dist[p] += link_follow
                
    return probability_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))
    
    for _ in range(n):
        page_ranks[current_page] += 1
        model = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            list(model.keys()),
            weights=list(model.values())
        )[0]
    
    # Normalize the results
    total = sum(page_ranks.values())
    for page in page_ranks:
        page_ranks[page] /= total
        
    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    ranks = {page: 1.0 / num_pages for page in corpus}
    threshold = 0.001
    converged = False
    
    while not converged:
        converged = True
        new_ranks = {}
        
        for page in corpus:
            new_rank = (1 - damping_factor) / num_pages
            
            # Sum the rank contributions from pages linking to this page
            for linking_page in corpus:
                # If linking_page has no links, treat as linking to all pages
                if not corpus[linking_page]:
                    new_rank += damping_factor * ranks[linking_page] / num_pages
                elif page in corpus[linking_page]:
                    new_rank += damping_factor * ranks[linking_page] / len(corpus[linking_page])
            
            new_ranks[page] = new_rank
            
            # Check for convergence
            if abs(new_ranks[page] - ranks[page]) > threshold:
                converged = False
                
        # Normalize the ranks (should sum to 1)
        total = sum(new_ranks.values())
        for page in new_ranks:
            new_ranks[page] /= total
            
        ranks = new_ranks
        
    return ranks


if __name__ == "__main__":
    main()