#!/bin/bash

pip install -r requirements.txt
mkdir logs
python scripts/download_data.py --data_dir "./data" >> logs/download_data.log 2>&1