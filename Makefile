.PHONY: airflow spark scale-spark metabase down

down:
	docker-compose down -v

airflow:
	docker-compose up -d airflow
	sleep 15
	docker-compose up -d airflow-spark-queue

scale-spark-queue:
	docker-compose scale airflow-spark-queue=3

spark:
	docker-compose up -d spark-master
	sleep 2
	docker-compose up -d spark-worker

scale-spark:
	docker-compose scale spark-worker=3

metabase:
	docker-compose up -d metabase

pg:
	docker-compose up -d postgres

run-spark:
	docker-compose exec airflow \
	spark-submit --master spark://spark-master:7077 \
	--deploy-mode client --driver-memory 2g --num-executors 1 \
	--py-files dags/etl/utils/common.py \
	--jars dags/etl/jars/postgresql-42.2.5.jar \
	dags/etl/spark_load_data.py