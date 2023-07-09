# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import re
import logging

import benchexec.result as result
import benchexec.tools.template

from benchexec.tools.sv_benchmarks_util import get_data_model_from_task
from benchexec.tools.sv_benchmarks_util import ILP32
from benchexec.tools.sv_benchmarks_util import LP64


class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info for ABC: A System for Sequential Synthesis and Verification
    URL: https://people.eecs.berkeley.edu/~alanmi/abc/
    """

    def executable(self, tool_locator):
        """""
        return "/home/darwin/PycharmProjects/pythonProject/main.py"
       
        """""

        return tool_locator.find_executable("main.py")

    def name(self):
        return "ChatGPT Tool"

    def cmdline(self, executable, options, task, rlimits):

        data_model_param = get_data_model_from_task(task, {ILP32: "--32", LP64: "--64"})
        if data_model_param and data_model_param not in options:
            options += [data_model_param]

        self.options = options

        return [executable] + list(task.input_files_or_identifier) + options

    def determine_result(self, run):
        if run.was_timeout:
            return result.RESULT_TIMEOUT
        for line in run.output:
            if line.startswith("Yes"):
                return result.RESULT_TRUE_PROP
            elif line.startswith("No"):
                return result.RESULT_FALSE_PROP
            elif line.startswith("Unknown"):
                return result.RESULT_UNKNOWN
            elif line.startswith("Error"):
                return result.RESULT_ERROR
        return result.RESULT_ERROR
