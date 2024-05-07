import os
import streamlit as st
import yaml

st.set_page_config(
    layout='wide',
    page_title='DIIP',
    page_icon='https://github.com/programmingwithclaudio/nextjs-tailwindcss-blog/blob/main/public/favicon-16x16.png?raw=true',
    initial_sidebar_state='expanded',
)

def load_activities(filepath):
    with open(filepath, 'r') as file:
        activities = yaml.safe_load(file)
    return activities

def run():
    working_directory = os.path.dirname(os.path.abspath(__file__))    

    LOGO_SIDEBAR_URL = "https://github.com/programmingwithclaudio/MVP_ML_TransporteNY/blob/main/public/hd.jpg?raw=true"

    if LOGO_SIDEBAR_URL: 
        st.sidebar.image(
            LOGO_SIDEBAR_URL,             
            caption='DATA-DIIP'
        )

    # Load the available activities from YAML
    ACTIVITIES_FILEPATH = os.path.join(working_directory, "app_activities.yaml")
    activities = load_activities(ACTIVITIES_FILEPATH)
    
    # Display the activity menu
    selected_activity = st.sidebar.selectbox('Activities', [activity['name'] for activity in activities])
    
    # Load the selected activity
    selected_activity_url = [activity['url'] for activity in activities if activity['name'] == selected_activity][0]
    selected_activity_filepath = os.path.join(working_directory, "activities", selected_activity_url)
    
    # Run the selected activity
    with open(selected_activity_filepath, 'r') as file:
        code = file.read()
    exec(code)

if __name__ == '__main__':
    run()
else:
    st.error('The app failed initialization. Report issue to mantainers in github')
