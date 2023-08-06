Behavior-Driven Development
===========================

About Behavior-Driven Development
---------------------------------

This introduction is inspired by the documentation of `Behave <http://behave.readthedocs.io/en/latest/philosophy.html>`__, a Python
library for Behavior-Driven Development (BDD).
BDD is an agile software development technique that encourages collaboration between developers,
QA and non-technical or business participants in a software project.
It was originally named in 2003 by Dan North as a response to test-driven development (TDD),
including acceptance test or customer test driven development practices as found in extreme programming.

BDD focuses on obtaining a clear understanding of desired software behavior through discussion with stakeholders.
It extends TDD by writing test cases in a natural language that non-programmers can read.
Behavior-driven developers use their native language in combination with the language of
domain-driven design to describe the purpose and benefit of their code.
This allows developers to focus on why the code should be created, rather than the technical details,
and minimizes translation between the technical language in which the code is written and the domain language
spoken by the business, users, stakeholders, project management, etc.


The Gherkin language
--------------------

The Gherkin language is a business readable, domain specific language created to support behavior descriptions in BDD.
It lets you describe software’s behaviour without the need to know its implementation details.
Gherkin allows the user to describe a software feature or part of a feature by means of
representative scenarios of expected outcomes.
Like YAML or Python, Gherkin aims to be a human-readable line-oriented language.

Here is an example of a feature and scenario description with Gherkin,
describing part of the intended behaviour of the Unix ls command:

.. code-block:: gherkin

    Feature: ls
    In order to see the directory structure
    As a UNIX user
    I need to be able to list the current directory's contents

    Scenario: List 2 files in a directory
        Given I am in a directory "test"
        And I have a file named "foo"
        And I have a file named "bar"
        When I run "ls"
        Then I should get:
            """
            bar
            foo
            """

As can be seen above, Gherkin files should be written using natural language - ideally
by the non-technical business participants in the software project.
Such feature files serve two purposes: documentation and automated tests.
Using one of the available Gherkin parsers, it is possible to execute the described scenarios and check the expected outcomes.

.. seealso:: A quite complete overview of the Gherkin language is available `here <http://docs.behat.org/en/v2.5/guides/1.gherkin.html>`__.


Sismic support for BDD
----------------------

Since statecharts are executable pieces of software, it is desirable for statechart users to be able to describe
the intended behavior in terms of feature and scenario descriptions.
While it is possible to manually integrate the BDD process with any library or software, Sismic is bundled with a
command-line utility ``sismic-bdd`` (or ``python -m sismic.bdd``) that automates the integration of BDD.

Sismic support for BDD relies on `Behave <http://behave.readthedocs.io/en/latest/>`__, a Python library for BDD
with full support of the Gherkin language.

As an illustrative example, let us define the desired behavior of our elevator statechart.
We first create a feature file that contains several scenarios of interest.
By convention, this file has the extension *.feature*, but this is not mandatory.
The example illustrates that Sismic provides a set of predefined steps (e.g., `given`, `when`, `then`) to describe
common statechart behavior without having to write a single line of Python code.

.. literalinclude:: examples/elevator/elevator.feature
    :language: gherkin

Let us save this file as *elevator.feature* in the same directory as the statechart description, *elevator.yaml*.
We can then instruct ``sismic-bdd`` to run on this statechart the scenarios described in the feature file:

.. code-block:: none

    sismic-bdd elevator.yaml --features elevator.feature

Under the hood, ``sismic-bdd`` will create a temporary directory where all the files required to execute
Behave are put. It also makes available a list of predefined *given*, *when*, and *then* steps and sets up many
hooks that are required to integrate Sismic and Behave.

.. note:: Module ``sismic.bdd`` exposes a :py:func:`~sismic.bdd.execute_bdd` function that is internally
    used by ``sismic-bdd`` CLI, and that can be used if programmatic access to these features is required.


When ``sismic-bdd`` is executed, it will somehow translate the feature file into executable code, compute the outcomes
of the scenarios, check whether they match what is expected, and display as summary of all executed scenarios and
encountered errors:

.. code-block:: none

    [...]

    1 feature passed, 0 failed, 0 skipped
    10 scenarios passed, 0 failed, 0 skipped
    22 steps passed, 0 failed, 0 skipped, 0 undefined
    Took 0m0.027s

The ``sismic-bdd`` command-line interface accepts several other parameters:

