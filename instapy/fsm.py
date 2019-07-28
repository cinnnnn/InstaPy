"""
Class to create all necessary environment for the Finite State Machine
"""

from transitions import Machine
import random


class FSMSession(Object):
    """
    Define all the states and transitions, callbacks of an instagram session

    V1: target is to be able to reproduce a set of InstaPy primitives on individual user/post
    Integration will be very basic, we are just replacing the need to write a complicated script

    Inputs: a set of configuration (what actions, how much, scheduled)
    Output: the state machine will perform the amount of actions configured and scheduled

    You will have no exact control on when a specific action is going to be done or when
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
        'watched'
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
        {'trigger': 'do_gather_data', 'source': 'idle', 'dest': 'idle'},
        {'trigger': 'do_work', 'source': 'idle', 'dest': '*'}
    ]

    # Instapy functions to call for doing the triggered action
    # This is very problematic as there is no uniform prototyping and no clear boundaries when
    # and action start or finish. So different functions here covers different things
    # ideally we need a unified prototype (**kvargs) and unitary actions
    actions = [
        {'follow': 'follow_by_list'},
        {'unfollow': 'unfollow_user'},
        {'like': 'like_image'},
        {'comment': ''},
        {'interact': ''},
        {'watch': ''}
    ]

    machine = None

    #currently safe default numbers
    quota = {
        "peak_likes": (40, 400),
        "peak_comments":  (20, 200),
        "peak_follows": (20, 200),
        "peak_unfollows": (50, 200),
        "peak_server_calls": (300, 3500)
    }

    # the stacks permit to pass the actions between states if we need to
    # and it works by a simple .append(), .pop()
    # stack of posts to do actions on
    posts_stack = {}
    posts_stack_likes = {}
    posts_stack_comment = {}
    # stack of users to do action on
    users_stack = {}
    users_stack_follow = {}
    users_stack_interact = {}
    users_stack_unfollow = {}
    #stack of comments to do action
    comments_stack = {}
    comments_stack_like = {}
    comments_stack_reply = {}


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

        :return:
        """

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
                self.machine.trigger('do_gather_data')

        #we arrive at a permanent state of the FSM, we stay idle forever

    def go_follow(self):
        """
        execute the actions needed to follow a user
        :return:
        """
        # quota is plugged in directly into each action
        # so we should wait if we are over automatically
        # no need to plug that in
        print("doing the follow action")

    def go_unfollow(self):
        """
        execute the actions needed to unfollow a user
        :return:
        """
        # quota is plugged in directly into each action
        # so we should wait if we are over automatically
        # no need to plug that in
        print("doing the unfollow action")

    def on_enter_followed(self):
        """
        we had a successfull follow
        :return:
        """
        # update the fsm info
        # but not really needed as each function will update everything it need
        # into live session
        self.followed_action +=1

        # clean up
        self.users_stack_follow.pop()


    def on_enter_unfollowed(self):
        """
        we had an successfull unfollow
        :return:
        """
        self.unfollowed_action +=1

        self.users_stack_unfollow.pop()

    def do_gather_data(self):
        """
        This function should execute gathering data from the usual functions of a script
        for example if we want to do follow_likers, then we should call the InstaPy function that gather the username of the likers
        and so on...

        This might be difficult as the InstaPy code might not be organized to support those functions separately
        Shall we mock/rewrite those functions?? How do we solve this
        Have an fsm_ entry point in class InstaPy
        or we should just leave this complexity outside for the moment and just expect that the state machine is initialized with the correct
        users, post to work on
        :return:
        """
        print("do nothing for the moment???")



