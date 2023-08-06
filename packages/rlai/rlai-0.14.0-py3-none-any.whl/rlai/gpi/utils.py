import os
import pickle
import statistics
from typing import Dict, Optional, List, Callable

import matplotlib.pyplot as plt

from rlai.agents.mdp import MdpAgent
from rlai.environments.openai_gym import Gym


def plot_policy_iteration(
        iteration_average_reward: List[float],
        iteration_total_states: List[int],
        iteration_num_states_updated: List[int],
        elapsed_seconds_average_rewards: Dict[int, List[float]]
):
    """
    Plot status of policy iteration.

    :param iteration_average_reward: Average reward per iteration.
    :param iteration_total_states: Total number of states per iteration.
    :param iteration_num_states_updated: Number of states updated per iteration.
    :param elapsed_seconds_average_rewards: Elapsed seconds and average rewards.
    """

    plt.close('all')

    # noinspection PyTypeChecker
    fig, axs = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(12, 6))

    # reward per iteration
    ax = axs[0]
    ax.plot(iteration_average_reward, '-', label='average')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Reward per episode')
    ax.legend(loc='upper left')
    ax.grid()

    # twin-x states per iteration
    state_space_ax = ax.twinx()
    state_space_ax.plot(iteration_total_states, '--', color='orange', label='total')
    state_space_ax.plot(iteration_num_states_updated, '-', color='orange', label='updated')
    state_space_ax.set_yscale('log')
    state_space_ax.set_ylabel('# states')
    state_space_ax.legend(loc='center right')

    # reward over elapsed time
    ax = axs[1]
    seconds = list(sorted(elapsed_seconds_average_rewards.keys()))
    ax.plot(seconds, [statistics.mean(elapsed_seconds_average_rewards[s]) for s in seconds], '-', label='average')
    ax.set_xlabel('Elapsed time (seconds)')
    ax.set_ylabel('Reward per episode')
    ax.legend()
    ax.grid()

    plt.show()


def resume_from_checkpoint(
        checkpoint_path: str,
        resume_function: Callable,
        new_checkpoint_path: Optional[str] = None,
        resume_args_mutator: Callable = None,
        **new_args
) -> MdpAgent:
    """
    Resume the execution of a previous optimization based on a stored checkpoint.

    :param checkpoint_path: Path to checkpoint file.
    :param resume_function: Function to resume.
    :param new_checkpoint_path: Path to new checkpoint file, if the original should be left as it is. Pass `None` to
    use and overwrite `checkpoint_path` with new checkpoints.
    :param resume_args_mutator: A function called prior to resumption. This function will be passed a dictionary of
    arguments comprising the checkpoint. The passed function can change these arguments if desired.
    :param new_args: As a simpler alternative to `resume_args_mutator`, pass any keyword arguments that should replace
    those in the checkpoint. Only those with non-None values will be used.
    :return: The updated agent.
    """

    if new_checkpoint_path is None:
        new_checkpoint_path = checkpoint_path

    print('Reading checkpoint file to resume...', end='')
    with open(os.path.expanduser(checkpoint_path), 'rb') as checkpoint_file:
        resume_args = pickle.load(checkpoint_file)
    print('.done')

    resume_args['checkpoint_path'] = os.path.expanduser(new_checkpoint_path)

    # because the native gym environments cannot be pickled, we only retain a string identifier for the native gym
    # object as the value of `environment.gym_native`. the only way to resume such an environment is for the caller to
    # pass in an instantiated gym environment as a new argument value. the id of this object must match the id in the
    # resume args's environment.gym_native. if it does match, then grab the native gym environment and use it in the
    # resume args.
    resume_environment = resume_args.get('environment')
    if isinstance(resume_environment, Gym):

        passed_environment = new_args.get('environment')
        if passed_environment is None:
            raise ValueError('No environment passed when resuming an assumed OpenAI Gym environment.')

        passed_environment: Gym

        passed_id = passed_environment.gym_native.spec.id
        if passed_id != resume_environment.gym_native:
            raise ValueError(f'Attempted to resume Gym environment {resume_environment.gym_native}, but passed environment is {passed_id}')

        resume_environment.gym_native = passed_environment.gym_native

        del new_args['environment']

    if new_args is not None:
        resume_args.update({
            arg: v
            for arg, v in new_args.items()
            if v is not None
        })

    if resume_args_mutator is not None:
        resume_args_mutator(**resume_args)

    resume_function(**resume_args)

    return resume_args['agent']
