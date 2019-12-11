#!/bin/sh
export PATHONPATH=`pwd`
coverage run --timid --branch --source fe,be --concurrency=thread -m pytest -v -k fe/test/test_new_order.py --ignore=fe/data
coverage combine
coverage report
coverage html
