"""Base FSM declarations."""

from __future__ import annotations

import inspect
from typing import Callable, List, Type
from viewflow.this_object import ThisObject
from viewflow.utils import MARKER
from .typing import Condition, StateTransitions


class TransitionNotAllowed(Exception):
    """Raised when a transition is not allowed."""


class Transition(object):
    """State transition definition."""

    def __init__(self, func, source, target, label=None, conditions=None, permission=None):  # noqa D102
        self.func = func
        self.source = source
        self.target = target
        self._label = label
        self.permission = permission
        self.conditions: List[Condition] = conditions if conditions else []

    def __str__(self):
        return f'{self.label} Transition'

    @property
    def label(self):
        """Transition human-readable label."""
        if self._label:
            return self._label
        else:
            try:
                return self.func.label
            except AttributeError:
                return self.func.__name__.title()

    @property
    def slug(self):
        return self.func.__name__

    def conditions_met(self, instance) -> bool:
        """Check that all associated conditions is True."""
        conditions = [
            condition.resolve(instance.__class__) if isinstance(condition, ThisObject) else condition
            for condition in self.conditions
        ]
        return all(map(lambda condition: condition(instance), conditions))

    def has_perm(self, instance, user) -> bool:
        """Check the permission of the transition."""
        if self.permission is None:
            return True
        elif callable(self.permission):
            return self.permission(instance, user)
        elif isinstance(self.permission, ThisObject):
            permission = self.permission.resolve(instance)
            return permission(user)
        else:
            raise ValueError(f"Unknown permission type {type(self.permission)}")


class TransitionMethod(object):
    """Unbound transition method wrapper.

    Provides shortcut to enumerate all method transitions, ex::

        Review.publish.get_transitions()
    """

    do_not_call_in_templates = True

    def __init__(self, state: State, func: Callable, descriptor: TransitionDescriptor, owner: Type):
        self._state = state
        self._func = func
        self._descriptor = descriptor
        self._owner = owner

        self.__doc__ = func.__doc__

    def get_transitions(self) -> List[Transition]:
        return self._descriptor.get_transitions()

    @property
    def slug(self):
        """Transition name."""
        return self.func.__name__


class TransitionBoundMethod(object):
    """Instance method wrapper that performs the transition."""

    do_not_call_in_templates = True

    class Wrapper(object):
        """Wrapper context object, to simplify __call__ method debug"""
        def __init__(self, parent: 'TransitionBoundMethod', kwargs):
            self.parent = parent
            self.caller_kwargs = kwargs
            self.initial_state = None
            self.target_state = None

        def __enter__(self):
            self.initial_state = self.parent._state.get(self.parent._instance)
            transition = self.parent._descriptor.get_transition(self.initial_state)

            if transition is None:
                raise TransitionNotAllowed(f'{self.parent.label} :: no transition from "{self.initial_state}"')

            if not transition.conditions_met(self.parent._instance):
                raise TransitionNotAllowed(
                    f" '{transition.label}' transition conditions have not been met"
                )

            self.target_state = transition.target
            if self.target_state:
                self.parent._state.set(self.parent._instance, self.target_state)

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is not None:
                self.parent._state.set(self.parent._instance, self.initial_state)
            else:
                self.parent._state.transition_succeed(
                    self.parent._instance, self.parent,
                    self.initial_state, self.target_state,
                    **self.caller_kwargs
                )

    def __init__(self, state, func, descriptor, instance):
        self._state: State = state
        self._func: Callable = func
        self._descriptor: TransitionDescriptor = descriptor
        self._instance = instance

    def original(self, *args, **kwargs):
        """Call the unwrapped class method."""
        return self._func(self._instance, *args, **kwargs)

    def can_proceed(self, check_conditions=True):
        """Check is transition available."""
        current_state = self._state.get(self._instance)
        transition = self._descriptor.get_transition(current_state)
        if transition and check_conditions:
            return transition.conditions_met(self._instance)
        return False

    def has_perm(self, user):
        current_state = self._state.get(self._instance)
        transition = self._descriptor.get_transition(current_state)
        if transition:
            return transition.has_perm(self._instance, user)
        return False

    @property
    def label(self):
        """Transition human-readable label."""
        current_state = self._state.get(self._instance)
        transition = self._descriptor.get_transition(current_state)
        if transition:
            return transition.label
        else:
            try:
                return self._func.label
            except AttributeError:
                return self._func.__name__.title()

    def __call__(self, *args, **kwargs):
        with TransitionBoundMethod.Wrapper(self, kwargs=kwargs):
            return self._func(self._instance, *args, **kwargs)

    def get_transitions(self):
        return self._descriptor.get_transitions()


