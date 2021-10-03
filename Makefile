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
	--packages io.delta:delta-core_2.12:1.0.0 --py-files dags/utils/common.py \
	--jars dags/jars/aws-java-sdk-1.11.534.jar,dags/jars/aws-java-sdk-bundle-1.11.874.jar,dags/jars/delta-core_2.12-1.0.0.jar,dags/jars/hadoop-aws-3.2.0.jar,dags/jars/mariadb-java-client-2.7.4.jar \
	dags/etl/spark_initial.py