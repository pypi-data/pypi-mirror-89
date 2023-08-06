import asyncio
import importlib
import sys
from functools import wraps

import click
from click import BadArgumentUsage, Context

from rearq.log import init_logging
from rearq.version import VERSION
from rearq.worker import TimerWorker, Worker


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(f(*args, **kwargs))

    return wrapper


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(VERSION, "-v", "--version")
@click.option("--verbose", default=False, is_flag=True, help="Enable verbose output.")
@click.pass_context
@coro
async def cli(ctx: Context, verbose):
    init_logging(verbose)


@cli.command(help="Start rearq worker.")
@click.argument("rearq", required=True)
@click.option("-q", "--queue", required=False, help="Queue to consume.")
@click.option("-t", "--timer", default=False, is_flag=True, help="Start a timer worker.")
@click.pass_context
@coro
async def worker(ctx: Context, rearq: str, queue, timer):
    splits = rearq.split(":")
    rearq_path = splits[0]
    rearq = splits[1]
    try:
        module = importlib.import_module(rearq_path)
        rearq = getattr(module, rearq, None)
        await rearq.init()
    except (ModuleNotFoundError, AttributeError) as e:
        raise BadArgumentUsage(ctx=ctx, message=f"Init rearq error, {e}.")

    if timer:
        w = TimerWorker(rearq, queue=queue,)
    else:
        w = Worker(rearq, queue=queue)
    await w.async_run()


def main():
    sys.path.insert(0, ".")
    cli()
