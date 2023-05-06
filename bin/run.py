#!/usr/bin/env python3
"""
CLI binary to run the code in this repository.
"""

import os
import sys

import numpy as np
import typer
from loguru import logger

from handout_10.rmq import block, naive, simple

app = typer.Typer()


def _setup_loggers(log_level: str = "INFO"):
    # this log sink writes to stdout
    logger.add(
        sys.stdout,
        colorize=True,
        format="<level>{level} | {name}::{function}:{line} | {message}</level>",  # noqa: E501
        level=log_level,
    )


def test(func, name, n=100):
    pts = []
    qts = []
    for i in range(2, n):
        _, pt, qt = func(i)
        pts.append(pt)
        qts.append(qt)
        if i % 10 == 0:
            logger.info(f"{name} : Finished testing with N = {i}")

    return pts, qts


@app.command()
def main():
    """
    Run the RMQ experiment.
    """
    # test simple
    pts, qts = test(simple, "Simple", n=200)
    np.savetxt(
        "rmq_simple.csv", np.array([pts, qts]), delimiter=",", fmt="%.16f"
    )
    os.system("tr , '\n' < rmq_simple.csv > tmp; mv tmp rmq_simple.csv")

    # test naive
    pts, qts = test(naive, "Naive", n=200)
    np.savetxt(
        "rmq_naive.csv", np.array([pts, qts]), delimiter=",", fmt="%.16f"
    )
    os.system("tr , '\n' < rmq_naive.csv > tmp; mv tmp rmq_naive.csv")

    # test block
    pts, qts = test(block, "Block", n=200)
    np.savetxt(
        "rmq_block.csv", np.array([pts, qts]), delimiter=",", fmt="%.16f"
    )
    os.system("tr , '\n' < rmq_block.csv > tmp; mv tmp rmq_block.csv")


def _main():
    """
    Dummy main function to instantiate the typer app for integration with
    poetry script commands.

    Args: None, Returns: None
    """
    _setup_loggers()
    app()


if __name__ == "__main__":
    """
    Include this in case there is a need to run this script outside of the
    'poetry run' environment. Typically needed if sudo privileges are required.
    """
    _main()
