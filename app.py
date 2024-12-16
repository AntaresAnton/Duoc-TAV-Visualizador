import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import io
import base64

def load_schedule():
    df = pd.read_csv('horarios.csv', sep=';')
    return df

def create_schedule_table(filtered_df):
    st.markdown("""
        <style>
        .schedule-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background-color: white;
            color: black;
        }
        .schedule-table th {
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: center;
            border: 1px solid #ddd;
        }
        .schedule-table td {
            padding: 12px;
            text-align: center;
            border: 1px solid #ddd;
            background-color: white;
            color: black;
        }
        .schedule-table td.empty {
            background-color: #f9f9f9;
        }
        .class-block {
            background-color: #e3f2fd;
            padding: 5px;
            border-radius: 4px;
            margin: 2px;
            font-size: 0.9em;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

    time_slots = [f"{i:02d}:00 - {i+1:02d}:00" for i in range(8, 21)]
    days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    schedule = {day: {time: [] for time in time_slots} for day in days}
    day_map = {'Lu': 'Lunes', 'Ma': 'Martes', 'Mi': 'Miércoles', 'Ju': 'Jueves', 'Vi': 'Viernes'}
    
    for _, row in filtered_df.iterrows():
        horario = row['Horario']
        dia_abrev = horario.split()[0]
        dia = day_map.get(dia_abrev, dia_abrev)
        start_time = horario.split(' - ')[0].split()[1]
        
        for time_slot in time_slots:
            slot_start = time_slot.split(' - ')[0]
            if start_time.startswith(slot_start.split(':')[0]):
                schedule[dia][time_slot].append(
                    f"<div class='class-block'>{row['Asignatura']}<br>Sala: {row['Sala']}</div>"
                )

    table_html = "<table class='schedule-table'>"
    table_html += "<tr><th>Hora</th>"
    for day in days:
        table_html += f"<th>{day}</th>"
    table_html += "</tr>"

    for time_slot in time_slots:
        table_html += f"<tr><td>{time_slot}</td>"
        for day in days:
            if schedule[day][time_slot]:
                table_html += f"<td>{''.join(schedule[day][time_slot])}</td>"
            else:
                table_html += "<td class='empty'></td>"
        table_html += "</tr>"
    
    table_html += "</table>"
    
    return table_html


def add_download_button():
    st.markdown("""
        <style>
        .download-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 20px;
        }
        </style>
        <button class="download-button" onclick="window.print()">
            📸 Descargar Horario
        </button>
    """, unsafe_allow_html=True)


def main():
    st.set_page_config(layout="wide")
    st.title('Horario Semanal')
    
    df = load_schedule()
    
    col1, col2 = st.columns([1, 2])
    with col1:
        carrera = st.selectbox('Carrera:', df['Carrera'].unique())
        filtered_subjects = df[df['Carrera'] == carrera]['Asignatura'].unique()
        selected_subjects = st.multiselect('Asignaturas:', filtered_subjects)
    
    if selected_subjects:
        filtered_df = df[
            (df['Carrera'] == carrera) & 
            (df['Asignatura'].isin(selected_subjects))
        ]
        
        schedule_html = create_schedule_table(filtered_df)
        st.markdown(schedule_html, unsafe_allow_html=True)
        
        # Add download button
        add_download_button()
        
        st.markdown("### Información Detallada")
        for subject in selected_subjects:
            subject_info = filtered_df[filtered_df['Asignatura'] == subject].iloc[0]
            st.markdown(f"""
            <div style='background-color: white; padding: 1rem; border-radius: 5px; margin: 0.5rem 0;'>
                <h4 style='color: #212529; margin: 0;'>{subject}</h4>
                <p style='color: #495057; margin: 0.5rem 0;'>
                    👨‍🏫 <b>Profesor:</b> {subject_info['Docente']}<br>
                    🏫 <b>Sala:</b> {subject_info['Sala']}<br>
                    📝 <b>Sección:</b> {subject_info['Sección']}
                </p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()