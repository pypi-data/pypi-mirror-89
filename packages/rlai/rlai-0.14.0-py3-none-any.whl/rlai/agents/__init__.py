from abc import ABC, abstractmethod
from argparse import Namespace, ArgumentParser
from typing import Tuple, List, final, Optional, Dict

from numpy.random import RandomState

from rlai.actions import Action
from rlai.meta import rl_text
from rlai.policies import Policy
from rlai.states import State
from rlai.states.mdp import MdpState


@rl_text(chapter='Agents', page=1)
class Agent(ABC):
    """
    Base class for all agents.
    """

    @classmethod
    def parse_arguments(
            cls,
            args
    ) -> Tuple[Namespace, List[str]]:
        """
        Parse arguments.

        :param args: Arguments.
        :return: 2-tuple of parsed and unparsed arguments.
        """

        parser = ArgumentParser(allow_abbrev=False)

        return parser.parse_known_args(args)

    @classmethod
    @abstractmethod
    def init_from_arguments(
            cls,
            args: List[str],
            random_state: RandomState,
            pi: Optional[Policy]
    ) -> List:
        """
        Initialize a list of agents from arguments.

        :param args: Arguments.
        :param random_state: Random state.
        :param pi: Policy.
        :return: List of agents.
        """
        pass

    def reset_for_new_run(
            self,
            state: State
    ):
        """
        Reset the agent to a state prior to any learning.

        :param state: New state.
        """

        self.most_recent_action = None
        self.most_recent_action_tick = None
        self.most_recent_state = state
        self.most_recent_state_tick = 0
        self.N_t_A = {a: 0.0 for a in self.N_t_A}

    def sense(
            self,
            state: State,
            t: int
    ):
        """
        Pass the agent state information to sense.

        :param state: State.
        :param t: Time tick for `state`.
        """

        self.most_recent_state = state
        self.most_recent_state_tick = t

    @final
    def act(
            self,
            t
    ) -> Action:
        """
        Request an action from the agent.

        :param t: Current time step.
        :return: Action
        """

        a = self.__act__(t=t)

        if a is None:
            raise ValueError('Agent returned action of None.')

        if not self.most_recent_state.is_feasible(a):
            raise ValueError(f'Action {a} is not feasible in state {self.most_recent_state}')

        self.most_recent_action = a
        self.most_recent_action_tick = t

        if a not in self.N_t_A:
            self.N_t_A[a] = 0

        self.N_t_A[a] += 1

        return a

    @abstractmethod
    def __act__(
            self,
            t: int
    ) -> Action:
        """
        Request an action from the agent.

        :param t: Current time step.
        :return: Action
        """
        pass

    def reward(
            self,
            r: float
    ):
        """
        Reward the agent.

        :param r: Reward.
        """
        pass

    def __init__(
            self,
            name: str,
            random_state: RandomState,
    ):
        """
        Initialize the agent.

        :param name: Name of the agent.
        :param random_state: Random state.
        """

        self.name = name
        self.random_state = random_state

        self.most_recent_action: Optional[Action] = None
        self.most_recent_action_tick: Optional[int] = None
        self.most_recent_state: Optional[State] = None
        self.most_recent_state_tick: Optional[int] = None
        self.N_t_A: Dict[Action, int] = {}

    def __str__(
            self
    ):
        """
        Return name.

        :return: Name.
        """

        return self.name


@rl_text(chapter='Agents', page=1)
class Human(Agent):
    """
    An interactive, human-driven agent that prompts for actions at each time step.
    """

    @classmethod
    def init_from_arguments(
            cls,
            args: List[str],
            random_state: RandomState,
            pi: Optional[Policy]
    ) -> List:
        """
        Not implemented. Will raise exception.
        """

        raise ValueError('Not implemented')

    def __act__(
            self,
            t: int
    ) -> Action:
        """
        Prompt the human user for input.

        :param t: Time step.
        :return: Action.
        """

        action = None

        while action is None:

            prompt = 'Please select from the following actions:  '

            self.most_recent_state: MdpState

            a_name_i = {
                a.name: i
                for i, a in enumerate(self.most_recent_state.AA)
            }

            for i, name in enumerate(sorted(a_name_i.keys())):
                prompt += f'{", " if i > 0 else ""}{name}'

            prompt += '\nEnter your selection:  '

            try:
                chosen_name = input(prompt)
                action = self.most_recent_state.AA[a_name_i[chosen_name]]
            except Exception:
                pass

        return action

    def __init__(
            self
    ):
        """
        Initialize the agent.
        """

        super().__init__(
            name='human',
            random_state=None
        )
