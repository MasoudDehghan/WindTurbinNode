#WindTurbine Application consists three major Parts:
1.Kafka Server
2.WindTurbine Node Application
3.WindTurbine Server Application

# WindTurbine Node Application
You should Run this app in any system that you want to send data to server.
# Requirements
    1.Install Python 
    2.pip install kafka-python
    3.pip install mysql-connector-python
    4.pip install jproperties

# Modfy app-config.properties 
    1.KAFKA_URL is the URL of Your Kafka Server ----> X.X.X.X:9092
    2.KAFKA_TOPIC  is the name of the topic you added to Kafka Server
    3.Modify DB_HOST,DB_SCHEMA,DB_User,DB_PWD base on your Running MySQL Instance config
    4.SEND_DATA_INTERVAL_SEC is the time period for sending records from nodesto server
    5.LAST_ID is the most recent ID of the record in WindTurbineData Table
        For the Initial Run, Last ID is zero, Every 5 minutes this value will be updated by program
        We track Last ID to prevent sending duplicated data to server
# How to Run
    * Unzip and Move to D:/
    * Open a Command prompt
    * cd to App Folder
    * python core.py

# Troubleshhoting
    * Logs will be saved in a file named "windturbine.log" in app folder