import os
from typing import Any

from penelope.corpus import CorpusVectorizer, TokensTransformOpts, VectorizedCorpus
from penelope.corpus.readers import ExtractTaggedTokensOpts
from penelope.corpus.readers.interfaces import TextReaderOpts
from penelope.utility import getLogger

from ._tokenized_corpus_factory import create_corpus
from .utils import WorkflowException

logger = getLogger("penelope")

# pylint: disable=too-many-arguments


def execute_workflow(
    *,
    corpus_type: str,
    input_filename: str,
    output_folder: str,
    output_tag: str,
    create_subfolder: bool,
    filename_field: Any = None,
    filename_pattern: str = '*.*',
    count_threshold: int = None,
    tokens_transform_opts: TokensTransformOpts = None,
    extract_tokens_opts: ExtractTaggedTokensOpts = None,
    **_,
) -> VectorizedCorpus:

    if not os.path.isfile(input_filename):
        raise WorkflowException(f'no such file: {input_filename}')

    if len(filename_field or []) == 0:
        raise WorkflowException("please specify at least one filename field (e.g. --filename-field='year:_:1')")

    if not output_tag:
        raise WorkflowException("please specify output tag")

    if create_subfolder:
        output_folder = os.path.join(output_folder, output_tag)
        os.makedirs(output_folder, exist_ok=True)

    if VectorizedCorpus.dump_exists(tag=output_tag, folder=output_folder):
        VectorizedCorpus.remove(tag=output_tag, folder=output_folder)

    reader_opts = TextReaderOpts(
        filename_pattern=filename_pattern,
        filename_fields=filename_field,
        index_field=None,  # use filename
        as_binary=False,
    )

    corpus = create_corpus(
        corpus_type=corpus_type,
        input_filename=input_filename,
        tokens_transform_opts=tokens_transform_opts,
        reader_opts=reader_opts,
        extract_tokens_opts=extract_tokens_opts,
    )

    logger.info('Creating document-term matrix...')
    vectorizer = CorpusVectorizer()
    v_corpus = vectorizer.fit_transform(corpus, already_tokenized=True)

    if (count_threshold or 1) > 1:
        v_corpus = v_corpus.slice_by_n_count(count_threshold)

    logger.info('Saving vectorized corpus...')
    v_corpus.dump(tag=output_tag, folder=output_folder)

    VectorizedCorpus.dump_options(
        tag=output_tag,
        folder=output_folder,
        options={
            'input_filename': input_filename,
            'output_folder': output_folder,
            'output_tag': output_tag,
            'count_threshold': count_threshold,
            'reader_opts': reader_opts.props,
            'tokens_transform_opts': tokens_transform_opts.props,
            'extract_tokens_opts': extract_tokens_opts.props if extract_tokens_opts is not None else {},
        },
    )

    logger.info('Done!')

    return v_corpus
