#!/bin/bash
cd app
celery -A tasks.app worker -c 2
python main.py