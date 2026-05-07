import pandas as pd

def Depurar_Fechas(df):
        df_edit = df.copy()

        lista_fecha = df_edit["Fecha"].to_list()
        
        date_day = []
        for fecha in lista_fecha:
            date_day.append(fecha.split()[0])
        
        df_edit["Fecha"] = date_day
        new_df = df_edit.groupby("Fecha").mean().round(0).reset_index()
        new_df = new_df.iloc[::-1].reset_index(drop=True)
        
        return new_df

def DF_Copy(df):
    df_default = pd.DataFrame()
    df_default["USD"] = df["USD"]
    df_default["EURO"] = df["EURO"]
    df_default["MLC"] = df["MLC"]
    df_default["Fecha"] = df["Fecha"]
        
    return df_default