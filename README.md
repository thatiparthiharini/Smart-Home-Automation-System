
# Smart Home Automation System

## Project Description
A web-based Smart Home Automation System that allows users to control and monitor simulated smart home devices through a dashboard.

## Features
- Control smart devices using ON/OFF buttons.
- Monitor device status.
- Schedule automatic device operations.
- Store device information using SQLite.
- Maintain device activity logs.
- Display scheduled tasks.
- Automatically refresh schedules and activity logs.

## Technologies Used
- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Paho MQTT (installed; hardware or broker integration is not yet implemented)

## Devices Simulated
- Smart Light
- Smart Fan
- Smart Air Conditioner

## How to Run
1. Install the required libraries:
   pip install -r requirements.txt

2. Run the Flask application:
   python app.py

3. Open the local URL displayed in the terminal.

## Project Structure
- app.py
- device_control.py
- scheduler.py
- database/
- templates/
- static/
- reports/

## Note
This project currently simulates smart home devices using Python and SQLite. Physical Raspberry Pi hardware and MQTT communication are not connected.
