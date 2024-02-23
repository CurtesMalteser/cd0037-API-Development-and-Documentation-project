#!/usr/bin/env bash

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
dropdb trivia_test