import logging

import asyncclick as click
from temporalio.worker import Worker

from agent import settings
from agent.temporal.client import get_temporal_client
from agent.temporal.workflow import SolveAoCProblemWorkflow
from agent.temporal import activities


@click.command()
async def main() -> None:
    # Just for the sake of this demo worker, let's see info logs.
    logging.basicConfig(level=logging.INFO)

    # Create a worker for the workflow
    worker = Worker(
        await get_temporal_client(),
        # TODO(steving) Generalize this to enable running locally or against prod Temporal Cloud.
        task_queue=settings.TEMPORAL_TASK_QUEUE_NAME,
        workflows=[SolveAoCProblemWorkflow],
        activities=[
            activities.extract_problem_part,
        ],
    )

    # Run the worker indefinitely, so that it polls for tasks.
    await worker.run()


if __name__ == "__main__":
    main()
