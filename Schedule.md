## Page Rank Calculations
Will happen once per day as a batch job. The Page Rank algorithm will be implemented as follows:
1. Initialize each page's rank to 1/N, where N is the total number of pages.
2. For each page, distribute its current rank equally among all pages it links to.
3. Update each page's rank based on the ranks received from other pages, using the formula:
   PR(A) = (1-d) + d * (PR(T1)/C(T1) + ... + PR(Tn)/C(Tn))
   where:
   - PR(A) is the Page Rank of page A
   - d is the damping factor (typically set to 0.85)
   - PR(Ti) is the Page Rank of page Ti that links to page A
   - C(Ti) is the number of outbound links on page Ti
4. Repeat steps 2 and 3 for a fixed number of iterations or until the ranks converge (i.e., the change in Page Rank values is below a certain threshold).
5. Store the final Page Rank values in the URL Lookup Table for use during search result ranking, enhancing the relevance of search results based on the authority of the pages.
