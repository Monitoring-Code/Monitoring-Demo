from datetime import datetime, timedelta
import time
from Log.Logging import Logger

from Utils.Compilador import Compiler
from DB.Editor_DB import DB

class Requests_Controller():
    def __init__(self):
        self.DB_Controller = DB()
        #self.df_csv = self.DB_Controller.Leer_CSV()
        self.logger = Logger()
    
    # Obtiene los precios y los guarda en el csv
    def __Save_Datos(self):
        respuesta = self.__Compilar_Datos()
        print(respuesta)
        
        if not respuesta:
            self.logger.add_log("critical", "No se obtuvo una respuesta y no escribió ningún valor en la base de datos por que no se encontró la base de datos")
            return
        
        lista_precios = [respuesta["USD"], respuesta["EURO"], respuesta["MLC"], respuesta["Fecha"]]
        
        base_datos = DB()
        base_datos.Add_Datos(lista_precios)
    
    def Run_Compiler(self):
        self.__Save_Datos()
        fecha_guardada = self.__Obtener_Fecha()
        fecha_actual = datetime.now()
        
        if not fecha_guardada:
            return
        
        diff = fecha_actual - fecha_guardada
        while diff > timedelta(hours=0, minutes=0, seconds=0):
            time.sleep(2)
            fecha_guardada = fecha_guardada + timedelta(hours=1)
            diff = fecha_actual - fecha_guardada
            self.__Save_Datos()
    
    def __Compilar_Datos(self):
        compiler = Compiler()
        fecha_guardada = self.__Obtener_Fecha()
        fecha_actual = datetime.now()

        fecha_final = fecha_guardada if fecha_guardada else fecha_actual
        respuesta = compiler.Give_Precios(fecha= fecha_final.strftime("%Y-%m-%d"), hora= fecha_final.strftime("%H"))

        last_value = self.__Last_Value()
        if not respuesta:
            if last_value:
                last_value["Fecha"] = fecha_final.strftime("%Y-%m-%d %H:%M")
                return last_value
            else:
                return None
            
        if last_value:
            movimiento_usd = abs(respuesta["USD"] - last_value["USD"])
            movimiento_euro = abs(respuesta["EURO"] - last_value["EURO"])
            movimiento_mlc = abs(respuesta["MLC"] - last_value["MLC"])

            count = 0
            while True:
                if count > 5:
                    break
                
                if any(x>10 for x in [movimiento_usd, movimiento_euro, movimiento_mlc]):
                    self.logger.add_log(level="warn", message=f"Se extrajo un movimiento más alto de 10 USD: {respuesta['USD']}, EURO: {respuesta['EURO']}, MLC: {respuesta['MLC']}")
                    time.sleep(10)
                    nueva_respuesta = compiler.Give_Precios(fecha= fecha_final.strftime("%Y-%m-%d"), hora= fecha_final.strftime("%H"))
                    
                    if nueva_respuesta:
                        respuesta = nueva_respuesta
                    
                    movimiento_usd = abs(respuesta["USD"] - last_value["USD"])
                    movimiento_euro = abs(respuesta["EURO"] - last_value["EURO"])
                    movimiento_mlc = abs(respuesta["MLC"] - last_value["MLC"])
                
                else: break
                
                count+=1
            
        return respuesta
    
    def __Last_Value(self):
        df_csv = self.DB_Controller.Leer_CSV()
        if not df_csv.empty:
            last_value = df_csv.loc[0].to_dict()
        else:
            self.logger.add_log("warn", "La base de datos estaba vacía. (Módulo-API_Compiler, Método-Last_Value, Line-57)")
            last_value = None
            
        return last_value
    
    def __Obtener_Fecha(self):
        last_value = self.__Last_Value()
        if last_value:
            ultima_fecha = last_value["Fecha"]
            fecha_iso = datetime.fromisoformat(ultima_fecha)
            new_fecha = fecha_iso + timedelta(hours=1)
            print(new_fecha)
            
            return new_fecha
        
        else:
            return None
        
if __name__ == "__main__":
    print("Inicio")
    controller = Requests_Controller()
    controller.Run_Compiler()







    
    
        
