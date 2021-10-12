#WindTurbine Application consists three major Parts:
1.Kafka Server
2.WindTurbine Node Application
3.WindTurbine Server Application

# Kafka Server
# Download and Setup Kafka Server
1.Download and Install JDK 11 FROM ORACLE WEBSITE
1.Download Kafka Server from https://dlcdn.apache.org/kafka/2.8.1/kafka_2.12-2.8.1.tgz
2.Unzip , Rename to "kafka",Move to D:/
3.Edit kafka/config/server.properties
    * In "Socket Server Settings" Section ---> advertised.listeners=PLAINTEXT://x.x.x.x:9092
        * Replace x.x.x.x with Server IP Address
    * In "Log Basics" Section ---> logs.dir=D:/kafka/data/kafka
4.Edit kafka/config/zookeeper.properties
    * Modify dataDit to dataDir=D:/kafka/data/zookeeper
5.Run zookeeper
    * open a command prompt
    * cd D:/kafka/bin/windows
    * zookeeper-server-start.bat ../../config/zookeeper.properties
6.Run Kafka
    * open a command prompt
    * cd D:/kafka/bin/windows
    * kafka-server-start.bat ../../config/server.properties
7.Add Topic
    * open a command prompt
    * cd D:/kafka/bin/windows
    * kafka-topics.vat --create --topic firstTopic --bootstrap-server localhost:9092    
8.Open TCP ports 9092 and 2181 for remote access in server firewall

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