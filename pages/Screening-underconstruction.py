import pandas as pd
import streamlit as st
import plotly.express as px

# Main function to calculate scores and display results
def main():
    st.set_page_config(page_title='Ticker Scores')
    st.header("Ticker Scores")

    # Load the CSV file
    csv_file = 'Streamlit/software.csv'  # Path to your CSV file
    df = pd.read_csv(csv_file)

    # Remove leading and trailing whitespaces from column names
    df.columns = df.columns.str.strip()

    # Create input fields for each column multiplier
    columns_to_multiply = [
        'Organic growth', 'EBITDA growth', 'Sales est change- 4 months',
        'EBITDA est change', 'Gross margin', 'EBITDA margin',
        'Sales to EV', 'EBITDA to EV', 'price target change -4 months'
    ]

    # Initialize default multipliers and input values
    default_multipliers = {column: 1.0 for column in columns_to_multiply}
    if 'multipliers' not in st.session_state:
        st.session_state.multipliers = default_multipliers.copy()
        st.session_state.input_values = pd.DataFrame({'Column': columns_to_multiply, 'Multiplier': [default_multipliers.get(col, 1.0) for col in columns_to_multiply]})

    # Display editable table for multipliers
    st.subheader("Edit Multipliers:")
    edited_multipliers = st.data_editor(st.session_state.input_values)
    st.session_state.input_values = edited_multipliers

    # Apply multipliers to the DataFrame
    for _, row in edited_multipliers.iterrows():
        column = row['Column']
        multiplier = row['Multiplier']
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

    # Display the bar chart for scores with a reversed sequential green color scale
    st.subheader("Bar Chart for Scores (Sequential Greens - Darker on Left)")
    fig = px.bar(sorted_ticker_scores, x='Ticker', y='Score', color='Score', labels={'Score': 'Average Score'},
                 color_continuous_scale=colorscale)
    fig.update_layout(xaxis_title="Ticker", yaxis_title="Average Score")
    st.plotly_chart(fig)

    # Display the data from the CSV file at the bottom
    st.subheader("
