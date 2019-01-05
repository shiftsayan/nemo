#!/bin/bash
echo "Task 1"
python3 ./stage1.py text.json > out1.json
echo "Task 2"
python3 ./stage2.py out1.json > out2.json
echo "Task 3"
python3 ./stage3.py out1.json out2.json > out3.json
echo "Task 4"
python3 ./stage4.py out2.json out3.json 
echo "Done"
