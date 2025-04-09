# Wholesale Vegetable Prices Monitoring


## Fix: 
1. Modify 'Transaction' model to 'VegetableAction'
2. Change 'Delete Vegetable' to 'Deactivate Vegetable' button label and icon
3. Add tooltip for Add, Update and Deactivate buttons


## Added Feature:
* Viewer, Admin
   1. Key Performance Indicator (KPI)
      - Highest price with date updated
      - Lowest price with date updated
   1. Price Chart view - Plot Date vs Average Price for each vegetable in a line chart (Daily)
      - x-axis: Date Updated
      - y-axis: Average Price (PHP / Kilo)
      - Dropdown Filter: Vegetable Name
