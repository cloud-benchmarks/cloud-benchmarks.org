# cloud-benchmarks.org

A Pyramid webapp that displays submitted benchmark results.


## Getting Started

### Database Setup

Postgres 9.4 or later is required due to the use of the JSONB datatype.
You can quickly start up the latest Postgres using Docker:

    # Create a data-only container for postgres data so that our
    # data is preserved when the postgres container is stopped.
    # Only need to do this once.
    sudo docker create -v /var/lib/postgresql/data \
      --name postgres-data postgres /bin/true

    # Start postgres, telling it to use the data volume from our
    # postgres-data container.
    sudo docker run -d --volumes-from postgres-data \
      -e POSTGRES_PASSWORD="postgres" -p 5432:5432 postgres

### Installing

    make

### Running Tests

    make test

### Running the web server

    make serve  # http://localhost:6543

### Loading a sample submission

    make sample  # web server must be running


## Submitting Benchmark Results

Submit benchmark results by posting json to the api:

    curl -X POST http://localhost:6543/submissions \
      -d @./tests/data/submission.json \
      --header "Content-Type: application/json"

The json must adhere to the following format:

    {
      "version": "1.0",
      "action": {
        "status": "completed",
        "started": "2015-06-03T23:45:20-04:00",
        "completed": "2015-06-03T23:49:14-04:00",
        "enqueued": "2015-06-03T23:45:19-04:00",
        "action": {
          "tag": "action-6bf10a8c-a67e-46f5-8fe4-fcac7c0650f1",
          "name": "stress",
          "parameters": {
            "operations": "INSERT",
            "replication-factor": 1,
          },
          "receiver": "unit-cassandra-0"
        },
        "output": {
          "meta": {
            "composite": {
              "units": "ops/sec",
              "direction": "desc",
              "value": "99989.0"
            },
            "start": "2015-06-03T23:45:20Z",
            "stop": "2015-06-03T23:49:13Z"
          },
          "results": {
            "interval-key-rate": {
              "units": "keys/sec",
              "value": "99989.0"
            },
            "total": {
              "units": "ops",
              "value": "11384815.0"
            }
          }
        }
      },
      "bundle": {
        "services": {
          "cabs-collector": {
            "charm": "local:trusty/cabs-collector-0",
            "num_units": 0
          },
          "cassandra": {
            "charm": "local:trusty/cassandra-5",
            "num_units": 1,
            "constraints": {
              "arch": x86_64,
              "mem": 512
            }
          }
        },
        "relations": [
          [
            "cabs-collector",
            "cassandra"
          ]
        ]
      },
      "environment": {
        "uuid": "42aac383-cc20-40fe-8285-0401b6a6532b",
        "cloud": "",
        "provider_type": "gce",
        "region": "us-central-1"
      }
    }

