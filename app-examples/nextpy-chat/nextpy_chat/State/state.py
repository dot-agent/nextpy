import nextpy as xt

class QA(xt.Base):
    """A question and answer pair."""
    question: str
    answer: str
    like_bg: str = 'white' 
    dislike_bg: str = 'white'
    index: int 


class State(xt.State):
    pass
    