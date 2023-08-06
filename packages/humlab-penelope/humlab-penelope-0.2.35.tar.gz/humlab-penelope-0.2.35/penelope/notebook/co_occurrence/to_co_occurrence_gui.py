from dataclasses import dataclass, field
from typing import Callable, Set

import ipywidgets as widgets
from penelope.co_occurrence import ContextOpts
from penelope.pipeline import CorpusConfig
from penelope.utility import get_logger

from ..gui_base import BaseGUI, button_layout, default_layout

logger = get_logger('penelope')

tooltips = {
    '_context_width': "Max distance to the midmost word, window size two times this value plus one",
    '_ignore_concept': "If checked, the concept words (if specified) are filtered out",
    '_concept': "If specified, then only windows having a focus word in the middle are considered.",
}
view = widgets.Output(layout={"border": "1px solid black"})


@dataclass
class ComputeGUI(BaseGUI):

    partition_key: str = field(default='year')

    _context_width = widgets.IntSlider(
        description='',
        min=1,
        max=40,
        step=1,
        value=2,
        layout=default_layout,
        # tooltip=tooltips['_context_width'],
    )
    _concept = widgets.Text(
        value='',
        placeholder='Use comma (,) as word delimiter',
        description='',
        disabled=False,
        layout=widgets.Layout(width='280px'),
        # tooltip=tooltips['_concept'],
    )
    _ignore_concept = widgets.ToggleButton(
        value=False,
        description='No Concept',
        icon='check',
        layout=button_layout,
        # tooltip=tooltips['_ignore_concept'],
    )

    def layout(self, hide_input=False, hide_output=False):

        placeholder: widgets.VBox = super().extra_placeholder
        extra_layout = widgets.HBox(
            [
                widgets.VBox([widgets.HTML("<b>Context distance</b>"), self._context_width]),
                widgets.VBox([widgets.HTML("<b>Concept</b>"), self._concept, self._ignore_concept]),
            ]
        )
        placeholder.children = [extra_layout]
        layout = super().layout(hide_input, hide_output)
        return layout

    def setup(self, *, config: CorpusConfig, compute_callback: Callable):
        super().setup(config=config, compute_callback=compute_callback)
        return self

    @property
    def context_opts(self) -> ContextOpts:
        return ContextOpts(
            concept=self.concept_tokens,
            context_width=self._context_width.value,
            ignore_concept=self._ignore_concept.value,
        )

    @property
    def concept_tokens(self) -> Set[str]:
        _concepts_str = [x.strip() for x in self._concept.value.strip().split(',') if len(x.strip()) > 1]
        if len(_concepts_str) == 0:
            return {}
        return set(_concepts_str)

    @staticmethod
    def create(
        *,
        corpus_folder: str,
        corpus_config: CorpusConfig,
        compute_callback: Callable = None,
        done_callback: Callable = None,
    ) -> "ComputeGUI":
        """Returns a GUI for turning a corpus pipeline to co-occurrence data"""
        corpus_config.folder(corpus_folder)
        gui = ComputeGUI(
            default_corpus_path=corpus_folder,
            default_corpus_filename=(corpus_config.pipeline_payload.source or ''),
            default_target_folder=corpus_folder,
        ).setup(
            config=corpus_config,
            compute_callback=lambda g: compute_callback(
                corpus_config=corpus_config,
                args=g,
                partition_key=gui.partition_key,
                done_callback=done_callback,
            ),
        )

        return gui