.. code-block:: none

    usage: sismic-bdd [-h] --features features [features ...]
                      [--steps steps [steps ...]]
                      [--properties properties [properties ...]] [--show-steps]
                      [--debug-on-error]
                      statechart

    Command-line utility to execute Gherkin feature files using Behave. Extra parameters will be passed to Behave.

    positional arguments:
      statechart            A YAML file describing a statechart

    optional arguments:
      -h, --help            show this help message and exit
      --features features [features ...]
                            A list of files containing features
      --steps steps [steps ...]
                            A list of files containing steps implementation
      --properties properties [properties ...]
                            A list of filepaths pointing to YAML property
                            statecharts. They will be checked at runtime following
                            a fail fast approach.
      --show-steps          Display a list of available steps (equivalent to
                            Behave's --steps parameter
      --debug-on-error      Drop in a debugger in case of step failure (ipdb if
                            available)

Additionally, any extra parameter provided to ``sismic-bdd`` will be passed to Behave.
See `command-line parameters of Behave <http://behave.readthedocs.io/en/latest/behave.html#command-line-arguments>`__
for more information.



Predefined steps
----------------

In order to be able to execute scenarios, a Python developer needs to write code defining the mapping from the actions
and assertions expressed as natural language sentences in the scenarios (using specific
keywords such as *given*, *when* or *then*) to Python code that manipulates the statechart.
To facilitate the implementation of this mapping, Sismic provides a set of predefined
statechart-specific steps.

By convention, steps starting with *given* or *when* correspond to actions that must be applied on the statechart,
while steps starting with *then* correspond to assertions about the execution or the current state of the statechart.
More precisely, (1) all *given* or *when* steps implicitly call the :py:meth:`~sismic.interpreter.Interpreter.execute`
method of the underlying interpreter, (2) all *when* steps capture the output of these calls, and (3) we developed all
predefined *then* steps to assert things based on the captured output (implying that only the steps that start
with *when* will be monitored in practice).


"Given" and "when" steps
~~~~~~~~~~~~~~~~~~~~~~~~


Given/when I send event {name}

    This step queues an event with provided name.


Given/when I send event {name} with {parameter}={value}

    This step queues an event with provided name and parameter.
    More than one parameter can be specified when using Gherkin tables, as follows:

    .. literalinclude:: examples/elevator/elevator.feature
        :language: gherkin
        :lines: 11-16
        :emphasize-lines: 3-5


Given/when I wait {seconds:g} seconds

Given/when I wait {seconds:g} second

    These steps increase the internal clock of the interpreter.


Given/when I do nothing

    This step does nothing. It's main usage is when assertions using *then* steps are written as first steps
    of a scenario. As they require a *when* step to be present, use "when I do nothing".


Given/when I reproduce "{scenario}"

    This step reproduces all the *given* and *when* steps that are contained in provided scenario.
    When this step is prefixed with *given* (resp. *when*), the steps of the provided scenario will be
    reproduced using *given* (resp. *when*).

    .. literalinclude:: examples/elevator/elevator.feature
        :language: gherkin
        :lines: 7-10, 18-23
        :emphasize-lines: 6


Given/when I repeat "{step}" {repeat:d} times

    This step repeats given step several times.
    The text of the step must be provided without its keyword, and will be executed using the
    current keyword (*given* or *when*).


"Then" steps
~~~~~~~~~~~~

Then state {name} is entered

Then state {name} is not entered

Then state {name} is exited

Then state {name} is not exited

    These steps assert that a state with provided name was respectively entered, not entered, exited,
    not exited.


Then state {name} is active

Then state {name} is not active

    These steps assert that a state with provided name is (not) in the active configuration of the statechart.


Then event {name} is fired

Then event {name} is fired with {parameter}={value}

    These steps assert that an event with provided name was sent.
    Additional parameters can be provided using Gherkin tables.


Then event {name} is not fired

    This step asserts that no event with provided name was sent.


Then no event is fired

    This step asserts that no event was fired.


Then variable {variable} equals {value}

    This step asserts that the context of the statechart has a variable with a given name and a given value.


Then variable {variable} does not equal {value}

    This step asserts that the context of a statechart has a variable with a given name, but a value different
    than the one that is provided.


Then expression "{expression}" holds

Then expression "{expression}" does not hold

    These steps assert that given expression holds (does not hold). The expression will be evaluated by the
    underlying code evaluator (a :py:class:`~sismic.code.PythonEvaluator` by default) using the current
    context.


Then statechart is in a final configuration

Then statechart is not in a final configuration

    These steps assert that the statechart is (not) in a final configuration.


Implementing new steps
----------------------

While the steps that are already predefined should be sufficient to manipulate the statechart, it is more intuitive
to use domain-specific steps to write scenarios.
For example, if the statechart being tested encodes the behavior of a microwave oven, the domain-specific step
"Given I open the door" corresponds to the action of sending an event ``door_opened`` to the statechart, and is
more intuitive to use when writing scenarios.

Consider the following scenarios expressed using a domain-specific language:

.. literalinclude:: examples/microwave/cooking_human.feature
    :language: gherkin


The mapping from domain-specific step "Given I open the door" to the action of sending a door opened event to the
statechart could be defined using plain Python code, by defining a new step following
`Python Step Implementations <http://behave.readthedocs.io/en/latest/tutorial.html#python-step-implementations>`__
of Behave.

.. code:: python

    from behave import given, when

    @given('I open the door')
    @when('I open the door')
    def opening_door(context):
        context.interpreter.queue('door_opened')

For convenience, the ``context`` parameter automatically provided by Behave at runtime exposes three Sismic-specific
attributes, namely ``interpreter``, ``trace`` and ``monitored_trace``.
The first one corresponds to the interpreter being executed, the second one is a list of all executed macro steps,
and the third one is list of executed macro steps restricted to the ones that were performed during the
execution of the previous block of *when* steps.


However, this domain-specific step can also be implemented more easily as an alias of predefined step "Given I send
event door_opened". As we believe that most of the domain-specific steps are just aliases or combinations of
predefined steps, Sismic provides two convenient helpers to map new steps to predefined ones:

.. automodule:: sismic.bdd
    :members: map_action, map_assertion
    :noindex:

Using these helpers, one can easily implement the domain-specific steps of our example:

.. literalinclude:: examples/microwave/steps.py
    :language: python


Assuming that the features are defined in ``cooking.feature``, these steps in ``steps.py``, and the microwave in
``microwave.yaml``, then ``sismic-bdd`` can be used as follows:

.. code-block:: none

    $ sismic-bdd microwave.yaml --steps steps.py --features cooking.feature

    Feature: Cooking # cooking.feature:1

    [...]

    1 feature passed, 0 failed, 0 skipped
    3 scenarios passed, 0 failed, 0 skipped
    17 steps passed, 0 failed, 0 skipped, 0 undefined
    Took 0m0.040s

