import json

import click

from mongometer.aggregation import AggregationChecker


@click.command()
@click.option(
    "--url", required=True, type=str, help="MongoDB connection string"
)
@click.option(
    "--db",
    required=True,
    type=str,
    help="MongoDB database name",
)
@click.option(
    "--collection",
    required=True,
    type=str,
    help="MongoDB collection name",
)
@click.option(
    "--path",
    required=True,
    type=str,
    help="Path to the aggregation pipeline json file",
)
@click.option(
    "--repeat",
    required=False,
    type=int,
    default=10,
    help="Number of repeats",
)
def measure(url, db, collection, path, repeat):
    with open(path) as f:
        pipeline = json.load(f)
        checker = AggregationChecker(url, db, collection, repeat)
        checker.measure(pipeline=pipeline).print()


if __name__ == "__main__":
    measure()
