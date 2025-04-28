import re
import random
from typing import Callable, Dict


class SyntheticDataFactory:
    """
    Base factory class to generate synthetic text data for document classification task
    """

    INDUSTRY_GENERATORS: Dict[str, Dict[str, Callable]] = {}

    def __init__(
        self, num_samples: int = 1000, add_noise: bool = True, industry: str = None
    ):
        """
        Args:
            num_samples (int): Number of samples to generate.
            add_noise (bool): Whether to apply random text formatting.
            industry (str): The type of industry the documents (synthetic data) is related to.
        """
        self.num_samples = num_samples
        self.add_noise = add_noise
        self.industry = industry
        self.generators = {}

        if self.industry:
            if self.industry not in self.INDUSTRY_GENERATORS:
                raise ValueError(f"Industry '{self.industry}' not supported.")
            self.generators = self.INDUSTRY_GENERATORS[self.industry]

    def add_random_formatting(self, text: str) -> str:
        """
        Applies random formatting to simulate inconsistencies in real-world documents.
        Args:
            text (str): Input document text

        Returns:
            str: Randomly formatted version of the input text
        """
        if random.random() < 0.3:
            text = text.upper()
        elif random.random() < 0.3:
            text = text.lower()

        text = re.sub(
            r"([:,-])", lambda m: m.group(1) + (" " * random.randint(1, 3)), text
        )
        text = re.sub(r"\n", lambda _: "\n" * random.randint(1, 2), text)

        if random.random() < 0.2:
            text = (
                text.replace("o", "0")
                .replace("O", "0")
                .replace("l", "1")
                .replace("I", "1")
            )

        if random.random() < 0.2:
            insert_index = random.randint(0, len(text))
            noise = random.choice(["*", "#", "!", "~", "^", "~~"])
            text = text[:insert_index] + noise + text[insert_index:]

        return text

    def generate(self) -> tuple[list[str], list[str]]:
        """
        Generate synthetic document text and associated labels.

        Returns:
            Tuple[List[str], List[str]]: A tuple containing:
                - List of generated document texts
                - List of document type labels
        """
        if not self.generators:
            raise ValueError("No document generators defined.")

        texts, labels = [], []
        for _ in range(self.num_samples):
            doc_type = random.choice(list(self.generators.keys()))
            text = self.generators[doc_type]()

            if self.add_noise:
                text = self.add_random_formatting(text)

            texts.append(text)
            labels.append(doc_type)

        return texts, labels

    @classmethod
    def register_industry(cls, industry: str, generators: Dict[str, Callable]):
        """
        Registers a set of generators for a specific industry.
        """
        cls.INDUSTRY_GENERATORS[industry] = generators
