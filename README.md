![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![ML Client CI](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/ml-client.yml/badge.svg)
![Web App CI](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/webapp.yml/badge.svg)

# Containerized App Exercise

## **Overview**

This application will utilize machine learning to assist with exercise, namely counting jumping jacks as well as tracking calories burned per session and over the usage lifetime. 

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

2. Access the application through the URL http://localhost:5001/ on your local system.

### Stopping the System
1. Run:
```bash
docker-compose down
```

