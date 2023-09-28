import pandas as pd
import streamlit as st
import chardet
import datetime
import base64

def process_file(file):
    try:
        global df
        file_encoding = chardet.detect(file.read())["encoding"]
        file.seek(0)

        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file, engine='openpyxl')
        elif file.name.endswith('.csv'):
            df = pd.read_csv(file, encoding=file_encoding)

        # Here you can add more processing steps as needed
        df = df[df['Country'] != 'South Africa']  # Example: remove rows where Country is South Africa

        st.success("File processed successfully. Now you can filter the race types below.")
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")


def display_race_type_data():
    try:
        # Create a new column 'Race Type' and initialize it as empty
        df['Race Type'] = ''

        # Determine which race names are in the DataFrame
        current_race_names = df['Race Name'].unique()

        # Calculate the intersection of all possible race types and the current race names
        intersect_race_types = [race_type for race_type in race_types if
                                any(race_type in race_name for race_name in current_race_names)]

        selected_race_types = st.multiselect('Select Race Types', intersect_race_types,
                                             default=intersect_race_types)

        if selected_race_types:
            # Update the 'Race Type' column for matching race names
            for race_type in selected_race_types:
                df.loc[df['Race Name'].str.contains(race_type), 'Race Type'] = race_type

            # Filter the DataFrame based on selected race types
            df_filtered = df[df['Race Type'].isin(selected_race_types)]

            if len(df_filtered) > 0:
                # Sort the filtered DataFrame by 'Time' column in ascending order
                df_filtered = df_filtered.sort_values(by='Time')

                # Display the DataFrame of races matching the selected race types
                st.write("Races:")
                st.dataframe(df_filtered)
            else:
                st.write("No races found for the selected race types.")

            # Download link for CSV
            csv = df_filtered.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:text/csv;charset=utf-8;base64,{b64}" download="filtered_data.csv">Download Filtered Data as CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

        else:
            st.write("Please select race types.")

    except Exception as e:
        st.error(f"An error occurred: {e}")


def main():
    st.title("Race Data Processor")

    # File uploader
    uploaded_file = st.file_uploader("Upload Excel or CSV File", type=['xlsx', 'csv'])

    if uploaded_file:
        if st.button("Process File"):
            process_file(uploaded_file)
            display_race_type_data()


if __name__ == "__main__":
    race_types = [
        'Selling Stakes',
        'Claiming Stakes',
        'Selling Handicap',
        'Nursery',
        'Maiden',
        'Amateur',
        'Group 1',
        'Group 2',
        'Group 3',
        'Other Handicap',
        'Classified Stakes',
        'Conditions Stakes',
        'Novice Stakes',
        'NH Flat',
        'Novice Hcap Hurdle',
        'Novice Hcap Chase',
        'Hunters Chase',
        'Handicap Hurdle',
        'Novice Hurdle',
        'Handicap Chase',
        'Novice Chase',
        'Listed',
        'Selling Hurdle',
        'Other Chase',
        'Other Hurdle',
        'Unclassified'
    ]

    main()
