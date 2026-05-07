import requests
from datetime import datetime
from datetime import timedelta
import time
import traceback
import random
import os

from Log.Logging import Logger


class Compiler():
    def  __init__(self):
        # Cosas a poner en secreto de github
        KEY_TOQUE = os.getenv("API_KEY")

        self.logger = Logger()
        
        self.headers={
            "accept": "*/*",
            "Authorization": KEY_TOQUE,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0"
        }
        
    def Give_Precios(self, fecha, hora):
        hoy=datetime.now()
        posibles_tiempos_to = [(hoy - timedelta(minutes=x)).strftime("%M") for x in range(1, 11)]
        print(posibles_tiempos_to)

        #fecha=hoy.strftime("%Y-%m-%d")
        minutos_from=(hoy - timedelta(minutes=10)).strftime("%M")
        minutos_to=random.choice(posibles_tiempos_to)
        
        for a in range(5):
            try:
                minutos_to=random.choice(posibles_tiempos_to)
                print(minutos_to, "Minuto aleatorio")
                
                response = requests.get(f"https://tasas.eltoque.com/v1/trmi?date_from={fecha}%20{hora}%3A{minutos_from}%3A01&date_to={fecha}%20{hora}%3A{minutos_to}%3A01", headers=self.headers)
                print(response, "%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                break
            except Exception as e:
                self.logger.add_log("error", str(e))
                self.logger.add_log("error", traceback.format_exc())
                response = None
                time.sleep(5)

            if not response:
                continue

            if response.status_code != 200:
                self.logger.add_log("error", f"El código de estado de la petición no fué 200, Status_Code: {response.status_code}")
                response = None
                time.sleep(5)
            else:
                break
                
        if not response:
            return response
            
        tasas = response.json()
        precio_usd = int(tasas["tasas"]["USD"])
        precio_euro = int(tasas["tasas"]["ECU"])
        precio_mlc = int(tasas["tasas"]["MLC"])
        
        return {
            "USD": precio_usd,
            "EURO": precio_euro,
            "MLC": precio_mlc,
            "Fecha": f"{fecha} {hora}:00"
        }
    
if __name__ == "__main__":
    pass
    print(Compiler().Give_Precios("2026-05-04","14"))
        
