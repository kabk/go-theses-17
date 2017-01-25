#!/bin/bash
git pull
python generate.py
git add index.html
git commit -m "update theses"
git push

