# Analytica-assignment

Important Notes. 
" In the test_cases folder , there are three automation scripts being developed.
--------------

Launch PyCharm
Click File > Open
Select the Assignment-Analytica folder
----------
Go to File > Settings (Windows)
Navigate to Project: Assignment-Analytica > Python Interpreter
Click the gear icon > Add
Choose New Environment
Select Python 3.8 or newer
------------
Install Required Packages
Open the Terminal in PyCharm (bottom panel) and run:
"pip install selenium pytest webdriver-manager"
-----------
To run the script , use these commands
pytest test_product.py -s
pytest test_product.py --html=report.html --capture=tee-sys
----------

