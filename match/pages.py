from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class FirstWP(WaitPage):
    template_name = 'match/MatchWP.html'




class ActivePage(Page):
    def is_displayed(self) -> bool:
        return self.player.active

class PassivePage(Page):
    def is_displayed(self) -> bool:
        return not self.player.active

page_sequence = [
    FirstWP,
    ActivePage,
    PassivePage,
]
