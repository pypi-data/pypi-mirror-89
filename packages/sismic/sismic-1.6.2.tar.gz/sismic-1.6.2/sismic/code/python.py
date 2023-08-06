import collections
import copy

from types import CodeType
from typing import Any, Dict, List, Optional, Mapping, Iterator

from . import Evaluator
from ..exceptions import CodeEvaluationError
from ..model import Event, InternalEvent, MetaEvent, Transition


__all__ = ['PythonEvaluator']


class FrozenContext(collections.abc.Mapping):
    """
    A shallow copy of a context. The keys of the underlying context are
    exposed as attributes.
    """
    __slots__ = ['__frozencontext']

    def __init__(self, context: Dict) -> None:
        self.__frozencontext = {k: copy.copy(v) for k, v in context.items()}

    def __getattr__(self, item):
        try:
            return self.__frozencontext[item]
        except KeyError:
            raise AttributeError('{} has no attribute {}'.format(self, item))

    def __getstate__(self):
        return self.__frozencontext

    def __setstate__(self, state):
        self.__frozencontext = state

    def __getitem__(self, key):
        return self.__frozencontext[key]

    def __len__(self):
        return len(self.__frozencontext)

    def __iter__(self):
        return iter(self.__frozencontext)


class PythonEvaluator(Evaluator):
    """
    A code evaluator that understands Python.

    This evaluator exposes some additional functions/variables:
    
    - On both code execution and code evaluation:
        - A *time: float* value that represents the current time exposed by interpreter clock.
        - An *active(name: str) -> bool* Boolean function that takes a state name and return *True* if and only
          if this state is currently active, ie. it is in the active configuration of the ``Interpreter`` instance
          that makes use of this evaluator.
    - On code execution:
        - A *send(name: str, **kwargs) -> None* function that takes an event name and additional keyword parameters and
          raises an internal event with it. Raised events are propagated to bound statecharts as external events and
          to the current statechart as internal event. If delay is provided, a delayed event is created.
        - A *notify(name: str, **kwargs) -> None* function that takes an event name and additional keyword parameters and
          raises a meta-event with it. Meta-events are only sent to bound property statecharts.
        - If the code is related to a transition, the *event: Event* that fires the transition is exposed.
        - A *setdefault(name:str, value: Any) -> Any* function that defines and returns variable *name* in
          the global scope if it is not yet defined.
    - On guard or contract evaluation:
        - If the code is related to a transition, an *event: Optional[Event]* variable is exposed. This variable
          contains the currently considered event, or None.
    - On guard or contract (except preconditions) evaluation:
        - An *after(sec: float) -> bool* Boolean function that returns *True* if and only if the source state
          was entered more than *sec* seconds ago. The time is evaluated according to Interpreter's clock.
        - A *idle(sec: float) -> bool* Boolean function that returns *True* if and only if the source state
          did not fire a transition for more than *sec* ago. The time is evaluated according to Interpreter's clock.
    - On contract (except preconditions) evaluation:
        - A variable *__old__* that has an attribute *x* for every *x* in the context when either the state
          was entered (if the condition involves a state) or the transition was processed (if the condition
          involves a transition). The value of *__old__.x* is a shallow copy of *x* at that time.
    - On contract evaluation:
        - A *sent(name: str) -> bool* function that takes an event name and return True if an event with the same name
          was sent during the current step.
        - A *received(name: str) -> bool* function  that takes an event name and return True if an event with the
          same name is currently processed in this step.

    If an exception occurred while executing or evaluating a piece of code, it is propagated by the
    evaluator.

    :param interpreter: the interpreter that will use this evaluator,
        is expected to be an *Interpreter* instance
    :param initial_context: a dictionary that will be used as *__locals__*
    """
    def __init__(self, interpreter=None, *, initial_context: Mapping[str, Any]=None) -> None:
        super().__init__(interpreter, initial_context=initial_context)

        self._context = {}  # type: Dict[str, Any]
        self._context.update(initial_context if initial_context else {})
        self._interpreter = interpreter

        # Precompiled code
        self._evaluable_code = {}  # type: Dict[str, CodeType]
        self._executable_code = {}  # type: Dict[str, CodeType]

        # Frozen context for __old__
        self._memory = {}  # type: Dict[int, FrozenContext]

    @property
    def context(self) -> Mapping:
        return self._context

    def _setdefault(self, name: str, value: Any) -> Any:
        """
        Define and return variable "name".

        :param name: name of the variable
        :param value: value to use for that variable, if not defined
        :return: value of the variable
        """
        return self._context.setdefault(name, value)

    def _evaluate_code(self, code: Optional[str], *, additional_context: Mapping[str, Any]=None) -> bool:
        """
        Evaluate given code using Python.

        :param code: code to evaluate
        :param additional_context: an optional additional context
        :return: truth value of *code*
        """
        if code is None:
            return True

        compiled_code = self._evaluable_code.get(code, None)
        if compiled_code is None:
            compiled_code = self._evaluable_code.setdefault(code, compile(code, '<string>', 'eval'))

        exposed_context = {
            'active': lambda s: s in self._interpreter.configuration,
            'time': self._interpreter.time,
        }
        exposed_context.update(additional_context if additional_context is not None else {})

        try:
            return bool(eval(compiled_code, exposed_context, self._context))
        except Exception as e:
            raise CodeEvaluationError('"{}" occurred while evaluating "{}"'.format(e, code)) from e


    def _execute_code(self, code: Optional[str], *, additional_context: Mapping[str, Any]=None) -> List[Event]:
        """
        Execute given code using Python.

        :param code: code to execute
        :param additional_context: an optional additional context
        :return: a list of sent events
        """
        if code is None:
            return []

        compiled_code = self._executable_code.get(code, None)
        if compiled_code is None:
            compiled_code = self._executable_code.setdefault(code, compile(code, '<string>', 'exec'))

        sent_events = []  # type: List[Event]

        exposed_context = {
            'active': lambda name: name in self._interpreter.configuration,
            'time': self._interpreter.time,
            'send': lambda name, **kwargs: sent_events.append(InternalEvent(name, **kwargs)),
            'notify': lambda name, **kwargs: sent_events.append(MetaEvent(name, **kwargs)),
            'setdefault': self._setdefault,
        }
        exposed_context.update(additional_context if additional_context is not None else {})

        try:
            exec(compiled_code, exposed_context, self._context)  # type: ignore
            return sent_events
        except Exception as e:
            raise CodeEvaluationError('"{}" occurred while executing "{}"'.format(e, code)) from e

    def evaluate_guard(self, transition: Transition, event: Optional[Event]=None) -> bool:
        """
        Evaluate the guard for given transition.

        :param transition: the considered transition
        :param event: instance of *Event* if any
        :return: truth value of *code*
        """
        additional_context = {
            'after': lambda seconds: self._interpreter.time - seconds >= self._interpreter._entry_time[transition.source],
            'idle': lambda seconds: self._interpreter.time - seconds >= self._interpreter._idle_time[transition.source],
            'event': event,
        }
        return self._evaluate_code(getattr(transition, 'guard', None), additional_context=additional_context)

    def evaluate_preconditions(self, obj, event: Optional[Event]=None) -> Iterator[str]:
        """
        Evaluate the preconditions for given object (either a *StateMixin* or a
        *Transition*) and return a list of conditions that are not satisfied.

        :param obj: the considered state or transition
        :param event: an optional *Event* instance, if any
        :return: list of unsatisfied conditions
        """
        additional_context = {
            'received': lambda name: name == getattr(event, 'name', None),
            'sent': lambda name: name in [e.name for e in self._interpreter._sent_events],
            'event': event,
        }

        # Deal with __old__ in contracts, only required if there is an invariant or a postcondition
        if len(getattr(obj, 'invariants', [])) > 0 or len(getattr(obj, 'postconditions', [])) > 0:
            self._memory[id(obj)] = FrozenContext(self._context)

        return filter(
            lambda c: not self._evaluate_code(c, additional_context=additional_context),
            getattr(obj, 'preconditions', [])
        )

    def evaluate_invariants(self, obj, event: Optional[Event]=None) -> Iterator[str]:
        """
        Evaluate the invariants for given object (either a *StateMixin* or a
        *Transition*) and return a list of conditions that are not satisfied.

        :param obj: the considered state or transition
        :param event: an optional *Event* instance, if any
        :return: list of unsatisfied conditions
        """
        state_name = obj.source if isinstance(obj, Transition) else obj.name

        additional_context = {
            '__old__': self._memory.get(id(obj), None),
            'after': lambda seconds: self._interpreter.time - seconds >= self._interpreter._entry_time[state_name],
            'idle': lambda seconds: self._interpreter.time - seconds >= self._interpreter._idle_time[state_name],
            'received': lambda name: name == getattr(event, 'name', None),
            'sent': lambda name: name in [e.name for e in self._interpreter._sent_events],
            'event': event,
        }

        return filter(
            lambda c: not self._evaluate_code(c, additional_context=additional_context),
            getattr(obj, 'invariants', [])
        )

    def evaluate_postconditions(self, obj, event: Optional[Event]=None) -> Iterator[str]:
        """
        Evaluate the postconditions for given object (either a *StateMixin* or a
        *Transition*) and return a list of conditions that are not satisfied.

        :param obj: the considered state or transition
        :param event: an optional *Event* instance, if any
        :return: list of unsatisfied conditions
        """
        state_name = obj.source if isinstance(obj, Transition) else obj.name

        additional_context = {
            '__old__': self._memory.get(id(obj), None),
            'after': lambda seconds: self._interpreter.time - seconds >= self._interpreter._entry_time[state_name],
            'idle': lambda seconds: self._interpreter.time - seconds >= self._interpreter._idle_time[state_name],
            'received': lambda name: name == getattr(event, 'name', None),
            'sent': lambda name: name in [e.name for e in self._interpreter._sent_events],
            'event': event,
        }

        return filter(
            lambda c: not self._evaluate_code(c, additional_context=additional_context),
            getattr(obj, 'postconditions', [])
        )

    def __getstate__(self):
        attributes = self.__dict__.copy()
        attributes['_executable_code'] = dict()  # Code fragment cannot be pickled
        attributes['_evaluable_code'] = dict()  # Code fragment cannot be pickled
        return attributes
