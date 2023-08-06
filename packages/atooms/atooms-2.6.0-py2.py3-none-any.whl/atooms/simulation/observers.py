# This file is part of atooms
# Copyright 2010-2017, Daniele Coslovich

"""
Scheduler and callbacks (aka observers) to be called during a simulation.

To add a callback `func` to a `Simulation` instance `sim` and have it
called every 100 steps

    #!python
    sim.add(func, Scheduler(100))

There are two ways to set them up and add them to a simulation:

1. callable classes

   Example of client code:
     sim.add(simulation.WriterThermo(), 100)
     sim.add(simulation.TargetRMSD(5.0))

2. use functions passing optional *args and **kwargs.

   Example of client code:
     sim.add(simulation.writer_thermo, 100)
     sim.add(simulation.target_rmsd, 100, rmsd=5.0)

To differentiate different types of callbacks, we following a naming
convention (for classes and function). If they contain

- target : these callbacks raise a SimulationEnd when it's over
- writer : these callbacks dump useful stuff to file

Of course, general purpose callback can be passed to do whatever.
"""

import sys
import os
import shutil
import time
import datetime
import logging
from atooms.core.utils import rmd, rmf

__all__ = ['SimulationEnd', 'WallTimeLimit', 'SimulationKill',
           'Scheduler', 'write_config', 'write_thermo', 'write',
           'target', 'target_rmsd', 'target_steps', 'target_walltime',
           'user_stop', 'target_user_stop', 'Speedometer',
           'shell_stop', 'target_shell_stop', 'target_python_stop']

_log = logging.getLogger(__name__)


# Helper functions

def _sec2time(time_interval):
    """
    Convert a time interval in seconds to (day, hours, minutes,
    seconds) format.
    """
    eta_d = time_interval / (24.0 * 3600)
    eta_h = (eta_d - int(eta_d)) * 24
    eta_m = (eta_h - int(eta_h)) * 60.0
    eta_s = (eta_m - int(eta_m)) * 60.0
    return '%dd:%02dh:%02dm:%02ds' % (eta_d, eta_h, eta_m, eta_s)


# Default exceptions

class SimulationEnd(Exception):
    """Raised when an targeter reaches its target."""
    pass

class SimulationKill(Exception):
    """Raised when a simulation is terminated by SIGTERM."""
    pass

class WallTimeLimit(Exception):
    """Raised when the wall time limit is reached."""
    pass


# Scheduler classes

