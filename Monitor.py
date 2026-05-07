import streamlit as st
import pandas as pd
import plotly as px

from Utils.Graficos import Graphics
from Utils.Tablas import Table
from Utils.Metricas import Tools_Metricas
from Utils.Metodos_Adicionales import DF_Copy

from DB.Editor_DB import DB

class Monitor_Controller():
    def __init__(self):
        self.__Configuracion()
        self.__Control_ForEmpty()
    
    def __Control_ForEmpty(self):
        db_controller = DB()
        if "df" not in st.session_state:
            st.session_state.df = db_controller.Leer_CSV()
        
        if not st.session_state.df.empty:
            self.df_default = DF_Copy(st.session_state.df)
            self.metricas = Tools_Metricas(st.session_state.df)
            self.tablas = Table()
            self.__Body()
        
        else: 
            st.warning("Aún no se puede mostrar el monitor porq no hay datos. Por favor espere a que se obtengan. Se hace un monitoreo a cada hora, si ya pasó ese tiempo y aún no hay datos asegurese de tener bien instalado el sistema. Gracias por su comprensión.")
    
    def __Body(self):
        self.__Styles()
        choice = self.__Sidebar()
        self.__Contenido(choice)
        

    def __Styles(self):
        st.markdown("""
                    <style>
                        :root {
                            --color-text-primary: #D9AF21;
                            --color-text-secundary: #21d949;
                        }

                        #MainMenu {
                            visibility: hidden;
                        }
                        
                        #bienvenido-al-monitor-de-monedas-en-el-mercado-informal {
                            color: var(--color-text-primary);
                        }
                        
                        .st-emotion-cache-vns552 {
                            color: var(--color-text-primary);
                        }
                        
                        #datos-extraidos{
                            color: var(--color-text-primary);
                        }
                        
                        a[kind="secondary"] {
                            color: var(--color-text-primary);
                        }
                        
                        a {
                            color: var(--color-text-primary);
                        }
                        
                        .st-emotion-cache-1lads1q {
                            color: var(--color-text-primary);
                        }
                        
                        .xy {
                            background: var(--color-text-primary);
                            color: var(--color-text-primary);
                        }
                        
                        .stMetric {
                            display: flex;
                            justify-content: space-around;
                            align-items: space-around;
                            text-align: center;
                        }
                    
                    </style>
                    """, unsafe_allow_html=True)
    
    def __Configuracion(self):
        st.set_page_config(
            page_title="Monitor de Monedas",
            page_icon="Media/Icons/Icon-primary.png"
        )
    
    def __Sidebar(self):
        with st.sidebar:
            st.header("Menú")
            
            choice = st.selectbox("Que sección quieres ver:", ["Resumen", "USD", "EURO", "MLC", "Sobre el proyecto"])
            
            return choice
        
    def __Contenido(self, choice):
        if choice == "Resumen":
            self.__Resumen()
        
        elif choice == "USD":
            self.__UI_Monedas("USD")
        
        elif choice == "EURO":
            self.__UI_Monedas("EURO")
        
        elif choice == "MLC":
            self.__UI_Monedas("MLC")
        
        else:
            self.__Saludo()
    
    def __Resumen(self):
        st.title("Bienvenido al monitor de monedas en el mercado informal", text_alignment="center")

        st.space()
        self.metricas.Metricas_Resumen()
        st.space()

        st.subheader("Datos extraidos", text_alignment="center")
        self.tablas.Building_Table(self.df_default)
        
    
    def __UI_Monedas(self, moneda):
        st.title(f"Mire los detalles sobre el {moneda.upper()}", text_alignment="center")
        st.divider()
        self.metricas.Metricas_Temporales(moneda.upper())
        st.divider()
        
        tablas = Graphics(self.df_default, moneda.upper())
        tablas.Building_Fig()

    
    def __Saludo(self):
        st.title("Espero que le agrade este monitor", text_alignment="center")
        st.divider()
        
        st.subheader("Si necesita monitorizar algo en la web puede contactar conmigo puedo realizar monitoreos de: \n")
        st.markdown("""
                - Monedas o criptomonedas.
                - Cualquier tipo de producto en la web.
                - Vacantes de algunos sitios.
                - Puedo añadir un sistema de notificaciones por telegram para avisarle ante cualquier cambio importante.
                """)

        st.space()
        with st.expander("Para pymes y pequeñas empresas."):
            st.markdown('<p style="color: var(--color-text-primary); text-align: center; font-size: 18px";><strong>¿Necesita organizar un poco más su negocio? Puedo crearle un dashboard interactivo para que pueda visualizar de manera eficiente todos los datos de su empresa.</strong></p>', unsafe_allow_html=True)
        st.divider()

        
        #with st.container(border=True):
        st.subheader("Cualquier duda o petición no dude en contactarme", text_alignment="center")
        st.space("small")
            
        self.__Buttons_Contact()

    @staticmethod
    @st.cache_data
    def __Buttons_Contact():
        with st.container(horizontal=True, horizontal_alignment="center"):

            st.link_button("WhatsApp", "https://wa.me/58535583", use_container_width=True, help="Escribe al 58535583")
                
            st.link_button("Email", "mailto:oscarcalero700@gmail.com", use_container_width=True, help="Envia un email a oscarcalero700@gmail.com")
        
    def __Building_Demo(self, cantidad_dias):
        import numpy
        from datetime import datetime
        
        fechas = pd.date_range(end="2026-03-20", periods=cantidad_dias*24, freq="h")
        usd = numpy.random.randint(530, 540, len(fechas))
        euro = numpy.random.randint(630, 640, len(fechas))
        mlc = numpy.random.randint(430, 440, len(fechas))

        df = pd.DataFrame(
            {
                "USD": usd,
                "EURO": euro,
                "MLC": mlc,
                "Fecha": fechas
            }
        )
        all_fechas = []
        for fecha in df["Fecha"].to_list():
            fecha_wena = fecha.isoformat().replace("T", " ")
            all_fechas.append(fecha_wena)
        
        df["Fecha"] = all_fechas
        df = df.iloc[::-1].reset_index(drop=True)
        
        return df
            
Monitor_Controller()
            
        
    
        
        
    
    
    
