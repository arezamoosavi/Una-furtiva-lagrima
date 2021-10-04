.PHONY: airflow spark scale-spark superset down

down:
	docker-compose down -v

airflow:
	docker-compose up -d airflow

spark:
	docker-compose up -d spark-master
	sleep 2
	docker-compose up -d spark-worker

scale-spark:
	docker-compose scale spark-worker=3

superset:
	docker-compose up -d superset

pg:
	docker-compose up -d postgres

create-dbs:
	docker-compose exec postgres |

run-spark:
	docker-compose exec airflow \
	spark-submit --master spark://spark-master:7077 \
	--deploy-mode client --driver-memory 2g --num-executors 2 \
	--py-files dags/etl/utils/common.py \
	--jars dags/etl/jars/postgresql-42.2.5.jar \
	dags/etl/spark_read_data.py