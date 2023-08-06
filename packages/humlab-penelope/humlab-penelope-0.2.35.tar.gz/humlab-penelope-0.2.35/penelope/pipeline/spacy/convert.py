from typing import Any, Dict, Iterable, List, Union

import pandas as pd
import spacy
from penelope.utility import deprecated, filter_dict
from spacy.language import Language
from spacy.tokens import Doc


def _filter_tokens_by_attribute_values(spacy_doc, attribute_value_filters):

    tokens = spacy_doc

    if attribute_value_filters is None:
        return tokens

    if len(attribute_value_filters) == 0:
        return tokens

    # Treat common attrbiutes explicitly for performance
    if 'is_space' in attribute_value_filters:
        value = attribute_value_filters['is_space']
        tokens = (t for t in tokens if t.is_space == value)

    if 'is_punct' in attribute_value_filters:
        value = attribute_value_filters['is_punct']
        tokens = (t for t in tokens if t.is_punct == value)

    attribute_value_filters = filter_dict(attribute_value_filters, ('is_space', 'is_punct'), filter_out=True)

    if len(attribute_value_filters) > 0:
        tokens = (t for t in spacy_doc if all([getattr(t, attr) == value for attr, value in attribute_value_filters]))

    return tokens


def spacy_doc_to_tagged_frame(
    *,
    spacy_doc: Doc,
    attributes: List[str],
    attribute_value_filters: Dict[str, Any],
) -> pd.DataFrame:
    """Returns token attribute values from a spacy doc a returns a data frame with given attributes as columns"""
    tokens = _filter_tokens_by_attribute_values(spacy_doc, attribute_value_filters)

    df = pd.DataFrame(
        data=[tuple(getattr(token, x, None) for x in attributes) for token in tokens],
        columns=attributes,
    )
    return df


def text_to_tagged_frame(
    document: str,
    attributes: List[str],
    attribute_value_filters: Dict[str, Any],
    nlp: Language,
) -> pd.DataFrame:
    """Loads a single text into a spacy doc and returns a data frame with given token attributes columns"""
    return spacy_doc_to_tagged_frame(
        spacy_doc=nlp(document),
        attributes=attributes,
        attribute_value_filters=attribute_value_filters,
    )


def texts_to_tagged_frames(
    stream: Iterable[str],
    attributes: List[str],
    attribute_value_filters: Dict[str, Any],
    language: Union[Language, str] = "en_core_web_sm",
) -> Iterable[pd.DataFrame]:
    """[summary]

    Parameters
    ----------
    stream : Iterable[str]
        A sequence of text stream
    attributes : List[str]
        A list of spaCy Token properties. Each property will be a column in the returned data frame.
        See https://spacy.io/api/token#attributes for valid properties.
        Example:
        "i", "text", "lemma(_)", "pos(_)", "tag(_)", "dep(_)", "shape",
            "is_alpha", "is_stop", "is_punct", "is_space", "is_digit"


    language : Union[Language, str], optional
        spaCy.Language or a string that specifies the language, by default "en_core_web_sm"

    Returns
    -------
    pd.DataFrame
        A data frame with columns corresponding to each given attribute

    Yields
    -------
    Iterator[pd.DataFrame]
        Seqence of documents represented as data frames
    """

    nlp: Language = spacy.load(language, disable=_get_disables(attributes)) if isinstance(language, str) else language

    for document in stream:
        yield text_to_tagged_frame(document, attributes, attribute_value_filters, nlp)


@deprecated
def filter_by_tags(doc, filter_opts, mask):

    if "is_space" in doc.columns:
        if not filter_opts.is_space:
            mask &= ~(doc.is_space)

    if "is_punct" in doc.columns:
        if not filter_opts.is_punct:
            mask &= ~(doc.is_punct)

    if filter_opts.is_alpha is not None:
        if "is_alpha" in doc.columns:
            mask &= doc.is_alpha == filter_opts.is_alpha

    if filter_opts.is_digit is not None:
        if "is_digit" in doc.columns:
            mask &= doc.is_digit == filter_opts.is_digit

    if filter_opts.is_stop is not None:
        if "is_stop" in doc.columns:
            mask &= doc.is_stop == filter_opts.is_stop

    return mask


def _get_disables(attributes):
    disable = ['vectors', 'textcat']
    if not any('ent' in x for x in attributes):
        disable.append('ner')

    if not any('dep' in x for x in attributes):
        disable.append('parser')
    return disable


# def extract_text_to_vectorized_corpus(
#     source: TextSource,
#     nlp: Language,
#     *,
#     reader_opts: TextReaderOpts,
#     transform_opts: TextTransformOpts,
#     extract_tagged_tokens_opts: ExtractTaggedTokensOpts,
#     tagged_tokens_filter_opts: TeagedTokensFilterOpts,
#     vectorize_opts: VectorizeOpts,
#     document_index: pd.DataFrame = None,
# ) -> VectorizedCorpus:
#     payload = interfaces.PipelinePayload(source=source, document_index=document_index)
#     pipeline = (
#         spacy_pipeline.SpacyPipeline(payload=payload)
#         .load(reader_opts=reader_opts, transform_opts=transform_opts)
#         .text_to_spacy(nlp=nlp)
#         .spacy_to_dataframe(nlp=nlp, attributes=['text', 'lemma_', 'pos_'])
#         .dataframe_to_tokens(extract_tokens_opts=extract_tokens_opts)
#         .tokens_to_text()
#         .to_dtm(vectorize_opts)
#     )

#     corpus = pipeline.resolve()

#     return corpus
