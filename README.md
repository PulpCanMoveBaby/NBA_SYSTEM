# Overview
Using statistical analysis and data from past NBA games over the course of the 2025-26 season, this is a system designed to give each team a score based off of performance over the past n-games.
This method is designed to be relatively hands-off and does not take injuries into consideration. Those analyses fall more into the category
of "scouting" and is left for the user to evaluate on thier own. This purely takes recent statistical performance and uses a unique scoring system to make the prediction.

As of this writing, the system has predicted 66.2% of 604 games correctly. In the early stages of developing this system it was hovering around 55%. 
After many adjustments made to the scoring system, those numbers have improved significantly. 

Reinforcement learning has been implemented as the contribution of each parameter to the overall score is weighted based off of its own performance. 
This weight system is re-calculated daily as new results come in from the previous day, and it is autonomously adjusted to reflect current performance.
The scoring system is adjusted daily in the same way, giving it two layers of reinforcement-learned weights that change and evolve with the actual data.

Optimization strategies, like reducing the sum of the squared errors between parameters with strong performace
and other parameters with variables available for optimization, have been implemented. These strategies have increased performance drastically and are the single biggest reason for the 
increased accuracy of the predictions.

This program will also capture and store the most important information necessary for determining each prediction in csv files
that can easily be imported into a spreadsheet or a pandas DataFrame for use in other programs.

## Features
  - Prediction algorithm capable of predicting just over 2/3 of NBA games correctly
  - Parameters optimized daily using:
      - Past data to determine weights for the scoring system
      - Sum of the squared errors between certain parameters
  - Automatically pulls the data from the nba_api library in python
  - Lead tracker graphs produced daily to visually assess the flow of games from the previous day
  - CSV files produced daily to evaluate team performance and overall system performance

## Libraries Necessary
  - nba_api
  - pandas
  - matplotlib

## Installation Steps
  - Open terminal
  - Create virtual environment and install necessary libraries (recommended) or install them into the base environment
      - pip install library_name
  - Activate venv by running (replacing venv with the name of your virtual environment)
      - source venv/bin/activate
  - Run command
      - python3 00_main_program.py
      - python 00_main_program.py

## Usage
  - Program will ask you if you want to add to the results_tracker csv file
      - This file tracks the performance of each individual parameter in the overall prediction
      - Make sure you want to do this as it is the only part of the program that is difficult to undo
          - To undo this, delete the results_tracker.csv, make a copy of the most recent results_tracker_{datetime.now()}.csv file (in the same folder) and rename it results_tracker.csv
          - If you want to run the program without overwriting this file
              - For example, you may want to just look at the lead tracker graphs, just enter no and you can update it later in a subsequent run
