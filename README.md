# Wholesale Vegetable Prices Monitoring


## Objective: 
1. This website is used to monitor daily vegetable prices.
2. Plots the price trend for each vegetable everyday.

## Intended Users: 
1. Farmers, Wholesalers of vegetables, Viewers - Monitor daily vegetable prices on certain market locations (e.g NVAT wholesale market)
   features:
      *  View vegetable details list
         * Vegetable details list view (Vegetable name, image, price, last updated)
         * Search by vegetable name

2. Admin - add, update, deactivate vegetable from list
   features:
      * View vegetable details list
         * Vegetable details list view (Vegetable name, image, price, last updated)
         * Search by vegetable name
         * Reset button for search bar
      * Add New Vegetable Form
         * Name - Should be unique (if in database, reactivate vegetable)
         * Description
         * Price - Should be greater then 0 (with validation)
         * Image - uploaded by user (only accepts image files such as jpg, png)
         * Save and Cancel buttons
      * Update Vegetable Form
         * Name and Image - not editable
         * Description
         * Price - Should be greater then 0 (with validation)
         * Save and Cancel buttons
      * Deactivate Vegetable
         * Confimation prompt
      * View Transaction Logs list
         * Order by date created


## How to run website locally:
1. Install Python 3.13.0
2. Install Pip 24.2
3. Create Virtual Environment (PythonTesting) --python -m venv PythonProject
4. Activate Venv (using git bash) --source PythonTesting/Scripts/activate *Activate using cmd or powershell --Scripts/activate
5. Clone remote repository to your local computer with folder name: Exercise2 
--git clone https://github.com/sally-orig/project.git project
6. Install additional extensions using requirements.txt
--pip install -r requirements.txt
7. Go to project/VegiePriceMonitoring
--cd PythonProject/project/VegiePriceMonitoring
8. Run server and open to browser
--py manage.py runserver
