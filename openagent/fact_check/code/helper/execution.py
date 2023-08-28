# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import ctypes
# libgcc_s = ctypes.CDLL('libgcc_s.so.1')

from collections import defaultdict
from concurrent.futures import as_completed, ProcessPoolExecutor
import logging

from factool.code.helper._execution import test_case_against_solution

logging.basicConfig(
    format="SystemLog: [%(asctime)s][%(name)s][%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

def evaluate_test_cases_multi_solution(prompt, testcases_input,
                                       multi_solutions, timeout=0.1):
    logger.info(f'Start evaluation with test code, timeout={timeout}')

    with ProcessPoolExecutor() as executor:
        futures = []
        results = [[None for _ in multi_solutions] for _ in testcases_input]

        for i, testcase in enumerate(testcases_input):
            for j, solution in enumerate(multi_solutions):
                args = (prompt, solution, testcase, timeout)
                future = executor.submit(test_case_against_solution, *args)
                futures.append((i, j, future))
        logger.info(f'{len(futures)} execution requests are submitted')
        
        for completed_future in as_completed([f[2] for f in futures]):
            for i, j, future in futures:
                if future == completed_future:
                    logger.info('[{}/{}] execution completed'.format(
                        i * len(multi_solutions) + j + 1, len(futures)))
                    result = completed_future.result()
                    results[i][j] = result
                    break

    return results






