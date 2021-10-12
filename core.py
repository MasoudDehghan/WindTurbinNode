from jproperties import Properties
from mysql.connector.errors import DatabaseError
from dbHandler import DatabaseHandler 
from kafka import KafkaProducer
from json import dumps
import json
from datetime import date, datetime
import decimal
import time, threading
import atexit
import logging
import sys

class CoreThread:

    def __init__(self):
        try:
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.DEBUG)

            c_handler = logging.StreamHandler(sys.stdout)
            f_handler = logging.FileHandler('wturbine.log')

            c_format = logging.Formatter('%(asctime)s - %(message)s')
            f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            c_handler.setFormatter(c_format)
            f_handler.setFormatter(f_format)
            c_handler.setStream(sys.stdout)
            # Add handlers to the logger
            self.logger.addHandler(c_handler)
            self.logger.addHandler(f_handler)
            self.logger.info('WindTurbine Data Producer is started')
            self.configFileName = "app-config.properties"
            self.config = Properties()
            self.producer = None
            
            with open(self.configFileName, 'r+b') as config_file:
                self.config.load(config_file)
        
            self.KAFKA_URL = self.config.get("KAFKA_URL").data
            self.KAFKA_TOPIC = self.config.get("KAFKA_TOPIC").data
            self.SEND_DATA_INTERVAL_SEC =  int(self.config.get("SEND_DATA_INTERVAL_SEC").data)
            self.LAST_ID = int(self.config.get("LAST_ID").data)
            self.prodbHandler = DatabaseHandler(self.config)
            if self.prodbHandler.probirdConnection is None:
                 raise DatabaseError("Unable to connect to db")
            
            #Save LastID to Config file every 5 minutes
            saveLastIDThread = threading.Timer(1 * 5, self.saveLastID)
            saveLastIDThread.start()
            self.logger.info("Timer Task for Updating Last ID every 5 minutes is started")

        except DatabaseError as e:
            self.logger.error(f'{e}, program is terminated!')
            exit()
        except:
            self.logger.error(f'Error in Reading from Config File {self.configFileName}, program is terminated !!!')
            exit()

    def run(self):
        #Save LastID & Close Db Connection on Program Termination
        atexit.register(self.terimnationHandler)

        #Init Kafka Producer
        try:
            # self.producer = KafkaProducer(bootstrap_servers=[self.KAFKA_URL],
            #                     valuse_serializer=lambda x: 
            #                     dumps(x).encode('utf-8'))     
            producer = KafkaProducer(bootstrap_servers=[self.KAFKA_URL],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))      
        except:
            self.logger.error("No Kafka Server is Available on "+self.KAFKA_URL+",program is terminated")
            exit()

        #Reading Data From DB and Send to Kafka Server
       
        while True:
            try:
                cntr = 0
                list = self.readData()           
                if list != None:
                    cntr = len(list)
                    for item in list:
                        try:        
                            jsonStr = json.dumps(item.__dict__,default=self.json_serial)
                            producer.send(self.KAFKA_TOPIC, value=jsonStr)
                            self.LAST_ID = item.ID  
                        except:
                            self.logger.info(f'Error in Sending Record with ID {item.id} , ignored')
                self.logger.info(f'{cntr} records sent to server')
                time.sleep(self.SEND_DATA_INTERVAL_SEC)
            except Exception as e:
                self.logger.error(f'{e}, program is terminated')
                exit(0)
            except KeyboardInterrupt as e:
                self.logger.error(f'Program is terminated by user')
                exit(0)


    def readData(self):
        try:            
            list = self.prodbHandler.readData(self.LAST_ID)  
            return list   
        except:
            self.logger.error("Error in Reading Data from DB")
            return None

    def json_serial(self,obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if type(obj) is decimal.Decimal:
            return float(obj)
        raise TypeError ("Type %s not serializable" % type(obj))

    def saveLastID(self):
        try:
            with open(self.configFileName, "r+b") as f:
                p = Properties()
                p.load(f, "utf-8")
                p["LAST_ID"]=str(self.LAST_ID)
                f.seek(0)
                f.truncate(0)
                p.store(f, encoding="utf-8")
                self.logger.info(f'Writing Last ID {self.LAST_ID} to properties file')
        except:
            self.logger.error("Unable to Update Last ID in properties file")
        
    def terimnationHandler(self):
        self.saveLastID()
        if self.prodbHandler.probirdConnection != None:
            self.prodbHandler.probirdConnection.close()

if __name__ =="__main__":
    coreThread = CoreThread()
    coreThread.run()
   