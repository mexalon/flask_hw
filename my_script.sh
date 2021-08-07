#!/bin/bash
celery -A tasks.app worker &
python3 main.py

