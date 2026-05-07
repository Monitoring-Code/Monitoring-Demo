import logging
from pathlib import Path
import traceback

class Logger():
    def __init__(self):
        self.logger = self.__set_logger()
    
    def __set_logger(self):
        log_ruta=Path(__file__).parent/"Historial.log"              
        
        logger=logging.getLogger(__name__)                    
        logger.setLevel(logging.DEBUG)                        
        
        file=logging.FileHandler(log_ruta, encoding="utf-8")  
        file.setLevel(logging.DEBUG)                          
        format=logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S") 
        file.setFormatter(format)                            
            
        if logger.hasHandlers():                              
            logger.handlers.clear()
            
        logger.addHandler(file)                               
        
        return logger

    #@classmethod
    def add_log(self, level, message):
        try:
            logger=self.__set_logger()
            
            if level=="critical":
                logger.critical(message)
            elif level=="debug":
                logger.debug(message)
            elif level=="error":
                logger.error(message)
            elif level=="info":
                logger.info(message)
            elif level=="warn":
                logger.warn(message)
                
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            
