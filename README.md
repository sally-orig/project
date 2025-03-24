--Wholesale Vegetable Prices Monitoring--

--Objective: 
1. This website is used to monitor daily vegetable prices.
2. Plots the price trend for each vegetable everyday.

--Intended Users: 
1. Farmers, Wholesalers of vegetables, Viewers - Monitor daily vegetable prices on certain market locations (e.g NVAT wholesale market)
   features:
      a. View vegetable details list
         a.1 Vegetable details list view (Vegetable name, image, price, last updated)
         a.2 Search by vegetable name

2. Admin - add, update, deactivate vegetable from list
   features:
      a. View vegetable details list
         a.1 Vegetable details list view (Vegetable name, image, price, last updated)
         a.2 Search by vegetable name
         a.3 Reset button for search bar
      b. Add New Vegetable Form
         b.1 Name - Should be unique (if in database, reactivate vegetable)
         b.2 Description
         b.3 Price - Should be greater then 0 (with validation)
         b.4 Image - uploaded by user (only accepts image files such as jpg, png)
         b.5 Save and Cancel buttons
      c. Update Vegetable Form
         c.1 Name and Image - not editable
         c.2 Description
         c.3 Price - Should be greater then 0 (with validation)
         c.4 Save and Cancel buttons
      d. Deactivate Vegetable
         d.1 Confimation prompt
      e. View Transaction Logs list
         e.1 Order by date created


--How to run website locally:
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
