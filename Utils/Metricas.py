import streamlit as st
import pandas as pd
from .Metodos_Adicionales import Depurar_Fechas

class Tools_Metricas():
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def Metricas_Resumen(self):
        if self.df.shape[0] >= 2:
            col1, col2, col3 = st.columns(3)
            
            precio_usd = self.df["USD"][0]
            precio_euro = self.df["EURO"][0]
            precio_mlc = self.df["MLC"][0]
            
            movimiento_usd = precio_usd - self.df["USD"][1]
            movimiento_euro = precio_euro - self.df["EURO"][1]
            movimiento_mlc = precio_mlc - self.df["MLC"][1]
            
            with col1:
                st.metric("USD:", f"${precio_usd}.00", f"{movimiento_usd}.00", delta_color="inverse", format="dollar", border=True, help="Muestra el precio actual del USD y la ultima variación")
                
            with col2:
                st.metric("EURO:", f"${precio_euro}.00", movimiento_euro, delta_color="inverse", format="dollar", border=True, help="Muestra el precio actual del EURO y la ultima variación")
                
            with col3:
                st.metric("MLC:", f"${precio_mlc}.00", movimiento_mlc, delta_color="inverse", format="dollar", border=True, help="Muestra el precio actual del MLC y la ultima variación")
        
        elif self.df.shape[0] == 1:
            col1, col2, col3 = st.columns(3)
            
            precio_usd = self.df["USD"][0]
            precio_euro = self.df["EURO"][0]
            precio_mlc = self.df["MLC"][0]
            
            with col1:
                st.metric("USD", precio_usd, 0.0, delta_color="inverse")
                
            with col2:
                st.metric("EURO", precio_euro, 0.0, delta_color="inverse")
                
            with col3:
                st.metric("MLC", precio_mlc, 0.0, delta_color="inverse")
        
        else:
            st.warning("Aún no hay suficientes datos para mostrar los movimientos")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("USD", 0.0, 0.0, delta_color="inverse")
                
            with col2:
                st.metric("EURO", 0.0, 0.0, delta_color="inverse")
                
            with col3:
                st.metric("MLC", 0.0, 0.0, delta_color="inverse")
    
    def Metricas_Temporales(self, moneda):
        new_df = Depurar_Fechas(self.df)
        if new_df.shape[0] >= 2:
            
            c1, c2, c3, c4, c5 = st.columns(5)
                
            with c1:
                delta = self.__Building_Delta(new_df, moneda, 1)
                st.metric("", "1 día", f"{delta}%", delta_color="inverse", label_visibility="collapsed")
                
            with c2:
                delta = self.__Building_Delta(new_df, moneda, 7) if new_df.shape[0] >= 7 else self.__Building_Delta(new_df, moneda, -1)
                st.metric("", "7 día", f"{delta}%", delta_color="inverse", label_visibility="collapsed")
                
            with c3:
                delta = self.__Building_Delta(new_df, moneda, 30) if new_df.shape[0] >= 30 else self.__Building_Delta(new_df, moneda, -1)
                st.metric("", "30 día", f"{delta}%", delta_color="inverse", label_visibility="collapsed")
                
            with c4:
                delta = self.__Building_Delta(new_df, moneda, 90) if new_df.shape[0] >= 90 else self.__Building_Delta(new_df, moneda, -1)
                st.metric("", "90 día", f"{delta}%", delta_color="inverse", label_visibility="collapsed")
                
            with c5:
                delta = self.__Building_Delta(new_df, moneda, -1)
                st.metric("", "Todo", f"{delta}%", delta_color="inverse", label_visibility="collapsed")
        
        else:
            st.warning("Aún no hay suficientes datos para mostrar las métricas temporales")
            c1, c2, c3, c4, c5 = st.columns(5)
                
            with c1:
                st.metric("", "1 día", "0.0%", delta_color="inverse", label_visibility="collapsed")
                
            with c2:
                st.metric("", "7 día", "0.0%", delta_color="inverse", label_visibility="collapsed")
                
            with c3:
                st.metric("", "30 día", "0.0%", delta_color="inverse", label_visibility="collapsed")
                
            with c4:
                st.metric("", "90 día", "0.0%", delta_color="inverse", label_visibility="collapsed")
                
            with c5:
                st.metric("", "Todo", "0.0%", delta_color="inverse", label_visibility="collapsed")
    
    
    def __Building_Delta(self, df: pd.DataFrame, moneda, posicion):
        precio_actual = df[str(moneda).upper()].iloc[0]
        
        precio_buscado = df[str(moneda).upper()].iloc[posicion]
        delta = precio_actual-precio_buscado
        
        delta_porcentual =  round((delta/precio_actual)*100, 1)
        return delta_porcentual
        
            
        
    
