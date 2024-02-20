# Bacon Number Project

## Overview

This project, titled Bacon Number, is inspired by the intriguing concept of the six degrees of Kevin Bacon. According to this concept, anyone in the Hollywood industry can be linked to Kevin Bacon through their film roles in at most six steps. The primary goal of this project is to investigate the validity of this claim and explore various relationships between actors and films.

## Raw Data

The project utilizes raw data stored in .pickle files within the resources folder. The raw data consists of a list of tuples, each containing three elements: actor_1, actor_2, and film.

## Main Code

The core functionality of the project is implemented in the `lab.py` file. Here's a breakdown of its contents:

### Data Transformation

- The `lab.py` file includes code to transform the raw data into two dictionaries:
  - Actor-Actor relations
  - Film-Actor relations

### Actor Relationships

- The file contains functions to check if two actors have worked together.

### Bacon Number Calculation

- The code uses a breadth-first search path-finding algorithm to calculate:
  - The shortest path between an actor and Kevin Bacon
  - The shortest path between two actors
  - The shortest path between an actor and another actor meeting a given constraint

## Test Cases

The `test.py` file consists of test cases created by MIT 6.101 staff to ensure the correctness of the implemented functionalities.

## Getting Started

To get started with the Bacon Number project, follow these steps:

1. Clone the repository.
2. Navigate to the project directory.
3. Execute the main code in `lab.py` to explore actor relationships and Bacon numbers.

## Usage

Provide examples or sample code snippets demonstrating how to use the project's functionalities.

## Acknowledgments

Give credit to MIT 6.101 staff for contributing test cases.

## License

Specify the license under which the project is released.

