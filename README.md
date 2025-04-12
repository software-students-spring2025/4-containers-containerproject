![ML Client Build and Test](https://github.com/software-students-spring2025/4-containers-containerproject/actions/workflows/ml-client.yml/badge.svg)
![Web App Build and Test](https://github.com/software-students-spring2025/4-containers-containerproject/actions/workflows/webapp.yml/badge.svg)

# Jumparoo

## **Overview**

Jumparoo is a web application that utilizes machine learning to assist with your exercise goals! Namely, Jumparoo uses your webcam to count the number of jumping jacks you do, as well as the time spent jumping. Jumparoo also tracks your calories burned per jumping session, the total number of calories you've burned using Jumparoo, and, to make jumping fun, Jumparoo also displays a leaderboard of the top jumpers so you can compete with friends and strangers alike!

This project provides a containerized system through these subsystems:
1. **ML Backend:** Uses camera data to perform ML-based jumping jack tracking
2. **Database:** MongoDB database for storing data
3. **Web Interface:** Front-end display using Flask that displays data and enables user interfacing.

## Team Members:
- [Larry Yang](https://github.com/larryyang04)
- [James Hou](https://github.com/James-Hou22)
- [Max Meyring](https://github.com/maxlmeyring)
- [Matthew Cheng](https://github.com/mattchng)

## Configuration and Run Instructions

### Prerequisites
Make sure both **[Docker](https://www.docker.com/products/docker-desktop)** and **[Docker Compose](https://docs.docker.com/compose/install/)** are installed.

### Config and Setup
1. Clone the repository:
```bash
git clone git@github.com:software-students-spring2025/4-containers-containerproject.git
```
2. Create a .env file (literally named: .env) in the root directory with the following contents:
```bash
MONGO_URI=mongodb://mongodb:27017/jumping-jack-db
```

### Running the System
1. Ensure you are in the root directory, and run:
```bash
docker-compose up
```

2. Once the containers are up and running, open your browser and navigate to [http://localhost:5001](http://localhost:5001).


### Stopping the System
1. Run:
```bash
docker-compose down
```

### Note on ML Client Linting
Pylint has historically experienced issues linting OpenCV(cv2)'s package as described in [this](https://github.com/pylint-dev/pylint/issues/2426) issue. It is labelled as fixed but users have had issues years after the issue closed. We tried all fixes as described in this thread but none worked, so we decided on ignoring these linter errors.

