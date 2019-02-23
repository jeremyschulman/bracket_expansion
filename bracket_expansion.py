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

_bracket = r'\[.+?\]'
_bracket_extract = r'\[(-?\d+)\-(-?\d+)(,\d)?\]'


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

    You can also get the complete list of values by applying
    the 'list' function, for example:

        ifs = list(bracket_expansion('ge-0/0/[0-47]'))
        # ifs is now a list containing 48 entries
    """
    re_br = re.compile(_bracket)
    re_ext = re.compile(_bracket_extract)

    # extract brackets from pattern

    brackets = re_br.findall(pattern)

    # extact values from the brackets [start-stop,step]  the step
    # value is optional, and defaults to :default_step:

    range_inputs = lambda n: (int(n[0]), int(n[1])+1, default_step if not n[2] else int(n[2][1:]))
    extracts = [range_inputs(re_ext.match(b).groups()) for b in brackets]

    # create the replacement numbers for each generator value by
    # taking the product of the extracted bracket values.  the product function
    # will create an iterator, so this is all nice and memory effecient

    repls = product(*[xrange(*n) for n in extracts])

    # create generator to string-substitue the replacement value
    # into the pattern on each iteration.  the technique is to make
    # each replacement value (originally a tuple) into a list.
    # this makes it pop'able.  so (1,2) becomes [1,2] so we can pop
    # values off the fron as the re.sub function iterates through
    # the string, yo!

    for each in repls:
        nums = list(each)
        yield(re_br.sub(lambda x: str(nums.pop(0)), pattern))


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
