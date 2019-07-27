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

    # all_possible_states
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

    # all possible transitions
    transitions = [
        {'trigger': 'go_idle', 'source': '*', 'dest': 'idle'},
        {'trigger': 'go_follow', 'source': 'idle', 'dest': 'followed'},
        {'trigger': 'go_unfollow', 'source': 'idle', 'dest': 'unfollowed'},
        {'trigger': 'go_like', 'source': 'idle', 'dest': 'liked'},
        {'trigger': 'go_comment', 'source': 'idle', 'dest': 'commented'},
        {'trigger': 'go_interact', 'source': ['followed', 'liked'], 'dest': 'interacted'},
        {'trigger': 'go_watch', 'source': 'idle', 'dest': 'watched'},
        {'trigger': 'go_pause', 'source': 'idle', 'dest': 'paused'},
        {'trigger': 'do_gather_data', 'source': 'idle', 'dest': 'idle'},
        {'trigger': 'do_work', 'source': 'idle', 'dest': '*'}
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
    posts_stack = {}
    posts_stack_likes = {}
    posts_stack_comment = {}
    #stack of users to do action on
    users_stack = {}
    users_stack_follow = {}
    users_stack_interact = {}
    users_stack_unfollow = {}


    def __init__(self, quota: dict = None, actions: dict = None):
        """
        Initialization of the FSM with what we want to do

        :param quota: the quota information
        :param actions: what we want to do
        """
        #we should initialize the state machine according to the config
        #no need to have followed states if following is not configured

        print("auto-configure states and transitions here!")
        self.machine = Machine(model=self, states=states, transitions=transitions, initial='idle')

    def on_enter_idle(self):
        """
        check if we still have some quota
        otherwise trigger pause
        :return:
        """
        if random.randint(0,100) <50:
            print("[FSM] - state {}=".format(self.machine.state))
            self.machine.trigger('go_pause')
        else:
            self.machine.trigger('do_work')

    def on_exit_idle(self):
        """

        :return:
        """

    def do_work(self):
        """
        execute the actions needed to go to the next actions
        ideally we randomize the states we want to go in and we trigger them
        :return:
        """
        # here we should have in the state machine only the states we can do
        # because we have data, otherwise the only state that it can go is in idle
        next_transition="go_"+random.sample(self.states,1)
        self.machine.trigger(next_transition)

    def go_idle(self):
        """
        do more work or fetch more data else stay idle
        :return:
        """
        if (len(self.users_stack) > 0) or (len(self.posts_stack) >0):
            self.machine.trigger('do_work')
        else:
            if self.nomore_data is False:
                self.machnie.trigger('do_get_data')

        #we arrive at a permanent state of the FSM, we stay idle forever

    def go_follow(self):
        """
        execute the actions needed to follow a user
        :return:
        """
        print("doing the follow action")

    def go_unfollow(self):
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
        print("action_delay")

        #clean up
        user=self.users_stack_follow.pop()
        if Setting.do_interact:
            self.users_stack_interact.append(user)
            self.trigger("go_interact")
        #more actions possible here if needed



