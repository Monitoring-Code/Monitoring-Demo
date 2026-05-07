import pandas as pd
from pathlib import Path
from datetime import datetime

class DB():
    def __init__(self):
        pass
    
    def Add_Datos(self, datos: list):
        ruta_db = self.__Building_Ruta()
        
        if ruta_db.exists():
            old_df = pd.read_csv(ruta_db)
            new_df = self.__Update_DF(old_df, datos)
            
            new_df.to_csv(ruta_db, index=False)
            
        else:
            new_df = self.__Building_NewDF(datos)
            new_df.to_csv(ruta_db, index=False)
    
    def __Update_DF(self, df_antiguo, datos):
        data_updateada = df_antiguo.values.tolist()
        data_updateada.insert(0, datos)
        
        df_updateado = pd.DataFrame(data_updateada, columns=df_antiguo.columns)
        return df_updateado
    
    def __Building_NewDF(self, datos):
        colums = ["USD", "EURO", "MLC", "Fecha"]
        all_datos = [datos]
        df = pd.DataFrame(all_datos, columns=colums)
        
        return df
    
    def __Building_Ruta(self):
        ruta_db = Path(__file__).parent
        nombre_archivo = "DB_Precios.csv"
        
        ruta_db.mkdir(exist_ok=True)
        ruta_db = ruta_db/nombre_archivo
        return ruta_db
    
    def Leer_CSV(self):
        ruta_db = self.__Building_Ruta()
        
        if ruta_db.exists():
            df = pd.read_csv(ruta_db)
        
        else:
            df = pd.DataFrame()
            
        return df