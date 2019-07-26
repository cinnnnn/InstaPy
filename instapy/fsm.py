"""
Class to create all necessary environment for the Finite State Machine
"""

from transitions import Machine
import random


class FSMSession(Object):
    """
    Define all the states and transitions, callbacks of an instagram session

    Inputs: a set of configuration (what actions, how much, scheduled)
    Output: the state machine will perform the amount of actions configured and scheduled

    You will have no exact control on when a specific action is going to be done or when as
    everything is as random as possible

    """

    states = [
        'idle',
        'follow',
        'unfollow',
        'like',
        'comment',
        'interact',
        'watch',
        'get_data'
    ]

    transitions = [

    ]

    #currently safe numbers
    quota = {
        "peak_likes": (40, 400),
        "peak_comments":  (20, 200),
        "peak_follows": (20, 200),
        "peak_unfollows": (50, 200),
        "peak_server_calls": (300, 3500)
    }

    #can this be generated from states automatically?
    actions = {
        "do_idle": {},
        "do_follow": {},
        "do_unfollow": {},
        "do_like": {},
        "do_comment": {},
        "do_interact": {},
        "do_watch": {},
        "do_get_data": {}
    }


    # def __init__(self, quota: dict = None, actions: dict = None):
    #     """
    #     Initialization of the FSM with what we want to do
    #
    #     :param quota: the quota information
    #     :param actions: what we want to do
    #     """



def main():
    self.fsm_session = Machine('fsm_session', states=states, transitions=transitions, initial='idle')

