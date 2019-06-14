#
# Copyright 2015, 2019 Jeremy Schulman, nwkautomaniac@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from itertools import product
import six

if six.PY3:
    xrange = range

__all__ = ['bracket_expansion', 'expand']


_re_brackets = re.compile(r'\[.+?\]')
_re_ranges = re.compile(r'\[(?P<start>-?\d+)-(?P<stop>-?\d+)(,(?P<step>-?\d+))?\]')


def bracket_expansion(pattern, default_step=1):
    """
    Returns a generator that will yield string-replacements of
    pattern given the bracket notation.  Bracket notation is
        [<start>-<stop>]                # step = <default_step>
        [<start>-<stop>,<step>]         # step is caller defined

    For example:
        # create 'ifs' as a generator for even numbered
        # ports on two different linecards:

        ifs = bracket_expansion('ge-[0-1]/0/[0-47,2]')

        # loop through each
        for ifname in ifs:
            print ifname

    The pattern can also be a "reversed" range, for example:
        ifs = bracket_expansion("M[48-1,-1]")

    which will result in the generator creating interfaces
        M48, M47, ... M1
    """

    # extract brackets from pattern

    brackets = _re_brackets.findall(pattern)

    # extract values from the brackets [start-stop,step]  the step
    # value is optional, and defaults to :default_step:

    def range_inputs(bracket):
        match = _re_ranges.match(bracket)
        if not match:
            raise RuntimeError("Invalid bracket expression: %s" % bracket)

        m_dict = match.groupdict()
        start = int(m_dict['start'])
        step = int(m_dict['step'] or default_step)

        # stop is optional, and needs to adjust +/- based on the step value

        stop = m_dict['stop']
        stop = start if stop is None else int(stop) + (1 if step > 0 else -1)

        return start, stop, step

    extracts = [range_inputs(b) for b in brackets]

    # create the replacement numbers for each generator value by
    # taking the product of the extracted bracket values.  the product function
    # will create an iterator, so this is all nice and memory effecient

    repls = product(*[xrange(*n) for n in extracts])

    # create generator to string-substitute the replacement value
    # into the pattern on each iteration.  the technique is to make
    # each replacement value (originally a tuple) into a list.
    # this makes it pop'able.  so (1,2) becomes [1,2] so we can pop
    # values off the front as the re.sub function iterates through
    # the string, yo!

    for each in repls:
        nums = list(each)
        yield(_re_brackets.sub(lambda x: str(nums.pop(0)), pattern))


def expand(pattern, default_step=1):
    """
    This function will return the expanded list of values.

    Parameters
    ----------
    pattern : str
        The bracket expansion expression.

    default_step : int (optional)
        The default numeric step

    Returns
    -------
    list[str]
        List of string values as expanded.
    """
    return list(bracket_expansion(pattern, default_step))
