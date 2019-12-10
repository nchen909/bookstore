#!/bin/sh
export PATHONPATH=`pwd`
coverage run --timid --branch --source fe,be --concurrency=thread -m pytest -v -k fe/test/test_add_book.py --ignore=fe/data
coverage combine
coverage report
coverage html
