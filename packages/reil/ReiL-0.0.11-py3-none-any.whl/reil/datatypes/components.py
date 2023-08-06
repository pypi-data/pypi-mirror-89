# -*- coding: utf-8 -*-
'''
PrimaryComponent and SecondayComponent classes
=============================================

A datatype used to specify entity components, such as `state`, `reward`,
and `statistic`.
'''


import dataclasses
import functools
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast

from reil.datatypes import ReilData
from reil.stats import ReilFunction

SubComponentInfo = Tuple[Callable[..., Dict[str, Any]], Tuple[str, ...]]


@dataclasses.dataclass
class SubComponentInstance:
    '''
    A `dataclass` to store an instance of a sub component.

    :meta private:
    '''
    name: str
    fn: Optional[Callable[..., Any]] = None
    args: Union[str, Dict[str, Any]] = dataclasses.field(default_factory=dict)


class PrimaryComponent:
    '''
    The datatype to specify primary component, e.g., `state`.
    '''

    def __init__(
        self,
        available_sub_components: Optional[Dict[str, SubComponentInfo]] = None,
    ) -> None:
        '''
        Parameters
        ----------
        available_sub_components:
            A dictionary with sub component names as keys and a tuple of
            function and its argument list as values.
        '''
        self._available_sub_components: Dict[str, SubComponentInfo] = {}
        self._definitions: Dict[str,
                                List[SubComponentInstance]] = defaultdict(list)

        if available_sub_components is not None:
            self.sub_components = available_sub_components

    @property
    def sub_components(self) -> Dict[str, SubComponentInfo]:
        '''Get and set the dictionary of sub components.

        Returns
        -------
        :
            Sub components

        Notes
        -----
        Sub components info can only be set once.
        '''
        return self._available_sub_components

    @sub_components.setter
    def sub_components(self, sub_components: Dict[str, SubComponentInfo]):
        if self._available_sub_components:
            raise ValueError('Available sub components list is already set. '
                             'Cannot modify it.')
        self._available_sub_components = sub_components

    def add_definition(self,
                       name: str,
                       *sub_components: Tuple[str, Dict[str, Any]]) -> None:
        '''Add a new component definition.

        Parameters
        ----------
        name:
            The name of the new component.

        sub_components:
            Sub components that form this new component. Each sub component
            should be specified as a tuple. The first item is the name of the
            sub component, and the second item is a dictionary of kwargs and
            values for that sub component.

        Raises
        ------
        ValueError
            Definition already exists for this name.

        ValueError
            Unknown sub component.

        ValueError
            Unknown keyword argument.
        '''
        _name = name.lower()
        if _name in self._definitions:
            raise ValueError(f'Definition {name} already exists.')

        unknown_sub_components = set(
            sc for sc, _ in sub_components).difference(
            self._available_sub_components)

        if unknown_sub_components:
            raise ValueError('Unknown sub components: '
                             f'{unknown_sub_components}')

        for sub_comp_name, kwargs in sub_components:
            fn, arg_list = self._available_sub_components[sub_comp_name]

            unknown_keywords = set(kwargs).difference(arg_list)
            if unknown_keywords:
                raise ValueError(
                    f'Unknown keyword argument(s): {unknown_keywords}.')

            self._definitions[_name].append(
                SubComponentInstance(name=sub_comp_name,
                                     fn=fn,
                                     args=kwargs))

    @property
    def definitions(self) -> Dict[str, List[SubComponentInstance]]:
        '''Return the dictionary of component definitions.

        Returns
        -------
        :
            The dictionary of component definitions.
        '''
        return self._definitions

    def default(self, _id: Optional[int] = None) -> ReilData:
        '''
        Generate the default component definition.

        Parameters
        ----------
        _id:
            ID of the caller object

        Returns
        -------
        :
            The component with the default definition.
        '''
        raise NotImplementedError

    def __call__(self, name: str, _id: Optional[int] = None) -> ReilData:
        '''
        Generate the component based on the specified `name` for the
        specified caller.

        Parameters
        ----------
        name:
            The name of the component definition.

        _id:
            ID of the caller.

        Returns
        -------
        :
            The component with the specified definition `name`.

        Raises
        ------
        ValueError
            Definition not found.
        '''
        if name not in self._definitions:
            raise ValueError(f'Definition {name} not found.')

        if name == 'default':
            return self.default(_id)

        return ReilData(
            d.fn(_id=_id, **d.args)
            for d in self._definitions[name.lower()])


