## MongoMeter

MongoDB aggregation pipeline performance checker

### Install

```shell
pip install mongometer
```

### Console

#### Example

Input

```shell
mongometer --url="mongodb://test:test@localhost:27017" --db=shop --collection bikes --path agg.json
```

Output

```shell
Processing ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
$match     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
$set       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
$match     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
$lookup    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
$unwind    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
$unwind    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
$project   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
$sort      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
$facet     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
$set       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
                 Results                  
┏━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    ┃ Name     ┃ Time (seconds)         ┃
┡━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ $match   │ 1.5710415840148926     │
│ 2  │ $set     │ 0.0                    │
│ 3  │ $match   │ 0.0                    │
│ 4  │ $lookup  │ 0.00015425682067871094 │
│ 5  │ $unwind  │ 0.0014383792877197266  │
│ 6  │ $unwind  │ 0.003248453140258789   │
│ 7  │ $project │ 0.06569337844848633    │
│ 8  │ $sort    │ 3.276400566101074      │
│ 9  │ $facet   │ 0.5028722286224365     │
│ 10 │ $set     │ 0.0                    │
└────┴──────────┴────────────────────────┘

```

#### Parameters

```shell
Usage: mongometer [OPTIONS]

Options:
  --url TEXT         MongoDB connection string  [required]
  --db TEXT          MongoDB database name  [required]
  --collection TEXT  MongoDB collection name  [required]
  --path TEXT        Path to the aggregation pipeline json file  [required]
  --repeat INTEGER   Number of repeats
  --help             Show this message and exit.

```

### Python code

```python
from mongometer import AggregationChecker

URI = "mongodb://test:test@localhost:27017"
DB_NAME = "shop"
COLLECTION_NAME = "bikes"

PIPELINE = [
    {
        "$match": {
            "$text": {"$search": "John"},
        }
    },
    {
        "$sort": {
            "created_at": 1
        }
    }
]

checker = AggregationChecker(URI, DB_NAME, COLLECTION_NAME)
checker.measure(pipeline=PIPELINE).print()
```