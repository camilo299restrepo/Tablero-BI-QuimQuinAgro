#!/usr/bin/env python3
# app.py
# Tablero para Reto 2 - Asociación QuimQuinAgro

import streamlit as st
import pandas as pd
import numpy as np
import SQlib as sq
from datetime import datetime, date
import sqlite3
import plotly.express as px

DB_PATH = "contabilidad (2).db"

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Dashboard Financiero - QuimQuinAgro", layout="wide")

# --- FUNCIONES AUXILIARES ---
def ejecutar_sql(consulta, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(consulta, conn, params=params)

# --- PANTALLA DE BIENVENIDA ---
if "nombre" not in st.session_state:
    st.session_state["nombre"] = ""

if st.session_state["nombre"] == "":
    st.title("Dashboard Financiero - QuimQuinAgro")
    st.subheader("Con este tablero podrás conocer diferentes tipos de datos sobre la asociación")
    nombre = st.text_input("Ingresa tu nombre:")
    if st.button("Entrar"):
        if nombre.strip() != "":
            st.session_state["nombre"] = nombre.strip()
            st.rerun()
        else:
            st.warning("Por favor, escribe tu nombre antes de continuar.")
else:
    st.title(f"Bienvenido, {st.session_state['nombre']}")
    st.write("Selecciona la consulta que quieras investigar en el menú lateral.")
    
    # --- MENÚ LATERAL ---
    consulta = st.sidebar.radio(
        "Selecciona una consulta:",
        [
            "Totales de Ingresos y Egresos por Mes",
            "Top 10 egresos",
            "Ingresos por socio",
        ]
    )

    # --- Q1: Totales de Ingresos y Egresos por Mes ---
    if consulta == "Totales de Ingresos y Egresos por Mes":
        st.header("Totales de Ingresos y Egresos por Mes (Todas las Cajas 2020–2025)")

        with sqlite3.connect(DB_PATH) as conn:
            tablas = pd.read_sql_query(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'caja%';", conn
            )["name"].tolist()

        if not tablas:
            st.error("No se encontraron tablas tipo 'caja' en la base de datos.")
        else:
            subconsultas = []
            for t in tablas:
                with sqlite3.connect(DB_PATH) as conn:
                    cols = pd.read_sql_query(f"PRAGMA table_info({t});", conn)["name"].tolist()
                if "entrada" in cols and "salida" in cols:
                    subconsultas.append(f"SELECT fecha, entrada, salida FROM {t}")
                elif "prestamo" in cols and "abono" in cols:
                    subconsultas.append(f"SELECT fecha, abono AS entrada, prestamo AS salida FROM {t}")

            if not subconsultas:
                st.error("Ninguna tabla tiene columnas válidas para calcular ingresos y egresos.")
            else:
                union_query = " UNION ALL ".join(subconsultas)
                fecha_ini = st.date_input("Fecha inicial", pd.Timestamp("2020-01-01"))
                fecha_fin = st.date_input("Fecha final", pd.Timestamp("2025-12-31"))

                sql = f"""
                SELECT 
                    strftime('%Y-%m', fecha) AS mes,
                    SUM(entrada) AS ingresos,
                    SUM(salida) AS egresos
                FROM ({union_query})
                WHERE fecha BETWEEN ? AND ?
                GROUP BY mes
                ORDER BY mes;
                """
                df = ejecutar_sql(sql, (fecha_ini, fecha_fin))

                if df.empty:
                    st.warning("No se encontraron datos para el rango seleccionado.")
                else:
                    fig = px.bar(df, x="mes", y=["ingresos", "egresos"],
                                 barmode="group",
                                 title="Ingresos vs Egresos Mensuales (Todas las Cajas 2020–2025)")
                    st.plotly_chart(fig, use_container_width=True)

                    # --- Conclusión automática ---
                    total_ingresos = df["ingresos"].sum()
                    total_egresos = df["egresos"].sum()
                    balance = total_ingresos - total_egresos
                    st.subheader("Conclusión:")
                    if balance > 0:
                        st.write(f"Durante el periodo seleccionado, los ingresos totales superaron a los egresos, con un balance positivo de {balance:,.0f}. Esto refleja una buena gestión financiera.")
                    elif balance < 0:
                        st.write(f"En el periodo analizado, los egresos superaron a los ingresos, generando un déficit de {abs(balance):,.0f}. Se recomienda revisar los meses con mayores salidas.")
                    else:
                        st.write("Los ingresos y egresos fueron equivalentes, reflejando un equilibrio financiero en el periodo analizado.")

    # --- Q2: Top 10 egresos ---
    elif consulta == "Top 10 egresos":
        st.header("Top 10 Egresos - Todas las Cajas (2020–2025)")

        with sqlite3.connect(DB_PATH) as conn:
            tablas = pd.read_sql_query(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'caja%';", conn
            )["name"].tolist()

        if not tablas:
            st.error("No se encontraron tablas tipo 'caja' en la base de datos.")
        else:
            subconsultas = []
            for t in tablas:
                with sqlite3.connect(DB_PATH) as conn:
                    cols = pd.read_sql_query(f"PRAGMA table_info({t});", conn)["name"].tolist()
                if "detalle" in cols and "salida" in cols:
                    subconsultas.append(f"SELECT fecha, detalle, salida FROM {t}")
                elif "detalle" in cols and "prestamo" in cols:
                    subconsultas.append(f"SELECT fecha, detalle, prestamo AS salida FROM {t}")

            if not subconsultas:
                st.error("Ninguna tabla tiene columnas válidas para calcular egresos.")
            else:
                union_query = " UNION ALL ".join(subconsultas)
                fecha_ini = st.date_input("Fecha inicial", pd.Timestamp("2020-01-01"))
                fecha_fin = st.date_input("Fecha final", pd.Timestamp("2025-12-31"))

                sql = f"""
                SELECT detalle, SUM(salida) AS total_egreso
                FROM ({union_query})
                WHERE fecha BETWEEN ? AND ?
                GROUP BY detalle
                ORDER BY total_egreso DESC
                LIMIT 10;
                """
                df = ejecutar_sql(sql, (fecha_ini, fecha_fin))

                if df.empty:
                    st.warning("No se encontraron egresos en ese periodo.")
                else:
                    fig = px.bar(df, x="detalle", y="total_egreso",
                                 title="Top 10 Conceptos de Egreso (Todas las Cajas 2020–2025)",
                                 text_auto=True)
                    fig.update_layout(xaxis_title="Concepto", yaxis_title="Valor", xaxis_tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)

                    # --- Conclusión automática ---
                    st.subheader("Conclusión:")
                    top = df.iloc[0]
                    st.write(f"El egreso más representativo corresponde a **{top['detalle']}**, con un valor total de {top['total_egreso']:,.0f}. Este tipo de gasto tiene un impacto significativo en la estructura de costos y debería ser monitoreado de cerca.")

    # --- Q3: Ingresos por socio ---
    elif consulta == "Ingresos por socio":
        st.header("Ingresos por Socio (CXC)")

        fecha_ini = st.date_input("Fecha inicial", pd.Timestamp("2024-01-01"))
        fecha_fin = st.date_input("Fecha final", pd.Timestamp("2024-12-31"))

        socios_df = ejecutar_sql("SELECT DISTINCT socio FROM cxc2024 ORDER BY socio;")
        socios = ["Todos"] + socios_df["socio"].dropna().tolist()
        socio_sel = st.selectbox("Selecciona un socio:", socios)

        if socio_sel == "Todos":
            sql = """
            SELECT socio, SUM(entrada) AS ingresos
            FROM cxc2024
            WHERE fecha BETWEEN ? AND ?
            GROUP BY socio
            ORDER BY ingresos DESC;
            """
            df = ejecutar_sql(sql, (fecha_ini, fecha_fin))
            fig = px.bar(df, x="socio", y="ingresos", title="Ingresos Totales por Socio", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)

            if not df.empty:
                st.subheader("Conclusión:")
                top_socio = df.iloc[0]
                st.write(f"El socio con mayores ingresos en el periodo fue **{top_socio['socio']}**, con un total de {top_socio['ingresos']:,.0f}. Esto sugiere una alta participación en las operaciones de la asociación.")
        else:
            sql = """
            SELECT fecha, SUM(entrada) AS ingresos
            FROM cxc2024
            WHERE fecha BETWEEN ? AND ? AND socio = ?
            GROUP BY fecha
            ORDER BY fecha;
            """
            df = ejecutar_sql(sql, (fecha_ini, fecha_fin, socio_sel))
            fig = px.line(df, x="fecha", y="ingresos", title=f"Ingresos de {socio_sel} en el tiempo")
            st.plotly_chart(fig, use_container_width=True)

            if not df.empty:
                st.subheader("Conclusión:")
                st.write(f"El comportamiento de los ingresos de **{socio_sel}** muestra una tendencia estable a lo largo del tiempo, lo cual refleja un flujo constante de aportes o ventas.")


