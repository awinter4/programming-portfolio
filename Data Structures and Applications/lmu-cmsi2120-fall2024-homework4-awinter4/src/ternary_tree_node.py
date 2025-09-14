from dataclasses import dataclass
from typing import Optional


@dataclass
class TTNode:
    '''
    Internal storage of autocompleter search terms
    as represented using a Ternary Tree with TTNodes
    '''

    # A brief explainer on the following parameters:
    # For your base solution, you will not need to 
    # use word_end_priority and snail_trail_priority:
    # those are for the Extra Credit.

    # The way this DataClass is designed is that the 
    # only required argument when instantiating is 
    # letter. word_end is defaulted to False, but 
    # when you add a Node that is the end of an 
    # inserted word, be sure to change that 
    # boolean to True.

    letter: str
    word_end: bool = False
    
    word_end_priority: int = -1
    snail_trail_priority: int = -1

    left: Optional['TTNode'] = None
    middle: Optional['TTNode'] = None
    right: Optional['TTNode'] = None

# There are a handfull of ways to initialize this DataClass.
# Default:
# TTNode("s") - creates a TTNode where letter is
# set to "s", and all other parameters are the defaults
# outlined above.
# 
# With word_end:
# TTNode("s", True) - creates a TTNode where letter is
# set to "s", word_end is set to True, and all other
# parameters are the defaults outlined above.
# 
# The above works because letter and word_end are adjacent,
# making positional arguments possible. But let's say you
# want to assign "s" to letter, keep word_end as False, 
# but you want to assign the left Node to another Node
# with the letter "o".
# In this case, you can use keyword arguments:
# 
# TTNode("s", left = TTNode("o"))
# 
# This will assign letter and left, and keep everything
# else the same as defaults.