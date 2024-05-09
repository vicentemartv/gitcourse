import streamlit as st
import plotly.graph_objects as go
from reportes import generar_reporte


def main():
    # Configuración del layout del aplicativo a modo wide
    st.set_page_config(layout="wide")

    st.title("Reportes de Manufactura")

    # Definir diccionario de reportes disponibles con ID
    reportes_disponibles = {
        "Utilización report": "ID_reporte_1",
    }

    # Usar st.session_state para mantener el estado entre recargas
    if 'data' not in st.session_state:
        st.session_state.data = None

    # Selección de reporte y fechas en sidebar
    with st.sidebar:
        reporte_seleccionado = st.selectbox(
            "Seleccione el reporte deseado:", list(reportes_disponibles.keys()))
        start_date = st.date_input("Seleccione la fecha de inicio:")
        end_date = st.date_input("Seleccione la fecha de fin:")
        submitted = st.button("Generar Reporte")

    if submitted:
        st.session_state.data = generar_reporte(
            reportes_disponibles[reporte_seleccionado], start_date, end_date)

    if st.session_state.data is not None:
        # Trabajar con una copia para no alterar los datos originales
        data = st.session_state.data.copy()

        # Filtros dinámicos en sidebar con dependencias
        with st.sidebar:
            unique_days = ["All"] + sorted(data['day'].unique().tolist())
            selected_day = st.selectbox(
                "Select Day", options=unique_days, index=0)

            if selected_day != "All":
                data = data[data['day'] == selected_day]

            unique_machine_groups = ["All"] + \
                sorted(data['machineGroup'].unique().tolist())
            selected_machine_group = st.selectbox(
                "Select Machine Group", options=unique_machine_groups, index=0)

            if selected_machine_group != "All":
                data = data[data['machineGroup'] == selected_machine_group]

            unique_machines = ["All"] + \
                sorted(data['machine'].unique().tolist())
            selected_machine = st.selectbox(
                "Select Machine", options=unique_machines, index=0)

            if selected_machine != "All":
                data = data[data['machine'] == selected_machine]

            unique_shifts = ["All"] + sorted(data['shift'].unique().tolist())
            selected_shift = st.selectbox(
                "Select Shift", options=unique_shifts, index=0)

            if selected_shift != "All":
                data = data[data['shift'] == selected_shift]

        # Línea divisoria
        st.markdown("<hr>", unsafe_allow_html=True)

        # Cálculo de la tasa de utilización
        total_time_in_cycle = data['timeInCycle'].sum()
        total_all_time = data['allTime'].sum()
        utilization_rate = (total_time_in_cycle /
                            total_all_time) * 100 if total_all_time > 0 else 0

        # Visualización de tarjetas de métricas con estilo mejorado
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Time in Cycle",
                    f"{int(total_time_in_cycle):,} hours", delta_color="off")
        col2.metric("Total All Time",
                    f"{int(total_all_time):,} hours", delta_color="off")
        col3.metric("Average Utilization Rate",
                    f"{utilization_rate:.0f}%", delta_color="off")

        # Crear gráfico de barras usando todo el ancho disponible
        fig = go.Figure()
        fig.add_trace(
            go.Bar(x=data['date'], y=data['timeInCycle'], name="Time in Cycle"))
        fig.add_trace(
            go.Bar(x=data['date'], y=data['allTime'], name="All Time"))

        # Configuración del layout del gráfico
        # Utilizar todo el ancho disponible
        fig.update_layout(barmode='group', width=1200)

        # Ajustar el gráfico al ancho del contenedor
        st.plotly_chart(fig, use_container_width=True)

        # Botón para descargar el reporte completo
        csv = data.to_csv(index=False)
        st.download_button(label="Descargar Reporte Completo",
                           data=csv, file_name="reporte.csv", mime="text/csv")
    else:
        st.error(
            "No se pudo generar el reporte. Por favor, intente nuevamente o genere un nuevo reporte.")


if __name__ == "__main__":
    main()
