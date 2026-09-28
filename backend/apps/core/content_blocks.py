from apps.base.blocks import ProgramProposalBlock, TimelineBlock
from apps.program.blocks import Excursions
from apps.registration.blocks import VueJsBlock

simple_section_content = [
    ("excursion_table", Excursions()),
    ("program_proposal", ProgramProposalBlock()),
    ("timeline", TimelineBlock()),
    ("vue_js", VueJsBlock()),
]
