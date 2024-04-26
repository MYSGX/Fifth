import pandas as pd
import streamlit as st
import plotly.express as px

# Load the CSV file
csv_file = 'Streamlit/modelscores.csv'  # Path to your CSV file
df = pd.read_csv(csv_file)

# Remove leading/trailing whitespace from column names
df.columns = df.columns.str.strip()

# Create a new column with ticker and company name
df['Ticker_Name'] = df['Ticker'] + ' - ' + df['Name']

# Define the columns for the table excluding 'Score'
columns_to_sort = [
    'Organic growth',
    'EBITDA growth',
    'Sales est change- 4 months',
    'EBITDA est change',
    'Gross margin',
    'EBITDA margin',
    'Sales to EV',
    'EBITDA to EV',
    'Earnings yield',
    'Price target change -4 months'  # Capitalize the 'p'
]

# Define the columns for the bar chart
columns_for_bar_chart = [
    'Organic growth',
    'EBITDA growth',
    'Sales est change- 4 months',
    'EBITDA est change',
    'Gross margin',
    'EBITDA margin',
    'Sales to EV',
    'EBITDA to EV',
    'Earnings yield',
    'Price target change -4 months'  # Capitalize the 'p'
]

# Set page layout to wide
st.set_page_config(layout="wide")

# Create dropdown input for ticker
ticker_input = st.selectbox("Select Ticker", sorted(df['Ticker_Name'].unique()))

# Extract ticker from the selected value
selected_ticker = ticker_input.split(' - ')[0]

# Check if ticker is valid and display corresponding values
if selected_ticker:
    ticker_data = df[df['Ticker'] == selected_ticker.upper()]  # Filter data for the selected ticker
    if not ticker_data.empty:
        # Display 'Score' in its own table
        st.write("### Score:")
        score_data = ticker_data[['Score']].transpose()
        score_data.columns = [selected_ticker.upper()]
        st.write(score_data)
        
        # Separate and sort specified columns for the table
        separated_data = ticker_data[columns_to_sort].transpose()
        separated_data.columns = [selected_ticker.upper()]
        separated_data_sorted = separated_data.sort_values(by=selected_ticker.upper(), axis=0)
        
        # Filter out empty rows
        separated_data_sorted = separated_data_sorted.dropna(how='all')
        
        # Create two columns layout
        col1, col2 = st.columns([2, 3])  # Adjust the column widths as needed
        
        # Add content to the first column (sorted table)
        with col1:
            st.write("### Sorted Ticker Data:")
            st.write(separated_data_sorted)
        
        # Add content to the second column (bar chart)
        with col2:
            # Create a bar chart for the specified columns
            st.write("### Bar Chart:")
            bar_data = ticker_data[columns_for_bar_chart].transpose().reset_index()
            bar_data.columns = ['Metric', 'Value']
            
            # Define custom color scale for the bar chart
            colorscale = [
                (0, 'green'),  # Lower values (green)
                (0.5, 'yellow'),  # Middle values (yellow)
                (1, 'red')  # Higher values (red)
            ]
            
            fig = px.bar(bar_data, x='Metric', y='Value', labels={'Value': 'Metric Value'}, color='Value',
                         color_continuous_scale=colorscale)
            st.plotly_chart(fig, use_container_width=True)
        
        # Display data for name, sector, industry, and market cap
        st.write("### Company Information:")
        company_info = ticker_data[['Name', 'Sector', 'Industry', 'Market cap']].transpose()
        st.write(company_info)
        
    else:
        st.write("Ticker not found!")
