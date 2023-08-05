import os
import pprint
import types
import warnings
from collections import namedtuple

from sqlalchemy.exc import SAWarning

# turn SQLAlchemy warnings into errors
warnings.simplefilter("error", SAWarning)

opj = os.path.join


# ACCEPTABLE_TAG_TYPES = {unicode, str, int, float, bool, type(None), list, tuple}


class Dependency(namedtuple("Dependency", "task param path")):
    def __new__(cls, task, param=None, path=None):
        """
        A way to specify a Task and parameter Dependency as one unit.

        :param task: The Dependent Task
        :param param: The dependent parameter of Task, ex 'out_tsv'
        :param path: The path to a file if it is not a Task parameter.  Cannot be specified if 'param' is specified.
        :return:
        """
        assert bool(param) ^ bool(path), "cannot specify both `param` and `path`".format(**locals())

        from cosmos.api import Task

        assert isinstance(task, Task), "task parameter must be an instance of Task, not %s" % type(task)
        if param:
            assert param in task.params, (
                "Invalid Dependency, param `%s` is not a parameter of `%s`.  "
                "Available parameters are:\n%s" % (param, task, pprint.pformat(task.params, indent=2))
            )
        return super(Dependency, cls).__new__(cls, task, param, path)

    def resolve(self):
        if self.param:
            return self.task.params[self.param]
        else:
            return self.path


def recursive_resolve_dependency(parameter):
    """
    Return a 2-tuple of the recursively resolved datastructure and a set of dependent tasks.
    """
    if isinstance(parameter, Dependency):
        return parameter.resolve(), {parameter.task}
    elif any(isinstance(parameter, t) for t in (bool, float, int, str, type(None))):
        return parameter, set()
    elif isinstance(parameter, list):
        tuple_list = list(recursive_resolve_dependency(v) for v in parameter)
        return (
            list(rds for (rds, _) in tuple_list),
            set.union(*[tasks for _, tasks in tuple_list]) if len(tuple_list) else set(),
        )
    elif isinstance(parameter, tuple):
        tuple_tuple = tuple(recursive_resolve_dependency(v) for v in parameter)
        return (
            tuple(rds for (rds, _) in tuple_tuple),
            set.union(*[tasks for _, tasks in tuple_tuple]) if len(tuple_tuple) else set(),
        )
    elif isinstance(parameter, dict):
        tuple_dict = {k: recursive_resolve_dependency(v) for k, v in list(parameter.items())}
        return (
            {k: rds for k, (rds, _) in list(tuple_dict.items())},
            set.union(*[tasks for _, tasks in tuple_dict.values()]) if len(tuple_dict) else set(),
        )
    else:
        raise ValueError(
            "Cannot handle function parameter of type {}.  "
            "Parameters must be jsonable.  Parameter value is {}".format(type(parameter), parameter)
        )


#########################################################################################################################
# Settings
#########################################################################################################################

library_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(library_path, "VERSION"), "r") as fh:
    __version__ = fh.read().strip()


#########################################################################################################################
# Misc
#########################################################################################################################


class WorkflowFailed(Exception):
    pass


#########################################################################################################################
# Signals
#########################################################################################################################
import blinker

signal_task_status_change = blinker.Signal()
signal_stage_status_change = blinker.Signal()
signal_workflow_status_change = blinker.Signal()

########################################################################################################################
# Enums
########################################################################################################################
import enum


class MyEnum(enum.Enum):
    def __str__(self):
        return "%s" % self._value_


NOOP = None


class TaskStatus(MyEnum):
    no_attempt = "Has not been attempted"
    waiting = "Waiting to execute"  # deprecated
    submitted = "Submitted to the job manager"
    successful = "Finished successfully"
    failed = "Finished, but failed"
    killed = "Manually killed"


class StageStatus(MyEnum):
    no_attempt = ("Has not been attempted",)
    running = ("Running",)
    running_but_failed = "Running, but a task failed"
    successful = "Finished successfully"
    failed = "Finished, but failed"
    killed = "Manually killed"


class WorkflowStatus(MyEnum):
    no_attempt = "No Attempt yet"
    resuming = "Resuming"
    running = "Running"
    successful = "Successfully Finished"
    killed = "Killed"
    failed_but_running = "Running, but a task failed"
    failed = "Failed, but finished"


class RelationshipType(MyEnum):
    one2one = "one2one"
    one2many = "one2many"
    many2one = "many2one"
    many2many = "many2many"
