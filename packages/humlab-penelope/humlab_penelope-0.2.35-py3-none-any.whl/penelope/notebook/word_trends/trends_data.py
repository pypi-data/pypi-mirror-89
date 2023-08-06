from dataclasses import dataclass, field
from typing import Dict, List

import pandas as pd
import penelope.common.goodness_of_fit as gof
from penelope.corpus import VectorizedCorpus


@dataclass
class TrendsOpts:
    normalize: bool
    smooth: bool
    group_by: str
    word_count: int
    words: List[str]
    descending: bool = False


@dataclass
class TrendsData:

    corpus: VectorizedCorpus = None
    corpus_folder: str = None
    corpus_tag: str = None
    compute_options: Dict = None

    goodness_of_fit: pd.DataFrame = None
    most_deviating_overview: pd.DataFrame = None
    most_deviating: pd.DataFrame = None

    _transformed_corpus: VectorizedCorpus = None
    _transformed_is_normalized = False
    _transformed_grouped_by = 'year'

    n_count: int = 25000

    memory: dict = field(default_factory=dict)

    def update(
        self,
        *,
        corpus: VectorizedCorpus = None,
        corpus_folder: str = None,
        corpus_tag: str = None,
        n_count: int = None,
    ) -> "TrendsData":

        if (corpus or self.corpus) is None:
            raise ValueError("TrendsData: Corpus is NOT LOADED!")

        self.n_count = n_count or self.n_count
        self.corpus = (corpus or self.corpus).group_by_year()
        self.corpus_folder = corpus_folder or self.corpus_folder
        self.corpus_tag = corpus_tag or self.corpus_tag

        self.compute_options = VectorizedCorpus.load_options(tag=self.corpus_tag, folder=self.corpus_folder)
        self.goodness_of_fit = gof.compute_goddness_of_fits_to_uniform(
            self.corpus, None, verbose=True, metrics=['l2_norm', 'slope']
        )
        self.most_deviating_overview = gof.compile_most_deviating_words(self.goodness_of_fit, n_count=self.n_count)
        self.most_deviating = gof.get_most_deviating_words(
            self.goodness_of_fit, 'l2_norm', n_count=self.n_count, ascending=False, abs_value=True
        )
        return self

    def remember(self, **kwargs) -> "TrendsData":
        self.memory.update(**kwargs)
        return self

    def get_corpus(self, normalize: bool, group_by: str) -> VectorizedCorpus:

        if self._transformed_corpus is None:
            self._transformed_corpus = self.corpus
            self._transformed_grouped_by = 'year'
            self._transformed_is_normalized = False

        if group_by != self._transformed_grouped_by or normalize != self._transformed_is_normalized:
            self._transformed_corpus = self.corpus.group_by_period(period=group_by)
            if normalize:
                self._transformed_corpus = self._transformed_corpus.normalize_by_raw_counts()
            self._transformed_grouped_by = group_by
            self._transformed_is_normalized = normalize

        return self._transformed_corpus

    def find_word_indices(self, opts: TrendsOpts) -> List[int]:
        indices: List[int] = self.get_corpus(
            group_by=opts.group_by, normalize=opts.normalize
        ).find_matching_words_indices(opts.words, opts.word_count, descending=opts.descending)
        return indices

    def find_words(self, opts: TrendsOpts) -> List[str]:
        words: List[int] = self.get_corpus(group_by=opts.group_by, normalize=opts.normalize).find_matching_words(
            opts.words, opts.word_count, descending=opts.descending
        )
        return words


# words: List[str], n_count: int, group_by: str, normalize: bool)
