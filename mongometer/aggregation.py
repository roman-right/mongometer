import time
from typing import List, Dict, Any

import pymongo
from rich.progress import Progress
from rich.table import Table
from rich.console import Console

MODERATE = 0.1
SLOW = 1


class StepPerformance:
    def __init__(self, number, step, time):
        self.number = number
        self.step = step
        self.name = list(step.keys())[0]
        self.time = time


class PerformanceInfo:
    def __init__(self):
        self.steps: List[StepPerformance] = []

    def _add_step_info(self, step: StepPerformance):
        self.steps.append(step)

    @staticmethod
    def _colorify(number: float):
        if number > SLOW:
            return f"[red]{number}"
        if number > MODERATE:
            return f"[yellow]{number}"
        return f"[green]{number}"

    def print(self):
        table = Table(title="Results")
        table.add_column("", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Time (seconds)")
        for step in self.steps:
            table.add_row(
                f"{step.number}", f"{step.name}", self._colorify(step.time)
            )
        console = Console()
        console.print(table)


class AggregationChecker:
    def __init__(
        self,
        connection_string: str,
        db_name: str,
        collection_name: str,
        repeat: int = 10,
    ):
        client = pymongo.MongoClient(connection_string)
        db = client[db_name]
        self.collection = db[collection_name]
        self.repeat = repeat
        self.results: List[StepPerformance] = []

    def _run_sub_pipeline(self, pipeline, progress) -> float:
        result = 0

        step_name = list(pipeline[-2].keys())[0]

        sub_task = progress.add_task(f"[green]{step_name}", total=self.repeat)

        for _ in range(self.repeat):
            time_started = time.time()
            self.collection.aggregate(pipeline)
            time_finished = time.time()

            result += time_finished - time_started

            progress.update(sub_task, advance=1)

        result = result / self.repeat

        return result

    def measure(self, pipeline: List[Dict[str, Any]]):
        performance = PerformanceInfo()
        new_pipeline = []
        prev_time = 0.0
        with Progress() as progress:

            main_task = progress.add_task(
                "[magenta]Processing", total=len(pipeline)
            )

            for number, step in enumerate(pipeline, start=1):
                new_pipeline.append(step)

                # TODO this reduces output time,
                #  but it should be implemented better
                new_pipeline.append({"$limit": 1})

                step_time = self._run_sub_pipeline(new_pipeline, progress)

                new_pipeline.pop()

                buf = step_time

                step_time -= prev_time
                if step_time < 0:
                    step_time = 0.0

                prev_time = buf

                step_info = StepPerformance(number, step, step_time)

                performance._add_step_info(step_info)

                progress.update(main_task, advance=1)

        return performance
