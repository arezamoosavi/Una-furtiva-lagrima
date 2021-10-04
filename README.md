# Una-furtiva-lagrima
Airflow and Spark at Scale

## Technologies
The main technologies are:
* Docker
* Spark
* Airflow
* Postgres
* Metabase

## How is it work?
This project is study on Bitcoin historical and recent data. Airflow and Spark is used for all the extraction and transformations. The bitcoin database will have two tables, raw and processed data.
#### [part1: Initial ETL](https://github.com/arezamoosavi/Una-furtiva-lagrima/blob/main/airflow/dags/dag_run_initial_load.py)
In order to aggregate all bitcoin historical data, process them and persist them into postgres.

#### [part2: Daily ETL](https://github.com/arezamoosavi/Una-furtiva-lagrima/blob/main/airflow/dags/dag_run_daily.py)
In order to aggregate yesterday bitcoin data, process them and persist them into postgres.

### Spark
Spark is used to read and write data in distributed and scalable manner.
```bash
make spark
```
will run spark master and one instance of worker
```bash
make scale-spark
```
will scale spark worker.
### Airflow
Airflow uses CeleryExecutor in order to scale the spark workflows and tasks. Here the postgres is used for celery result backend and broker.

```bash
make pg
make airflow
```
```bash
make scale-spark-queue
```
This will scale spark celery queue.

```bash
make stop-airflow
```
It will stop airflow and spark queue.

### Metabase
In order to create a simple dashboard:
```bash
make metabase
```
A sample result could be found [here](https://github.com/arezamoosavi/Una-furtiva-lagrima/blob/main/docs/metabase_chart.png).

#### CLEAN
In order to clean and stop all the containrs:
```bash
make down
```