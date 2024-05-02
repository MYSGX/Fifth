import pandas as pd
import streamlit as st
import plotly.express as px

# Load the CSV files
csv_file_factors = 'Factors4-26-2024.csv'  # Path to your Factors CSV file
csv_file_cor = 'Cor4-30-24.csv'  # Path to your Correlation CSV file

# Read both CSV files
df_factors = pd.read_csv(csv_file_factors)
df_cor = pd.read_csv(csv_file_cor)

# Remove leading/trailing whitespace from column names in both dataframes
df_factors.columns = df_factors.columns.str.strip()
df_cor.columns = df_cor.columns.str.strip()

# Set page layout to wide
st.set_page_config(layout="wide")

# Create dropdown input for ticker
ticker_input = st.selectbox("Select Ticker", sorted(df_factors[['Ticker', 'Name']].astype(str).apply(lambda x: f"{x['Ticker']} - {x['Name']}", axis=1).unique()))

# Extract ticker and name from the selected value
selected_ticker = ticker_input.split(' - ')[0]
selected_name = ticker_input.split(' - ')[1]

# Check if ticker is valid and display corresponding values
if selected_ticker:
    # Filter data for the selected ticker from Factors data
    ticker_data_factors = df_factors[df_factors['Ticker'] == selected_ticker.upper()]  
    if not ticker_data_factors.empty:
        # Display data for selected ticker from Factors data
        st.write("### Company Information:")
        company_info = ticker_data_factors[['Ticker', 'Name', 'Sector', 'Industry']].transpose()
        st.write(company_info)

        # Convert factors data to numeric
        factors_data_factors = ticker_data_factors[['Growth', 'Value', 'Price Momentum', 'Estimates', 'Profitability',
                                                    'Stability', 'Low Beta', 'Cyclicality', 'Liquidity', 'Size']]
        factors_data_factors = factors_data_factors.apply(pd.to_numeric, errors='coerce')

        # Create a bar chart for the factors from Factors data
        st.write("### Bar Chart (Factors):")
        factors_data_factors = factors_data_factors.transpose().reset_index()
        factors_data_factors.columns = ['Factor', 'Value']

        # Define custom color scale for the bar chart from Factors data
        colorscale = [
            (0, 'red'),  # Lower bound (0) - red
            (0.5, 'yellow'),  # Middle value (0.5) - yellow
            (1, 'green')  # Upper bound (1) - green
        ]

        fig_factors = px.bar(factors_data_factors, x='Factor', y='Value', labels={'Value': 'Factor Value'}, color='Value',
                             color_continuous_scale=colorscale, range_color=(-3, 3))

        # Display the Plotly chart for Factors data
        st.plotly_chart(fig_factors)

        # Display top and bottom twenty factors tables for Correlation data
        st.write("### Top and Bottom Twenty Factors (Correlation):")
        ticker_data_cor = df_cor[df_cor['Ticker'] == selected_ticker.upper()]  
        if not ticker_data_cor.empty:
            # Convert data to numeric
            factors_data_cor = ticker_data_cor.drop(columns=['Ticker', 'Name', 'Sector', 'Industry'])  
            factors_data_cor = factors_data_cor.apply(pd.to_numeric, errors='coerce')  

            # Compute mean values for factors
            factors_mean_cor = factors_data_cor.mean()  

            # Concatenate top and bottom twenty factors
            top_bottom_twenty_mean_cor = pd.concat([factors_mean_cor.nlargest(20), factors_mean_cor.nsmallest(20)])  

            # Color the top twenty values green and bottom twenty values red
            def color_negative_red(val):
                color = 'red' if val in top_bottom_twenty_mean_cor.nsmallest(20).values else 'green'
                return 'color: %s' % color

            top_table_cor = top_bottom_twenty_mean_cor.nlargest(20).to_frame().reset_index()
            top_table_cor.columns = ['Factor', 'Value']
            top_table_cor = top_table_cor.style.applymap(color_negative_red, subset=['Value'])

            bottom_table_cor = top_bottom_twenty_mean_cor.nsmallest(20).to_frame().reset_index()
            bottom_table_cor.columns = ['Factor', 'Value']
            bottom_table_cor = bottom_table_cor.iloc[::-1].style.applymap(color_negative_red, subset=['Value'])  

            # Display tables side by side with narrower width
            col1_cor, col2_cor = st.columns(2)
            with col1_cor:
                st.write("#### Top Twenty Factors:")
                st.table(top_table_cor)  
            with col2_cor:
                st.write("#### Bottom Twenty Factors:")
                st.table(bottom_table_cor)  

            # Create a bar chart for top and bottom twenty factors for Correlation data
            st.write("### Bar Chart (Correlation):")
            top_bottom_twenty_mean_df = top_bottom_twenty_mean_cor.reset_index()
            top_bottom_twenty_mean_df.columns = ['Factor', 'Value']
            top_bottom_twenty_mean_df['Color'] = top_bottom_twenty_mean_df['Value'].apply(lambda x: 'red' if x in top_bottom_twenty_mean_cor.nsmallest(20).values else 'green')
            fig_cor = px.bar(top_bottom_twenty_mean_df, x='Factor', y='Value', color='Color',
                             labels={'Value': 'Factor Value'}, title=f'Top and Bottom Twenty Factors for {selected_name}',
                             color_discrete_map={'red': 'red', 'green': 'green'})
            fig_cor.update_layout(showlegend=False)  # Hide legend
            st.plotly_chart(fig_cor)
