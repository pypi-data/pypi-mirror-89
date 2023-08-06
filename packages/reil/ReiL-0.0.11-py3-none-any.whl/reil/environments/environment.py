# -*- coding: utf-8 -*-
'''
Environment class
==================

The base class of all learning environments in which one or more `agents` act
on one or more `subjects`.
'''
import pathlib
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from reil import agents as rlagents
from reil import stateful
from reil import subjects as rlsubjects
from reil.datatypes import InteractionProtocol, ReilData
from reil.utils import functions
from reil.utils import instance_generator as rlgenerator

AgentSubjectTuple = Tuple[str, str]
Entity = Union[rlagents.Agent, rlsubjects.Subject]
EntityGenerator = Union[rlgenerator.InstanceGenerator[rlagents.Agent],
                        rlgenerator.InstanceGenerator[rlsubjects.Subject]]


class Environment(stateful.Stateful):
    '''
    Provide an interaction and learning environment for `agents` and
    `subjects`.

    Notes
    -----
    `Agents` act on `subjects` and receive the reward of their action and
    the new state of those `subjects`. Then `agents` learn based on this
    information to improve their actions.

    `Pass`: visiting all protocols in the interaction sequence, once.

    `Epoch`: For each subject, an epoch is one time reaching its terminal
    state. If the subject is an instance generator, then the generator should
    reach to terminal state, not just its current instance.
    '''
    # TODO: Statistics aggregators are not supported yet!
    # TODO: simulate_passes and simulate_one_pass do not return anything!

    def __init__(self,
                 entity_dict: Optional[
                     Dict[str, Union[Entity, EntityGenerator, str]]] = None,
                 **kwargs: Any):
        '''
        Arguments
        ---------
        entity_dict:
            a dictionary that contains `agents`, `subjects`, and
            `generators`.
        '''
        super().__init__(name=kwargs.get('name', __name__),
                         logger_name=kwargs.get('logger_name', __name__),
                         **kwargs)

        self._agents: Dict[str, rlagents.AgentType] = {}
        self._subjects: Dict[str, rlsubjects.SubjectType] = {}
        self._instance_generators: Dict[str, EntityGenerator] = {}
        self._assignment_list: Dict[AgentSubjectTuple, Union[int, None]] = \
            defaultdict(lambda: None)
        self._epochs: Dict[str, int] = defaultdict(int)
        self._history: Dict[AgentSubjectTuple, stateful.History] = defaultdict(
            lambda: [stateful.Observation()])
        self._agent_statistics: Dict[AgentSubjectTuple, List[ReilData]] = \
            defaultdict(list)
        self._subject_statistics: Dict[AgentSubjectTuple, List[ReilData]] = \
            defaultdict(list)

        if entity_dict is not None:
            self.add(entity_dict)

    def add(self,
            entity_dict: Dict[str, Union[Entity, EntityGenerator, str]]
            ) -> None:
        '''
        Add `agents` and `subjects` to the environment.

        Arguments
        ---------
        entity_dict:
            a dictionary consist of `agent`/ `subject` name and the
            respective entity. Names should be unique, otherwise overwritten.
            To assign one entity to multiple names, use the name in the
            first assignment as the value of the dict for other assignments.
            For example:
            >>> env.add({'agent_1': Agent(), 'agent_2': 'agent_1'})

            When using name as value, the name is being looked up first in
            instance generators, then agents, and finally subjects. Whichever
            contains the name first, the entity corresponding to that instance
            is being used.

        Notes
        -----
        Reusing an `InstanceGenerator` produces unintended consequences.

        Raises
        ------
        ValueError
            An entity is being reused without being defined first.

        TypeError
            The entity is niether an `agent` [generator] nor a `subject`
            [generator].
        '''
        for name, obj in entity_dict.items():
            if isinstance(obj, str):
                _obj = self._instance_generators.get(
                    obj, self._agents.get(
                        obj, self._subjects.get(obj)))
                if _obj is None:
                    raise ValueError(f'entity {obj} defined for {name} is '
                                     'not in the list of agents, subjects, '
                                     'and generators.')
            else:
                _obj = obj
            if isinstance(_obj, rlgenerator.InstanceGenerator):
                self._instance_generators.update({name: _obj})
            elif isinstance(_obj, rlagents.Agent):
                self._agents.update({name: _obj})
            elif isinstance(_obj, rlsubjects.Subject):
                self._subjects.update({name: _obj})
            else:
                raise TypeError(
                    f'entity {name} is niether an agent nor a subject.')

        for name, generator in self._instance_generators.items():
            _, obj = next(generator)
            if isinstance(obj, rlagents.Agent):
                self._agents.update({name: obj})
            elif isinstance(obj, rlsubjects.Subject):
                self._subjects.update({name: obj})
            else:
                raise TypeError(
                    f'entity {name} is niether an agent nor a subject.')

    def remove(self, entity_names: Tuple[str, ...]) -> None:
        '''
        Remove `agents`, `subjects`, or `instance_generators` from
        the environment.

        Arguments
        ---------
        entity_names:
            A list of `agent`/ `subject` names to be deleted.

        Notes
        -----
        This method removes the item from both `agents` and `subjects`
        lists. Hence, it is not recommended to use the same name for both
        an `agent` and a `subject`.
        '''
        for name in entity_names:
            if name in self._agents:
                del self._agents[name]
            if name in self._subjects:
                del self._subjects[name]
            if name in self._instance_generators:
                del self._instance_generators[name]

    def simulate_one_pass(self) -> None:
        '''
        Go through the interaction sequence for one pass and
        simulate interactions accordingly.
        '''
        raise NotImplementedError

    def simulate_passes(self, passes: int) -> None:
        '''
        Go through the interaction sequence for a number of passes and
        simulate interactions accordingly.

        Arguments
        ---------
        passes:
            The number of passes that simulation should go.
        '''
        for _ in range(passes):
            self.simulate_one_pass()

    def simulate_to_termination(self) -> None:
        '''
        Go through the interaction sequence and simulate interactions
        accordingly, until all `subjects` are terminated.

        Notes
        -----
        To avoid possible infinite loops caused by normal `subjects`,
        this method is only available if all `subjects` are generated
        by `instance generators`.

        Raises
        ------
        TypeError:
            Attempt to call this method will normal subjects in the interaction
            sequence.
        '''
        raise NotImplementedError

    @staticmethod
    def interact_once(agent_id: int,
                      agent_instance: rlagents.Agent,
                      subject_instance: rlsubjects.Subject,
                      protocol: InteractionProtocol,
                      epoch: int
                      ) -> Tuple[ReilData, ReilData, Union[ReilData, None]]:
        '''
        Allow `agent` and `subject` to interact once.

        Attributes
        ----------
        agent_id:
            Agent's ID by which it is registered at the subject.

        agent_instance:
            An instance of an `agent` that takes the action.

        subject_instance:
            An instance of a `subject` that computes reward, determines
            possible actions, and takes the action.

        protocol:
            An `InteractionProtocol` that specifies the state and reward
            function definitions.

        epoch:
            The epoch of of the current run. This value is used by the `agent`
            to determine the action.

        Returns
        -------
        :
            Reward received by `subject`  and state before taking an action and
            the action that `agent` took.

        Notes
        -----
        If the subject is terminated or no possible actions are available,
        `None` is returned for action.
        '''
        reward = subject_instance.reward(
            name=protocol.reward_function_name, _id=agent_id)

        state = subject_instance.state(name=protocol.state_name, _id=agent_id)
        if not subject_instance.is_terminated(agent_id):
            possible_actions = subject_instance.possible_actions(agent_id)
            if possible_actions:
                action = agent_instance.act(state, actions=possible_actions,
                                            epoch=epoch)
                subject_instance.take_effect(action, agent_id)
            else:
                action = None
        else:
            action = None

        return reward, state, action

    @classmethod
    def interact_n_times(cls,
                         agent_id: int,
                         agent_instance: rlagents.Agent,
                         subject_instance: rlsubjects.Subject,
                         protocol: InteractionProtocol,
                         epoch: int,
                         times: int = 1) -> stateful.History:
        '''
        Allow `agent` and `subject` to interact at most `times` times.

        Attributes
        ----------
        agent_id:
            Agent's ID by which it is registered at the subject.

        agent_instance:
            An instance of an `agent` that takes the action.

        subject_instance:
            An instance of a `subject` that computes reward, determines
            possible actions, and takes the action.

        protocol:
            An `InteractionProtocol` that specifies the state and reward
            function definitions.

        epoch:
            The epoch of of the current run. This value is used by the `agent`
            to determine the action.

        times:
            The number of times the `agent` and the `subject` should interact.

        Returns
        -------
        :
            A list of subject's reward and state before taking an action
            and agent's action.

        Notes
        -----
        If subject is terminated before "times" iterations, the result will
        be truncated and returned. In other words, the output will not
        necessarily have a lenght of "times".
        '''
        if subject_instance.is_terminated():
            return []

        trajectory = [stateful.Observation() for _ in range(times + 1)]
        for i in range(times):
            reward, state, action = cls.interact_once(
                agent_id, agent_instance, subject_instance, protocol, epoch)

            trajectory[i].reward = reward
            trajectory[i+1].state = state
            trajectory[i+1].action = action

            if action is None:
                if subject_instance.is_terminated(agent_id):
                    trajectory[i+1].reward = None
                    return trajectory[:i+2]

        return trajectory

    @classmethod
    def interact_while(cls,
                       agent_id: int,
                       agent_instance: rlagents.Agent,
                       subject_instance: rlsubjects.Subject,
                       protocol: InteractionProtocol,
                       epoch: int) -> stateful.History:
        '''
        Allow `agent` and `subject` to interact until `subject` is terminated.

        Attributes
        ----------
        agent_id:
            Agent's ID by which it is registered at the subject.

        agent_instance:
            An instance of an agent that takes the action.

        subject_instance:
            An instance of a subject that computes reward,
            determines possible actions, and takes the action.

        protocol:
            An `InteractionProtocol` that specifies the state and reward
            function definitions.

        epoch:
            The epoch of of the current run. This value is used by the agent
            to determine the action.

        Returns
        -------
        :
            A list of subject's reward and state before taking an action and
            agent's action.

        Notes
        -----
        For `instance generators`, only the current
        instance is run to termination, not the whole generator.
        '''
        trajectory = [stateful.Observation()]

        while not subject_instance.is_terminated(agent_id):
            reward, state, action = cls.interact_once(
                agent_id, agent_instance, subject_instance, protocol, epoch)

            trajectory[-1].reward = reward
            trajectory.append(stateful.Observation(state=state, action=action))

        return trajectory

    def append_observations(self,
                            agent_name: str,
                            subject_name: str,
                            observations: stateful.History) -> None:
        '''
        Append observations to the history of the given `agent` and `subject`.

        Arguments
        ---------
        agent_name:
            Name of the `agent` that the observations belong to.

        subject_name:
            Name of the `subject` that the observations belong to.

        observations:
            A `History` of `agent`/ `subject` interactions.
        '''
        if observations:
            self._history[(agent_name, subject_name)][-1].reward = \
                observations[0].reward
            self._history[(agent_name, subject_name)].extend(observations[1:])

    def assert_protocol(self, protocol: InteractionProtocol) -> None:
        '''
        Check whether the given protocol:

        * contains only entities that are known to the `environment`.

        * unit is one of the possible values.

        Arguments
        ---------
        protocol:
            An interaction protocol.

        Raises
        ------
        ValueError
            `agent` or `subject` is not defined.

        ValueError
            `unit` is not one of `interaction`, `instance`, or `epoch`.
        '''
        if protocol.agent.name not in self._agents:
            raise ValueError(f'Unknown agent name: {protocol.agent.name}.')
        if protocol.subject.name not in self._subjects:
            raise ValueError(f'Unknown subject name: {protocol.subject.name}.')
        if protocol.unit not in ('interaction', 'instance', 'epoch'):
            raise ValueError(
                f'Unknown unit: {protocol.unit}. '
                'It should be one of interaction, instance, or epoch. '
                'For subjects of non-instance generator, epoch and '
                'instance are equivalent.')
        # if (protocol.agent_name in self._instance_generators or
        #     protocol.subject_name in self._instance_generators) and

    def register_agents(self) -> None:
        '''
        Register all `agents` in the interaction sequence in their
        corresponding `subjects`.

        Notes
        -----
        When registration happens for the first time, the agents
        get any ID that subjects provide. However, in the follow up
        registrations, `agents` attempt to register with the same ID to
        have access to the same information.
        '''
        raise NotImplementedError

    def _reset_subject(self, subject_name: str) -> None:
        '''
        When a `subject` is terminated for all interacting `agents`, this
        function is called to reset the subject.

        If the subject is an `InstanceGenerator`, a new instance is created.
        If reset is successful, `epoch` is incremented by one.

        Attributes
        ----------
        subject_name:
            Name of the `subject` that is terminated.


        :meta private:
        '''
        if subject_name in self._instance_generators:
            # get a new instance if possible,
            # if not instance generator returns StopIteration.
            # So, increment epoch by 1, then if the generator is not
            # terminated, get a new instance.
            try:
                _, self._subjects[subject_name] = cast(
                    Tuple[int, rlsubjects.SubjectType],
                    next(self._instance_generators[subject_name]))
            except StopIteration:
                # TODO: self._aggregated
                self._epochs[subject_name] += 1
                if not self._instance_generators[subject_name].is_terminated():
                    _, self._subjects[subject_name] = cast(
                        Tuple[int, rlsubjects.SubjectType],
                        next(self._instance_generators[subject_name]))
        else:
            self._epochs[subject_name] += 1
            self._subjects[subject_name].reset()

    def manage_terminated_subjects(self) -> None:
        '''
        Go over all `subjects`. If terminated, collect terminal rewards,
        calculate stats, train related `agents`, and reset the `subject`.
        '''
        raise NotImplementedError

    def load(self,
             entity_name: Union[List[str], str] = 'all',
             filename: Optional[str] = None,
             path: Optional[Union[pathlib.Path, str]] = None) -> None:
        '''
        Load an entity or an `environment` from a file.

        Arguments
        ---------
        filename:
            The name of the file to be loaded.

        entity_name:
            If specified, that entity (`agent` or `subject`) is being
            loaded from file. 'all' loads an `environment`.

        Raises
        ------
        ValueError
            The filename is not specified.
        '''
        _filename: str = functions.get_argument(filename, self._name)
        _path = pathlib.Path(path if path is not None else self._path)

        if entity_name == 'all':
            super().load(filename=_filename, path=_path)
            self._agents: Dict[str, rlagents.AgentType] = {}
            self._subjects: Dict[str, rlsubjects.SubjectType] = {}
            for name, obj_type in self._env_data['agents']:
                self._agents[name] = obj_type.from_pickle(
                    path=(_path / f'{_filename}.data'), filename=name)
            for name, obj_type in self._env_data['subjects']:
                self._subjects[name] = obj_type.from_pickle(
                    path=(_path / f'{_filename}.data'), filename=name)

            del self._env_data

        else:
            for obj in entity_name:
                if obj in self._agents:
                    self._agents[obj].load(
                        path=(_path / f'{_filename}.data'), filename=obj)
                    self._agents[obj].reset()
                elif obj in self._subjects:
                    self._subjects[obj].load(
                        path=(_path / f'{_filename}.data'), filename=obj)
                    self._subjects[obj].reset()

    def save(self,
             filename: Optional[str] = None,
             path: Optional[Union[pathlib.Path, str]] = None,
             data_to_save: Union[List[str], str] = 'all'
             ) -> Tuple[pathlib.Path, str]:
        '''
        Save an entity or the `environment` to a file.

        Arguments
        ---------
        filename:
            The name of the file to be saved.

        path:
            The path of the file to be saved.

        entity_name:
            If specified, that entity (`agent` or `subject`) is being saved
            to file. 'all' saves the `environment`.

        Raises
        ------
        ValueError
            The filename is not specified.
        '''
        _filename = functions.get_argument(filename, self._name)
        _path = pathlib.Path(path if path is not None else self._path)

        if data_to_save == 'all':
            self._env_data: Dict[str, List[Any]] = defaultdict(list)

            for name, agent in self._agents.items():
                _, fn = agent.save(
                    path=_path / f'{_filename}.data', filename=name)
                self._env_data['agents'].append((fn, type(agent)))

            for name, subject in self._subjects.items():
                _, fn = subject.save(
                    path=_path / f'{_filename}.data', filename=name)
                self._env_data['subjects'].append((fn, type(subject)))

            super().save(
                filename=_filename, path=_path,
                data_to_save=tuple(v for v in self.__dict__
                                   if v not in ('_agents', '_subjects')))

            del self._env_data
        else:
            for obj in data_to_save:
                if obj in self._agents:
                    self._agents[obj].save(
                        path=_path / f'{_filename}.data', filename=obj)
                elif obj in self._subjects:
                    self._subjects[obj].save(
                        path=_path / f'{_filename}.data', filename=obj)

        return _path, _filename

    def __repr__(self) -> str:
        try:
            return super().__repr__() + '\n Agents:\n' + \
                '\n\t'.join((a.__repr__() for a in self._agents.values())) + \
                '\nSubjects:\n' + \
                '\n\t'.join((s.__repr__() for s in self._subjects.values()))
        except AttributeError:
            return super().__repr__()
