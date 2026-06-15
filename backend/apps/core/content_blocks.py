from apps.base.blocks import TimelineBlock, ProgramProposalBlock
from apps.program.blocks import Excursions

simple_section_content = [
    ("excursion_table", Excursions()),
    ("program_proposal", ProgramProposalBlock()),
    ("timeline", TimelineBlock()),
]
