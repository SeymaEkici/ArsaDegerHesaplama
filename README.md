# Land Value Calculator

This application calculates the value changes of land investments over time, comparing purchase and sale values across multiple currencies (TRY, USD, EUR) and gold.

## Project Overview

This application helps users calculate how their land investment has performed over time. It compares the purchase and sale values in Turkish Lira and also converts them to equivalent values in USD, EUR, and gold, providing percentage changes to show real investment performance.

## Key Features

- Calculate land value changes between purchase and sale dates
- Convert values to USD, EUR, and gold for true investment performance
- Calculate per square meter pricing
- Show percentage changes in various currencies

## File Structure

- **main.py**: The main GUI application entry point
- **calculator.py**: Core calculation logic for land value comparisons
- **currency.py**: Currency rate fetching from Excel data source (to be modified)
- **design.py**: UI styling and component creation utilities
- **gui_utils.py**: Additional GUI helper functions
- **update_excel.py**: Script to update the exchange rate data from online sources

## How It Works

1. User enters purchase and sale information (date, price, area)
2. Application fetches currency rates from an Excel file for the relevant dates
3. Values are calculated in multiple currencies and compared
4. Results show the real change in value accounting for currency fluctuations

## Currency Data Source

The application currently reads currency and gold rates from an Excel file. The currency.py file will be modified to use a different API for fetching this data.

## Future Improvements

- Replace Excel-based currency rates with API data
- Add graph visualization of value changes
- Support additional currencies and investment metrics

## Usage

Run the application by executing:
```
python main.py
```
