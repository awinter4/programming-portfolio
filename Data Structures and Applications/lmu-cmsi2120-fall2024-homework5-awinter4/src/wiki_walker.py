'''
CMSI 2120 - Homework 5
Author: Andrew Winter

Original Java assignment written by Andrew Forney @forns,
converted to Python by Natalie Lau @nklau.
'''


class WikiWalker:
    """
    Simplified web crawler that tracks links between articles.

    Attributes:
    - site_map: Dictionary representing the site map, where:
        - Keys = article names (str).
        - Values = dictionaries mapping linked article names (str) to clickthrough counts (int).
    """

    def __init__(self) -> None:
        self.site_map: dict[str, dict[str, int]] = {}

    def add_article(self, article_name: str, article_links: list[str]) -> None:
        '''
        Adds an article with the given name to the site map and associates the
        given linked articles found on the page. Duplicate links in that list are
        ignored, as should an article's links to itself.

        :param article_name: The name of the page's article
        :param article_links: List of names for those articles linked on the page
        '''
        self.site_map.setdefault(article_name, {})
        for link in set(article_links):
            if link != article_name: 
                self.site_map.setdefault(link, {})
                self.site_map[article_name].setdefault(link, 0)

    def has_path(self, start: str, target: str) -> bool:
        '''
        Determines whether or not, based on the added articles with their links,
        there is *some* sequence of links that could be followed to take
        the user from the source article to the target article.

        :param src: The beginning article of the possible path
        :param target: The end article along a possible path
        :returns: Boolean representing whether or not that path exists
        '''
        if start not in self.site_map or target not in self.site_map:
            return False
        return self._path_exists(start, target, set())

    def log_trajectory(self, path: list[str]) -> None:
        '''
        Increments the click counts of each link along some trajectory. For
        instance, a trajectory of ["A", "B", "C"] will increment the click
        count of the "B" link on the "A" page, and the count of the "C" link
        on the "B" page. Assume that all given trajectories are valid,
        meaning that a link exists from page i to i+1 for each index i

        :param path: A sequence of a user's page clicks; must be at least
        2 article names in length
        '''
        if len(path) < 2:
            raise ValueError("Length of path must be at least 2 articles long.")

        self._validate_articles(path)
        for i in range(len(path) - 1):
            src, target = path[i], path[i + 1]
            if target not in self.site_map[src]:
                self.site_map[src][target] = 0
            self.site_map[src][target] += 1

    def clickthroughs(self, src: str, target: str) -> int:
        '''
        Returns the number of clickthroughs recorded from the src article
        to the target article. If the target article is not
        a link directly reachable from the src, returns -1.

        :param src: The article on which the clickthrough occurs.
        :param target: The article requested by the clickthrough.
        :returns: The number of times the target has been requested
        :raises ValueError: If src isn't in site map
        from the source.
        '''
        self._validate_articles([src])
        return self.site_map[src].get(target, -1)

    def most_likely_trajectory(self, src: str, max_length: int) -> list[str]:
        '''
        Based on the pattern of clickthrough trajectories recorded by this
        WikiWalker, returns the most likely trajectory of max_length clickthroughs
        starting at (but not including in the output) the given src article.

        Duplicates and cycles are valid output along a most likely trajectory.
        In the event of a tie in max clickthrough "weight," this method will choose
        the link earliest in the ascending alphabetic order of those tied.

        :param src: The starting article of the trajectory (which will not be
        included in the output)
        :param max_length: The maximum length of the desired trajectory (though may be
        shorter in the case that the trajectory ends with a terminal article).
        :returns: A list containing the ordered article names of the most likely
        trajectory starting at src.
        :raises ValueError: If src isn't in site map
        '''
        if src not in self.site_map:
            raise ValueError(f"Source article '{src}' does not exist.")

        trajectory = []
        current = src
        for _ in range(max_length):
            next_article = self._most_likely_neighbor(current)
            if next_article is None:
                break
            trajectory.append(next_article)
            current = next_article

        return trajectory

    # Helper Methods
    # -----------------------------------------------------------
    def _validate_articles(self, articles: list[str]) -> None:
        """
        Checks if all articles in the given list exist in the site map.
        Raises ValueError if any article in the list does not exist in the site map.

        param: 
        - articles: A list of article names to validate.
        """
        for article in articles:
            if article not in self.site_map:
                raise ValueError(f"Article '{article}' does not exist.")

    def _path_exists(self, start: str, target: str, visited: set[str]) -> bool:
        """
        Recursively checks if a path exists from start article to target article.
        Returns True if a path exists from start to target, False otherwise.

        param:
        - start: The starting article for the path search.
        - target: The target article to find a path to.
        - visited: Intermediary articles already visited during the search.
        """
        if start == target:
            return True
        visited.add(start)
        for neighbor in self.site_map.get(start, {}):
            if neighbor not in visited and self._path_exists(neighbor, target, visited):
                return True
        return False

    def _most_likely_neighbor(self, article: str) -> str | None:
        """
        Finds the most likely next article based on clickthrough counts.
        Resolves ties alphabetically. Returns the name of the most likely 
        next article, or None if no neighbors exist.

        param:
        - article: Current article for which to determine the most likely next neighbor.
        """
        neighbors = self.site_map.get(article, {})
        if not neighbors:
            return None

        max_clicks = -1
        most_likely = None

        for neighbor, clicks in neighbors.items():
            if (clicks > max_clicks) or (clicks == max_clicks and (most_likely is None or neighbor < most_likely)):
                max_clicks = clicks
                most_likely = neighbor

        return most_likely
