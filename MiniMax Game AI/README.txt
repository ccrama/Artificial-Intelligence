Name: Arnav Garg
ID: 1001039593
Class: CSE 4308 - 001

=== I WOULD LIKE TO PARTICIPATE IN THE TOURNAMENT. ==

------------------------------
ABOUT THE CODE
------------------------------

The minimax depth-limited alpha-beta pruning is in the AiPlayer.java file. 
The state of the gameboard is in the file GameBoard.java

The main function of the code is in maxconnect4.java

The interactive mode will create and store the state of the board after AI plays in the computer.txt file and the state after the human
plays in the human.txt file.

In one-move mode, the code will create an output.txt file if one is not created already.

-----------------------------
COMMAND TO RUN THE CODE
-----------------------------

COMPILE
--------
javac AiPlayer.java GameBoard.java maxconnect4.java

THEN -->

INTERACTIVE MODE
------------------
java MaxConnectFour interactive [ input_file ] [ computer-next / human-next ] [ search depth]

ONE-MOVE MODE
---------------
java maxConnectFour.MaxConnectFour one-move [ input_file ] [ output_file ] [ search depth]