class Scheduler(object):

    """
    Schedule observer calls during the simulation.

    This is nothing but a callable that takes a simulation instance
    and returns the next step at which an observer has to to notified.
    """

    def __init__(self, interval=None, calls=None, steps=None,
                 block=None, seconds=None):
        """
        Only one of the arguments can be different from None.

        - `interval`: notify at a fixed steps interval
        - `calls`: fixed number of notification
        - `steps`: list of steps at which the observer will be notified
        - `block`: as steps, but will be called periodically
        - `seconds`: notify every `seconds`
        """
        self.interval = interval
        self.calls = calls
        self.steps = steps
        self.block = block
        self.seconds = seconds

        # Normalize non-positive intervals and n. of calls
        if self.interval is not None and self.interval <= 0:
            self.interval = None
        if self.calls is not None and self.calls <= 0:
            self.calls = None

    def __call__(self, sim):
        """
        Given a simulation instance `sim`, return the next step at which
        the observer will be called.
        """
        if self.interval is not None and self.calls is None:
            # Regular interval
            return (sim.current_step // self.interval + 1) * self.interval

        elif self.calls is not None:
            # Fixed number of calls
            interval = max(1, sim.steps // self.calls)
            return (sim.current_step // interval + 1) * interval

        elif self.steps is not None:
            # List of selected steps
            inext = sys.maxsize
            for i, step in enumerate(self.steps):
                if step > sim.current_step:
                    inext = self.steps[i]
                    break
            return inext

        elif self.block is not None:
            # Periodic block of steps
            step_of_last_block = (sim.current_step // self.block[-1]) * self.block[-1]
            inext = sys.maxsize
            for i, step in enumerate(self.block):
                if step > sim.current_step % self.block[-1]:
                    inext = self.block[i] + step_of_last_block
                    break
            return inext

        elif self.seconds is not None:
            pass
        else:
            return sys.maxsize


# Writer callbacks
# Callbacks as pure function to distinguish their role we adopt a naming convention:
# if the callback contains write (target) in its __name__ then it is a writer (targeter).

def write_to_ram(sim, trajectory_ram):
    """
    Write configurations to a trajectory in ram.
    """
    trajectory_ram.write(sim.system, sim.current_step)


def write_config(sim, fields=None, precision=None):
    """
    Write configurations to a trajectory file.

    The trajectory format is taken from the passed Simulation
    instance.
    """
    # Initialize
    # This will clear the variable in a new run
    if sim.current_step == 0 or not hasattr(sim, '__init_write_config'):
        sim.__init_write_config = False
    if sim.restart:
        sim.__init_write_config = True

    # Header
    if not sim.__init_write_config:
        sim.__init_write_config = True
        # TODO: folder-based trajectories should ensure that mode='w' clears up the folder
        rmd(sim.output_path)
        rmf(sim.output_path)

    with sim.trajectory_class(sim.output_path, 'a') as t:
        if precision is not None:
            t.precision = precision
        if fields is not None:
            t.fields = fields
        t.write(sim.system, sim.current_step)


def write_thermo(sim, fields=None, fmt=None, precision=6, functions=None):
    """
    Write thermodynamic properties to a file.

    By default, available fields are:
    - steps
    - temperature
    - potential energy per particle
    - kinetic energy per particle
    - total energy
    - pressure
    - rmsd
    
    The set of available `fields` can be augmented by passing an extra
    `functions` dictionary.

    The `fmt` dictionary can be used to provide custom formatting
    options for fields.

    The `precision` parameter controls the default precision of
    floating point fields.
    """

    # By default write minimal info
    if fields is None:
        fields = ['steps',
                  'temperature',
                  'potential energy per particle',
                  'kinetic energy per particle',
                  'total energy per particle',
                  'rmsd']

    # Internal function database.
    # It can be augmented via functions parameter
    _db_func = {
        'steps': lambda x: x.current_step,
        'potential energy per particle': lambda x: x.system.potential_energy(True),
        'kinetic energy per particle': lambda x: x.system.kinetic_energy(True),
        'total energy per particle': lambda x: x.system.total_energy(True, cache=True),
        'temperature': lambda x: x.system.temperature,
        'density': lambda x: x.system.density,
        'pressure': lambda x: x.system.pressure,
        'rmsd': lambda x: x.rmsd,
    }

    # Update db with extra functions
    if functions is not None:
        _db_func.update(functions)

    # Internal database for formats
    _db_fmt = {}
    for key in _db_func:
        # Default to float formatting
        _db_fmt[key] = '{{:.{precision}{form}}}'.format(precision=precision, form='g')
    # Steps are integer
    _db_fmt['steps'] = '{:d}'

    # Update db with extra formats
    if fmt is not None:
        _db_fmt.update(fmt)

    # TODO: make it possible to have multiple write_thermo callbacks. At present they interfere
    # Initialize
    # This will clear the variable in a new run
    if sim.current_step == 0 or not hasattr(sim, '__init_write_thermo'):
        sim.__init_write_thermo = False
    if sim.restart:
        sim.__init_write_thermo = True

    # Header
    if not sim.__init_write_thermo:
        sim.__init_write_thermo = True
        with open(sim.output_path + '.thermo', 'w') as fh:
            txt = ', '.join(fields)
            fh.write('# columns: {}\n'.format(txt))

    # Line
    with open(sim.output_path + '.thermo', 'a') as fh:
        values = [_db_func[field](sim) for field in fields]
        result = ' '.join([_db_fmt[field].format(value) for value, field in zip(values, fields)])
        fh.write('{}\n'.format(result))


def write(sim, name, attributes):
    """
    Write generic attributes of simulation and system to a file.

    `name` is a tag appended to `sim.base_path` to define the output
    file path.

    `attributes` must be a list of valid properties of the Simulation
    instance `sim` or of its System instance `sim.system`.
    """
    f = sim.output_path + '.' + name
    if sim.current_step == 0:
        with open(f, 'w') as fh:
            fh.write('# columns: %s\n' % ', '.join(attributes))
    else:
        # Extract the requested attributes
        values = []
        for attr in attributes:
            level = len(attr.split('.'))
            if level == 1:
                values.append(getattr(sim, attr))
            elif level == 2:
                system_attr = attr.split('.')[-1]
                if attr.startswith('system'):
                    values.append(getattr(sim.system, system_attr))
            else:
                raise ValueError('attribute is too deep')
        # Format output string
        fmt = ('%s ' * len(attributes)) + '\n'
        with open(f, 'a') as fh:
            fh.write(fmt % tuple(values))


# Target callbacks.
# They should return a fractional measure of completion

def target(sim, attribute, value):
    """
    An observer that raises a `SimulationEnd` exception when a given
    target `value` of a property is reached during a simulation. The
    property is `attribute` and is assumed to be an attribute of
    simulation.

    Return: the ratio between current and target values of the attribute.
    """
    x = float(getattr(sim, attribute))
    if value > 0:
        frac = float(x) / value
        _log.debug('target %s now at %g [%d]', attribute, x, int(frac * 100))
    if x >= value:
        raise SimulationEnd('reached target %s: %s', attribute, value)
    return frac

def target_rmsd(sim, value):
    """Target the root mean squared displacement."""
    return target(sim, 'rmsd', value)

def target_steps(sim, value):
    """Target the number of steps."""
    if sim.current_step >= value:
        raise SimulationEnd('reached target steps %d' % value)
    return float(sim.current_step) / value

def target_walltime(sim, value):
    """
    Target a value of the elapsed wall time in seconds from the
    beginning of the simulation.

    Useful to self restarting jobs in a queining system with time
    limits.
    """
    wtime_limit = value
    if sim.wall_time() > wtime_limit:
        raise SimulationEnd('target wall time reached')
    else:
        t = sim.wall_time()
        dt = wtime_limit - t
        _log.debug('elapsed time %g, reamining time %g', t, dt)


def target_python_stop(sim, condition):
    """
    Stop the simulation if `condition` is True.

    `condition` will interpolate attributes of the passed `sim`
    instance. For instance, the condition

        #!python
        {current_step} > 1000 and {rmsd} > 1.0

    will stop the simulation when the step is > 1000 and the rmsd > 1.
    """
     # We do nothing on the first step
    if sim.current_step == 0:
        return
    # Interpolate the command string
    cmd = condition.replace('{', '{0.')
    cmd = cmd.format(sim)
    if eval(cmd):
        raise SimulationEnd('condition "{}" satisfied'.format(condition))

def shell_stop(sim, cmd, exit_code=1):
    """
    Execute the shell command `cmd` and stop the simulation if the
    command returns an exit value equal to `exit_code`.

    `cmd` is actually a format string that may contain references to
    the passed `sim` instance. For instance, a valid command is

        #!python
        echo {sim.current_step} {sim.rmsd} >> {sim.output_path}.out

    which will append the step and rmsd to {sim.output_path}.out.
    """
    import subprocess
    # We do nothing on the first step
    if sim.current_step == 0:
        return
    try:
        # Interpolate the command string
        wrap_cmd = cmd.format(sim=sim)
        # Run the shell command
        output = subprocess.check_output(wrap_cmd, shell=True,
                                         stderr=subprocess.STDOUT, executable="/bin/bash")
        if len(output) > 0:
            _log.info('shell command "{}" returned: {}'.format(cmd, output.strip()))

    except subprocess.CalledProcessError as e:
        # We stop the simulation
        if e.returncode == exit_code:
            raise SimulationEnd('shell command "{}" returned "{}"'.format(cmd, e.output.strip()))
        else:
            _log.error('shell command {} failed with output {}'.format(cmd, e.output))
            raise

def user_stop(sim):
    """
    Allows a user to stop the simulation smoothly by touching a STOP
    file in the output root directory.  Currently the file is not
    deleted to allow parallel jobs to all exit.
    """
    # To make it work in parallel we should broadcast and then rm
    # or subclass userstop in classes that use parallel execution
    if sim.output_path is not None:
        if os.path.isdir(sim.output_path):
            dirpath = sim.output_path
        else:
            dirpath = os.path.dirname(sim.output_path)
        if os.path.exists('%s/STOP' % dirpath):
            raise SimulationEnd('user has stopped the simulation')

# Aliases

target_user_stop = user_stop
target_shell_stop = shell_stop


class Speedometer(object):

    """Display speed of simulation and remaining time to reach target."""

    def __init__(self):
        self._init = False

    def __str__(self):
        return 'speedometer'

    def __call__(self, sim):
        if not self._init:
            # We could store all this in __init__() but this
            # way we allow targeters added to simulation via add()
            for c in sim._callback:
                if c is self:
                    continue
                if 'target' in c.__name__.lower():
                    self._callback = c
                    args = sim._cbk_params[c]['args']
                    kwargs = sim._cbk_params[c]['kwargs']
                    self.x_last = c(sim, *args, **kwargs)
                    self.t_last = time.time()
                    self._init = True
                    return

        t_now = time.time()
        args = sim._cbk_params[self._callback]['args']
        kwargs = sim._cbk_params[self._callback]['kwargs']
        x_now = self._callback(sim, *args, **kwargs)
        # Get the speed at which the simulation advances
        speed = (x_now - self.x_last) / (t_now - self.t_last)
        # Report fraction of target achieved and ETA
        frac = float(x_now) / 1
        try:
            eta = (1.0 - x_now) / speed
            d_now = datetime.datetime.now()
            d_delta = datetime.timedelta(seconds=eta)
            d_eta = d_now + d_delta
            # self._callback.__name__,
            _log.info('%2d%% ETA: %s S/T: %.1f T/SP: %.2e',
                      int(frac * 100),
                      d_eta.strftime('%Y-%m-%d %H.%M'),
                      1./sim.wall_time(per_step=True),
                      sim.wall_time(per_step=True, per_particle=True))
        except ZeroDivisionError:
            print(x_now, self.x_last)
            raise

        self.t_last = t_now
        self.x_last = x_now
