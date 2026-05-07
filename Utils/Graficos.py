import streamlit as st 
import pandas as pd
import plotly.express as px 
from datetime import datetime
from datetime import timedelta

from .Metodos_Adicionales import Depurar_Fechas, DF_Copy

class Graphics():
    def __init__(self, df: pd.DataFrame, moneda):
        self.df = DF_Copy(df)
        self.df_depurado = Depurar_Fechas(df)
        self.moneda = moneda
        
    def Building_Fig(self):
        
        
        if self.df_depurado.shape[0] >= 2:
            self.fig = px.line(self.df, x="Fecha", y=str(self.moneda).upper(), title=f"Precio de {self.moneda} en función del tiempo:")
            
            self.__Configuracion_Inicial()
            
            self.__Grid_Buttons()
            self.__Write_Graphic(self.fig)
            
        else:
            st.warning("Aún no hay suficientes datos para mostrar el gráfico")

    @staticmethod
    @st.cache_data
    def __Write_Graphic(fig):
        st.plotly_chart(fig, use_container_width=True)
    
    def __Configuracion_Inicial(self):
        ultima_fecha = self.df["Fecha"][0]
        fecha_buscada = self.__Buscar_Fecha(ultima_fecha, 1)

        
        self.fig.update_xaxes(
            range=[fecha_buscada, ultima_fecha]
            )
        
        self.fig.update_yaxes(title = "Precio", fixedrange = True)
        
        self.fig.update_traces(hovertemplate = "<b style='color:#D9AF21;'>"+str(self.moneda)+"</b><br>Fecha: %{x|%Y-%m-%d}<br>Hora: %{x|%H:%M}<br>Precio: %{y} CUP<extra></extra>")
        self.fig.update_traces(line=dict(color="#D9AF21"))
    
    def __Grid_Buttons(self):
        c1, c2, c3, c4, c5 = st.columns(5)
        ultima_fecha = self.df["Fecha"][0]
        no_hay=None
        
        with c1:
            if st.button("1 día", use_container_width=True, help="Muestra en el gráfico los datos del último día"):
                if self.df_depurado.shape[0] >= 2:
                    fecha_inicial = self.__Buscar_Fecha(ultima_fecha, 1)

                    self.fig.update_xaxes(range=[fecha_inicial, ultima_fecha])
                else:
                    no_hay=1

                    primera_fecha = self.df["Fecha"].iloc[-1]
                    self.fig.update_xaxes(range=[primera_fecha, ultima_fecha])
        
        with c2:
            if st.button("7 día", use_container_width=True, help="Muestra en el gráfico los datos de la ultima semana"):
                if self.df_depurado.shape[0] >= 8:
                    fecha_inicial = self.__Buscar_Fecha(ultima_fecha, 7)
                    no_hay = None
                    
                    self.fig.update_xaxes(range=[fecha_inicial, ultima_fecha])
                    
                else:
                    no_hay=7

                    primera_fecha = self.df["Fecha"].iloc[-1]
                    self.fig.update_xaxes(range=[primera_fecha, ultima_fecha])
        with c3:
            if st.button("30 día", use_container_width=True, help="Muestra en el gráfico los datos del último mes"):
                if self.df_depurado.shape[0] >= 31:
                    fecha_inicial = self.__Buscar_Fecha(ultima_fecha, 30)
                    no_hay = None
                    
                    self.fig.update_xaxes(range=[fecha_inicial, ultima_fecha])
                
                else:
                    no_hay=30

                    primera_fecha = self.df["Fecha"].iloc[-1]
                    self.fig.update_xaxes(range=[primera_fecha, ultima_fecha])
        
        with c4:
            if st.button("90 día", use_container_width=True, help="Muestra en el gráfico los datos de los ultimos 3 meses"):
                if self.df_depurado.shape[0] >= 91:
                    fecha_inicial = self.__Buscar_Fecha(ultima_fecha, 90)
                    no_hay = None
                    
                    self.fig.update_xaxes(range=[fecha_inicial, ultima_fecha])
                
                else:
                    no_hay=90
                    
                    primera_fecha = self.df["Fecha"].iloc[-1]
                    self.fig.update_xaxes(range=[primera_fecha, ultima_fecha])
        
        with c5:
            if st.button("Todo", use_container_width=True, help="Muestra en el gráfico todos los datos guardados"):
                primera_fecha = self.df["Fecha"].iloc[-1]
                self.fig.update_xaxes(range=[primera_fecha, ultima_fecha])
        
        if no_hay:
            st.warning(f"Aún no hay datos de {no_hay} días atrás. Se mostrarán todos los datos que hay")
    
    # Metodos adicionales
    def __Buscar_Fecha(self, ultima_fecha, diferencial):
        lista_fecha = ultima_fecha.split()
        fecha_iso = datetime.fromisoformat(lista_fecha[0])
        dia_buscado = (fecha_iso - timedelta(days=diferencial)).isoformat()
        
        fecha_buscada = dia_buscado.replace("T", " ")
        
        return fecha_buscada
    
    def __Buscar_Indice(self, fecha_buscada):
        indice = self.df[self.df["Fecha"] == fecha_buscada].index.unique()[0]
        return indice
        
        
            
    
