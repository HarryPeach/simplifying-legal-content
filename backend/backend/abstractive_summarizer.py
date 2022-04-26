
import lorem


class AbstractiveSummariser():
    def __init__(self):
        ...

    def summarise(self, doc: list[str]) -> str:
        """Takes a list of sentences and creates an abstractive simplification

        Args:
            doc (list[str]): The list of sentences

        Returns:
            str: The simplification as a string
        """
        # TODO: Implement
        return lorem.paragraph()
