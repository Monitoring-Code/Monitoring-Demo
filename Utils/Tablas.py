import streamlit as st 
import pandas as pd

from .Metodos_Adicionales import Depurar_Fechas, DF_Copy

class Table():
    def __init__(self):
        pass
    
    def Building_Table(self, df):
        df_default = DF_Copy(df)
        
        df_depurado = Depurar_Fechas(df)
        
        if df_depurado.shape[0] <= 7:
            df_default = self.__Formatear_Fecha(df_default)
            self.__Write_Table(df_default)
            
        else:
            columna_borrada = df_depurado.pop("Fecha")
            df_depurado["Fecha"] = columna_borrada
            self.__Write_Table(df_depurado)

    @staticmethod
    @st.cache_data   
    def __Write_Table(df):
        st.dataframe(df)
    
    def __Formatear_Fecha(self, df):
        lista_fechas = df["Fecha"].to_list()
        
        all_fechas = []
        for fecha in lista_fechas:
            all_fechas.append("/".join(fecha.split()))
            
        df["Fecha"] = all_fechas
        return df
            
    
        