class TransitionDescriptor(object):
    """Base transition definition descriptor."""

    do_not_call_in_templates = True

    def __init__(self, state, func):  # noqa D102
        self._state = state
        self._func = func
        self._transitions = {}

    def __get__(self, instance, owner=None):
        if instance:
            return TransitionBoundMethod(self._state, self._func, self, instance)
        else:
            return TransitionMethod(self._state, self._func, self, owner)

    def add_transition(self, transition):
        self._transitions[transition.source] = transition

    def get_transitions(self) -> List[Transition]:
        """List of all transitions."""
        return self._transitions.values()

    def get_transition(self, source_state):
        """Get a transition of a source_state.

        Returns None if there is no outgoing transitions.
        """
        transition = self._transitions.get(source_state, None)
        if transition is None:
            transition = self._transitions.get(State.ANY, None)
        return transition


class SuperTransitionDescriptor(object):
    do_not_call_in_templates = True

    def __init__(self, state, func):  # noqa D102
        self._state = state
        self._func = func

    def __get__(self, instance, owner=None):
        if instance:
            return TransitionBoundMethod(self._state, self._func, self.get_descriptor(instance.__class__), instance)
        else:
            return TransitionMethod(self._state, self._func, self.get_descriptor(owner), owner)

    def get_descriptor(self, owner) -> TransitionDescriptor:
        """Lookup for the transition descriptor in the base classes."""
        for cls in owner.__mro__[1:]:
            if hasattr(cls, self._func.__name__):
                super_method = getattr(cls, self._func.__name__)
                if isinstance(super_method, TransitionMethod):
                    break
        else:
            raise ValueError('Base transition not found')

        return super_method._descriptor


class StateDescriptor(object):
    """Class-bound value for a state descriptor.

    Provides shortcut to enumerate all class transitions, ex::

        Review.state.get_transitions()
    """

    def __init__(self, state: 'State', owner: type):
        self._state = state
        self._owner = owner

    def __getattr__(self, attr):
        return getattr(self._state, attr)

    def get_transitions(self) -> StateTransitions:
        propname = '__fsm_{}_transitions'.format(self._state.propname)
        transitions = self._owner.__dict__.get(propname, None)
        if transitions is None:
            transitions = {}

            methods = inspect.getmembers(
                self._owner,
                lambda attr: isinstance(attr, TransitionMethod)
            )
            transitions = {
                method: method.get_transitions()
                for _, method in methods
            }
            setattr(self._owner, propname, transitions)

        return transitions

    def get_outgoing_transitions(self, state) -> List[Transition]:
        return [
            transition
            for transitions in self.get_transitions().values()
            for transition in transitions
            if transition.source == state or (transition.source == State.ANY and transition.target != state)
        ]


class State(object):
    """State slot field."""

    ANY = MARKER('ANY')

    def __init__(self, states, default=None):
        self._default = default
        self._setter = None
        self._getter = None
        self._on_success = None

    def __get__(self, instance, owner=None):
        if instance:
            return self.get(instance)
        return StateDescriptor(self, owner)

    def __set__(self, instance, value):
        raise AttributeError('Direct state modification is not allowed')

    def get(self, instance):
        """Get the state from the underline class instance."""
        if self._getter:
            value = self._getter(instance)
            if self._default:
                return value if value else self._default
            else:
                return value
        return getattr(instance, self.propname, self._default)

    def set(self, instance, value):
        """Get the state of the underline class instance."""
        if self._setter:
            self._setter(instance, value)
        else:
            setattr(instance, self.propname, value)

    def transition_succeed(self, instance, descriptor, source, target, **kwargs):
        if self._on_success:
            self._on_success(instance, descriptor, source, target, **kwargs)

    @property
    def propname(self):
        """State storage attribute."""
        return '__fsm{}'.format(id(self))

    def transition(
        self, source=None, target=None, label=None,
        conditions=None, permission=None,
    ):
        """Transition method decorator."""
        def _wrapper(func):
            if isinstance(func, TransitionDescriptor):
                descriptor = func
            else:
                descriptor = TransitionDescriptor(self, func)

            source_list = source
            if not isinstance(source, (list, tuple, set)):
                source_list = [source]

            for src in source_list:
                transition = Transition(
                    func=descriptor._func,
                    source=src,
                    target=target,
                    label=label,
                    conditions=conditions,
                    permission=permission
                )
                descriptor.add_transition(transition)

            return descriptor
        return _wrapper

    def super(self):
        def _wrapper(func):
            return SuperTransitionDescriptor(self, func)
        return _wrapper

    def setter(self):
        def _wrapper(func):
            self._setter = func
            return func
        return _wrapper

    def getter(self):
        def _wrapper(func):
            self._getter = func
            return func
        return _wrapper

    def on_success(self):
        def _wrapper(func):
            self._on_success = func
            return func
        return _wrapper

    class CONDITION(object):
        """Boolean-like object to return value accompanied with a messsage from fsm conditions."""

        def __init__(self, is_true: bool, unmet: str = ""):
            self.is_true = is_true
            self.unmet = unmet

        @property
        def message(self):
            return self.message if self.unmet else ''

        def __bool__(self):
            return self.is_true
