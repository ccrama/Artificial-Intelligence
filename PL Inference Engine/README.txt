Name: Arnav Garg
ID: 1001039593
Class: CSE 4308-001

Programming Language Used: Python 2.4.3 (Omega version)
--------------------------

----------------
CODE STRUCTURE
-----------------

All the functions for tt_entails algorithm are in the logical_expression.py file. For more details, read below.

check_true_false.py
--------------------
contains the functions:
	1) Main
		converts the input string into expression and passes the function to the check_true_false function. 
		NOTE: for optimization, while creating the expression, if the expression consists of only a symbol (or not of that symbol), that symbol is directly put into the models dictionary. 

	2) check_true_false:
		This function extracts all the symbols from the KB and the statment, creates a model expanding on the model_dictioanry created in the previous function and calles the TT-ENTAILS function described in the logical_expression.py file twice, once for statement, and the other for not_statement and then compares the boolean value for both the calls for the appropriate answer. 

logical_expression.py
----------------------
contains the class:
	1) logical_expression:
		stores all the expression variables and instances.

contains the function (to which I made changes or created) :
	1) extract_symbols:
		extracts all the symbols from the expression
	2) tt_check_all:
		performs the tt_check_all algorithm
	3) pl_true:
		performs the pl_true algorithm
	4) extend model:
		A function needed for when performing the tt_check_all


--------------------
HOW TO RUN THE CODE
--------------------

Command
-------
python check_true_false.py wumpus_rules.txt [addn_knowledge_file] [statement_file]

NOTE
----
The wumpus_rules.txt should be in the same directory for the above command 
