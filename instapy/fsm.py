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
        'followed',
        'unfollowed',
        'liked',
        'commented',
        'interacted',
        'watched',
        'paused'
    ]

    transitions = [
        {'trigger': 'do_idle', 'source': '*', 'dest': 'idle'},
        {'trigger': 'do_follow', 'source': 'idle', 'dest': 'followed'},
        {'trigger': 'do_unfollow', 'source': 'idle', 'dest': 'unfollowed'},
        {'trigger': 'do_like', 'source': 'idle', 'dest': 'liked'},
        {'trigger': 'do_comment', 'source': 'idle', 'dest': 'commented'},
        {'trigger': 'do_interact', 'source': 'followed', 'dest': 'interacted'},
        {'trigger': 'do_interact', 'source': 'liked', 'dest': 'interacted'},
        {'trigger': 'do_watch', 'source': 'idle', 'dest': 'watched'},
        {'trigger': 'do_pause', 'source': 'idle', 'dest': 'paused'},

    ]

    #currently safe numbers
    quota = {
        "peak_likes": (40, 400),
        "peak_comments":  (20, 200),
        "peak_follows": (20, 200),
        "peak_unfollows": (50, 200),
        "peak_server_calls": (300, 3500)
    }

    machine = None

    #stack of posts to do actions on
    posts_stack_likes = {}
    posts_stack_interact = {}
    posts_stack_comment = {}
    #stack of users to do action on
    users_stack = {}
    users_stack_follow = {}
    users_stack_unfollow = {}


    def __init__(self, quota: dict = None, actions: dict = None):
        """
        Initialization of the FSM with what we want to do

        :param quota: the quota information
        :param actions: what we want to do
        """
        self.machine = Machine(model=self, states=states, transitions=transitions, initial='idle')

    def on_enter_idle(self):
        """
        check if we still have some quota
        otherwise trigger pause
        :return:
        """
        if random.randint(0,100) <50:
            self.machine.trigger('do_pause')

    def on_exit_idle(self):
        """

        :return:
        """

    def do_idle(self):
        """
        execute the actions needed to go to the next actions
        ideally we randomize the states we want to go in and we trigger them
        :return:
        """

        self.machine.trigger(random.sample(self.states,1))

    def do_follow(self):
        """
        execute the actions needed to follow a user
        :return:
        """
        print("doing the follow action")

    def do_unfollow(self):
        """
        execute the actions needed to unfollow a user
        :return:
        """
        print("doing the unfollow action")

    def on_enter_followed(self):
        """
        we had a successfull follow
        :return:
        """
        self.followed +=1
        #update the db
        #do all what is needed to do

        #clean up
        user=self.users_stack_follow.pop()
        if Setting.do_interact:
            self.users_stack_interact.append(user)
        #more actions possible here if needed