class SecondayComponent:
    '''
    The datatype to specify secondary components, e.g. `statistic` and
    `reward`.
    '''

    def __init__(self,
                 name: str,
                 primary_component: Optional[PrimaryComponent] = None,
                 ) -> None:
        '''

        Parameters
        ----------
        name:
            The name of the secondary component.

        primary_component:
            An instance of a `PrimaryComponent` from which component
            definitions are used.
        '''
        self._name = name
        self._primary_component = primary_component

        self._definitions: Dict[str, SubComponentInstance] = defaultdict(None)

    def set_primary_component(
            self,
            primary_component: PrimaryComponent) -> None:
        '''Set the primary component.

        Parameters
        ----------
        primary_component:
            An instance of a `PrimaryComponent` from which component
            definitions are used.

        Raises
        ------
        ValueError
            Primary component is already set.
        '''
        if self._primary_component is not None:
            raise ValueError('Primary component is already set. '
                             'Cannot modify it.')

        self._primary_component = primary_component

    def add_definition(self,
                       name: str,
                       fn: ReilFunction,
                       primary_component_name: str = 'default') -> None:
        '''
        Add a new component definition.

        Parameters
        ----------
        name:
            The name of the new component.

        fn:
            The function that will receive the primary component instance and
            computes the value of the secondary component.

        primary_component_name:
            The component name that will be used by `fn`.

        Raises
        ------
        ValueError
            Definition already exists for this name.

        ValueError
            Undefined primary component name.
        '''
        _name = name.lower()
        if _name in self._definitions:
            raise ValueError(f'Definition {name} already exists.')

        if primary_component_name not in self._primary_component.definitions:
            raise ValueError(f'Undefined {primary_component_name}.')

        self._definitions[_name] = SubComponentInstance(
            name=name,
            fn=fn,
            args=primary_component_name)

    def default(self, _id: Optional[int] = None) -> ReilData:
        '''
        Generate the default component definition.

        Parameters
        ----------
        _id:
            ID of the caller object

        Returns
        -------
        :
            The component with the default definition.
        '''
        raise NotImplementedError

    def __call__(self, name: str, _id: Optional[int] = None) -> ReilData:
        '''
        Generate the component based on the specified `name` for the
        specified caller.

        Parameters
        ----------
        name:
            The name of the component definition.

        _id:
            ID of the caller.

        Returns
        -------
        :
            The component with the specified definition `name`.

        Raises
        ------
        ValueError
            Definition not found.
        '''
        _name = name.lower()
        if _name not in self._definitions:
            raise ValueError(f'Definition {name} not found.')

        if _name == 'default':
            return self.default(_id)

        d = self._definitions[_name]

        return ReilData.single_base(name=self._name,
                                    value=d.fn(self._primary_component(
                                        name=cast(str, d.args), _id=_id)))


if __name__ == '__main__':  # noqa: C901
    from reil.stats import Arguments, NormalizedSquareDistance

    def aggregation_function(x):
        v = {
            'name': 't1',
            'value': sum(xi['value'] for xi in x)}
        return v
        # return x

    class test:
        def __init__(self) -> None:
            self._INR = 2.5
            sub_comp_dict = self._extract_sub_components()
            state = PrimaryComponent(sub_comp_dict)
            reward = SecondayComponent(name='reward', primary_component=state)
            state.add_definition('normal_state',
                                 ('age', {}),
                                 ('INR', {'length': 5})
                                 )
            reward.add_definition('normal_reward',
                                  NormalizedSquareDistance(
                                      name='TTR',
                                      arguments=Arguments('INR',),
                                      length=2,
                                      multiplier=-1.0,
                                      retrospective=True,
                                      interpolate=False,
                                      center=2.5,
                                      band_width=0.5,
                                      exclude_first=True),
                                  'normal_state')
            print(state('normal_state', _id=1).value)
            print(reward('normal_reward', _id=1).value)
            self._INR = 1000
            print(state('normal_state', _id=1).value)
            print(reward('normal_reward', _id=1).value)

        def _sub_comp_age(self, _id, **kwargs):
            return {'name': 'age', 'value': 10}

        def _sub_comp_INR(self, _id, length, **kwargs):
            return {'name': 'INR', 'value': [self._INR] * length}

        def _extract_sub_components(self):
            sub_comp_dict = {}
            for k, v in self.__class__.__dict__.items():
                if callable(v) and k[:10] == '_sub_comp_':
                    keywords = list(v.__code__.co_varnames)
                    if 'self' in keywords:
                        keywords.remove('self')
                        f = functools.partial(v, self)
                    else:
                        f = v

                    if 'kwargs' in keywords:
                        keywords.remove('kwargs')

                    if len(keywords) == 0 or keywords[0] != '_id':
                        raise ValueError(
                            f'Error in {k} signature: '
                            'The first argument, except for "self", '
                            'should be "_id".')

                    if '_id' in keywords:
                        keywords.remove('_id')

                    sub_comp_dict[k[10:]] = (f, tuple(keywords))

            return sub_comp_dict

    test()
    print('hi')
