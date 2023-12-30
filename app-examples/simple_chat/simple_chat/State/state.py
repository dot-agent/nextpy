# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

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
    