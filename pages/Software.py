import pandas as pd
import streamlit as st
import plotly.express as px

# Function to display inputs in a table
def display_inputs_in_table(columns_to_multiply, multipliers):
    st.sidebar.subheader("Multipliers for each column:")
    df_inputs = pd.DataFrame({'Column': columns_to_multiply, 'Multiplier': [multipliers.get(col, 1.0) for col in columns_to_multiply]})
    st.sidebar.table(df_inputs)

# Function to reset multipliers to default values
def reset_multipliers(default_multipliers):
    st.session_state.input_values = default_multipliers.copy()

# Main function to calculate scores and display results
def main():
    st.set_page_config(page_title='Ticker Scores')
    st.header("Ticker Scores")

    # Load the CSV file
    csv_file = 'software.csv'  # Path to your CSV file
    df = pd.read_csv(csv_file)

    # Remove leading and trailing whitespaces from column names
    df.columns = df.columns.str.strip()

    # Create input fields for each column multiplier in sidebar
    columns_to_multiply = [
        'Organic growth', 'EBITDA growth', 'Sales est change- 4 months',
        'EBITDA est change', 'Gross margin', 'EBITDA margin',
        'Sales to EV', 'EBITDA to EV', 'price target change -4 months'
    ]

    # Initialize default multipliers and input values
    default_multipliers = {column: 1.0 for column in columns_to_multiply}
    if 'multipliers' not in st.session_state:
        st.session_state.multipliers = default_multipliers
        st.session_state.input_values = default_multipliers.copy()

    # Reset multipliers if requested
    reset_button = st.sidebar.button("Reset Multipliers")
    if reset_button:
        reset_multipliers(default_multipliers)
        st.experimental_rerun()

    # Display input fields for multipliers
    st.sidebar.subheader("Please input multipliers for each column:")
    for column in columns_to_multiply:
        default_multiplier = st.session_state.input_values.get(column, 1.0)
        st.session_state.input_values[column] = st.sidebar.number_input(f"{column}", min_value=0.0, step=0.1, value=default_multiplier, key=column)

    # Apply multipliers to the DataFrame
    for column, multiplier in st.session_state.input_values.items():
        df[column] = df[column] * multiplier

    # Calculate the average score for each ticker
    df['Score'] = df[columns_to_multiply].mean(axis=1)

    # Define colors for scores
    colorscale = [
        [0, 'green'],
        [0.5, 'yellow'],
        [1, 'red']
    ]

    # Display average scores for each ticker and sort them from lowest to highest
    ticker_scores = df[['Ticker', 'Name', 'Sector', 'Score']].groupby(['Ticker', 'Name', 'Sector']).mean().reset_index()
    sorted_ticker_scores = ticker_scores.sort_values(by='Score', ascending=True)
    st.subheader("Lower scores better")
    st.write(sorted_ticker_scores)

    # Display inputs in a table in the sidebar
    display_inputs_in_table(columns_to_multiply, st.session_state.input_values)

    # Display the bar chart for scores with a reversed sequential green color scale
    st.subheader("Bar Chart for Scores (Sequential Greens - Darker on Left)")
    fig = px.bar(sorted_ticker_scores, x='Ticker', y='Score', color='Score', labels={'Score': 'Average Score'},
                 color_continuous_scale=colorscale)
    fig.update_layout(xaxis_title="Ticker", yaxis_title="Average Score")
    st.plotly_chart(fig)

    # Display the data from the CSV file at the bottom
    st.subheader("Data:")
    st.write(df)

if __name__ == "__main__":
    main()
