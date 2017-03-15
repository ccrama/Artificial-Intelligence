import java.util.*;

/*
 * @author: Arnav Garg
 * @class: CSE 4308-001
 *
 */

public class AiPlayer 
{
    /**
     * The constructor essentially does nothing except instantiate an
     * AiPlayer object.
     *
     */

    public AiPlayer() 
    {
    }

    /**
     * This method plays a piece randomly on the board
     * @param currentGame The GameBoard object that is currently being used to
     * play the game.
     * @return an integer indicating which column the AiPlayer would like
     * to play in.
     */
    public int findBestPlay( GameBoard currentGame ) 
    {
	// start random play code
	Random randy = new Random();
	int playChoice = 99;
	
	playChoice = randy.nextInt( 7 );
	
	while( !currentGame.isValidPlay( playChoice ) )
	    playChoice = randy.nextInt( 7 );
	
	// end random play code
	
	return playChoice;
    }

    // The function plays the move based on Mini-Max algorithm with Alpha-Beta Pruning.
    // @params: GameBoard: The board the players are playing.
    // @params: depth: Maximum depth we want the code to go to.
    public int alphaBetaDecision(GameBoard gameBoard, int depth) {

        // The action that the player will play
        int action = 0; 
        // The various utility values.
        double utilityValue = 0;
        // The maximum utility out of all the moves.
        double maxUtility = -10;
        // Keeping track of the current depth for the recursion.
        int currentDepth = 0;

        // Getting the current player.
        int ai = gameBoard.getCurrentTurn();

        // Going over the possible moves.
        for (int i = 0; i < 7; i++) {

            // Checking for the move -> if valid or not.
            if (gameBoard.isValidPlay(i)) {

                GameBoard newGameBoard = new GameBoard(gameBoard.getGameBoard());
                newGameBoard.playPiece(i);

                // Mini-Max recursion.
                utilityValue = MinValue(newGameBoard, -10, 10, currentDepth, depth, ai);

                // System.out.println("Utility: " + utilityValue);

                // Finding the max utility.
                if (utilityValue >= maxUtility) {
                    maxUtility = utilityValue;
                    action = i;
                }
            }
        }

        //returning the action.
        return action;
    }

    public double MaxValue(GameBoard gameBoard, double alpha, double beta, int currentDepth, int depth, int ai) {


        currentDepth++;

        if (!(gameBoard.getPieceCount() < 42 || currentDepth == depth)) {

            return evaluateUtility(gameBoard, ai);

            // return (gameBoard.getScore(ai) - gameBoard.getScore(3-ai));
        }

        double v = -10;

        for (int i = 0; i < 7; i++) {

            if (gameBoard.isValidPlay(i)) {
                GameBoard newGameBoard = new GameBoard(gameBoard.getGameBoard());
                newGameBoard.playPiece(i);

                v = Math.max(v, MinValue(newGameBoard, alpha, beta, currentDepth, depth, ai));

                if (v >= beta) {
                    return v;
                }

                alpha = Max(alpha, v);
            }
        }

        return v;
    }

    public double MinValue(GameBoard gameBoard, double alpha, double beta, int currentDepth, int depth, int ai) {

        currentDepth++;

        if (gameBoard.getPieceCount() >= 42 || currentDepth >= depth) {

            return evaluateUtility(gameBoard, ai);

            // return (gameBoard.getScore(ai) - gameBoard.getScore(3-ai));
        }

        double v = 10;

        for (int i = 0; i < 7; i++) {

            if (gameBoard.isValidPlay(i)) {

                GameBoard newGameBoard = new GameBoard(gameBoard.getGameBoard());
                newGameBoard.playPiece(i);

                v = Math.min(v, MaxValue(newGameBoard, alpha, beta, currentDepth, depth, ai));

                if (v <= alpha) {
                    return v;
                }

                beta = Min(beta, v);
            }
        }

        return v;
    } 

    public double evaluateUtility(GameBoard gameBoard, int ai) {

        // This is the final utility.
        double utility = 0;

        double score = ( (double) gameBoard.getScore(ai) - (double) gameBoard.getScore(3-ai) );

        utility = score*100;

        utility += evaluateUtilityHelper(gameBoard, ai);

        

        return utility;

    }

    public double evaluateUtilityHelper(GameBoard gameBoard, int ai) {

        int totalPlaysNeeded = 0;
        int totalPossibilities = 0;

        int[][] board = gameBoard.getGameBoard();

        // Calculating the number of pieces I need more to make a 4.
        // rows
        for (int i = 0; i < 7; i++) {
            int connect4tracker = 4;
            for (int j = 0; j < 6; j++) {
                if (board[j][i] == 0) {
                    totalPlaysNeeded += connect4tracker;

                    if ((5-j+1) > 4) {
                        totalPossibilities += 5-j+1;
                    }

                    break;
                } else if (board[j][i] == ai) {
                    connect4tracker--;
                    if (connect4tracker == 0) {
                        connect4tracker = 4;
                    }
                } else if (board[j][i] != ai) {
                    connect4tracker = 4;
                }
                if (connect4tracker > (5-j+1)) {
                    break;
                }
            }
        }

        // Calculating the number of pieces I need more to make a 4.
        // columns
        for (int i = 0; i < 6; i++) {
            int connect4tracker = 4;
            for (int j = 0; j < 7; j++) {
                if (board[i][j] == 0) {
                    totalPlaysNeeded += connect4tracker;

                    if ((6-j+1) > 4) {
                        totalPossibilities += 6-j+1;
                    }
                    break;

                } else if (board[i][j] == ai && i > 0 && board[i-1][j] == ai) {
                    connect4tracker--;
                    if (connect4tracker == 0) {
                        connect4tracker = 4;
                    }
                } else if (board[i][j] != ai) {
                    connect4tracker = 4;
                }
                if (connect4tracker > (6-j+1)) {
                    break;
                }
            }
        }
        return ( (100/((double)totalPlaysNeeded)) + (((double)totalPossibilities)/100) );
    }

    public double Max(double i, double j){
        if( i >= j){
            return i;
        }
        else{
            return j;
        }
    }
    
    public double Min(double i, double j){
        if( i <= j){
            return i;
        }
        else{
            return j;
        }
    }

}
