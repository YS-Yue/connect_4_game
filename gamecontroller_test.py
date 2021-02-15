from gamecontroller import GameController
from score_record import Score_Record


"""
This test file includes only non-graphical functionality.
The methods with graphical functionality are commented out.
Also, if a method is designed to call other methods,
only the methods be called are tested.
"""


def test_init_play_board():
    """Test the init_play_board method"""
    gc1 = GameController(0, 0, 100)
    gc2 = GameController(3, 2, 100)
    assert gc1.init_play_board() == []
    assert gc2.init_play_board() == [[0, 0, 0], [0, 0, 0]]

# def refresh_frame(self):
    # Refresh and draw the screen


# def draw_board(self):
    # Draw the grid


# def update(self):
    # Update all disks' positions in the screen, a disk will keep dropping
    # until reaching its target Y position.
    # Update the waittime for the AI's drops.
    # Update the waittime for the score file input.


# def display_all_disks(self):
    # Display all disks dropped


# def show_whoes_turn_to_drop(self):
    # Show it is the player's or AI's turn on the screen


def test_column_not_full():
    """Test the column_not_full method"""
    gc = GameController(2, 2, 100)
    gc.play_board = [[1, 0], [2, 1]]

    assert gc.column_not_full(1) is False
    assert gc.column_not_full(0) is True


def test_get_open_row():
    """Test the get_open_row method"""
    gc = GameController(2, 2, 100)
    gc.play_board = [[1, 0], [0, 0]]

    assert gc.get_open_row(0) == 1
    assert gc.get_open_row(1) == 0


def test_no_moving_disks():
    """Test the no_moving_disks method"""
    gc1 = GameController(2, 2, 100)

    gc2 = GameController(2, 2, 100)
    gc2.drop_a_disk(0)
    gc2.update()

    gc3 = GameController(2, 2, 100)
    gc3.drop_a_disk(0)
    gc3.update()
    for disk in gc3.disks:
        disk.y_vel = 0
        disk.landed = True

    assert gc1.no_moving_disks() is True
    assert gc2.no_moving_disks() is False
    assert gc3.no_moving_disks() is True


def test_is_ready_for_a_player_move():
    """Test the is_ready_for_a_player_move method"""
    gc1 = GameController(2, 2, 100)

    gc2 = GameController(2, 2, 100)
    gc2.drop_a_disk(0)
    gc2.drop_a_disk(0)
    gc2.drop_a_disk(1)

    gc3 = GameController(2, 2, 100)
    gc3.drop_a_disk(0)
    gc3.update()

    assert gc1.is_ready_for_a_player_move(80) is True
    assert gc2.is_ready_for_a_player_move(80) is False
    assert gc2.is_ready_for_a_player_move(180) is True
    assert gc3.is_ready_for_a_player_move(80) is False


def test_mouse_above_grid():
    """Test the mouse_above_grid method"""
    gc = GameController(2, 2, 100)
    assert gc.mouse_above_grid(180, 80) is True
    assert gc.mouse_above_grid(280, 80) is False
    assert gc.mouse_above_grid(180, 180) is False
    assert gc.mouse_above_grid(280, 280) is False


# def draw_leading_circle(self, mouseX):
    # Show a leading circle above the column into which
    # a player is going to drop a disk


# def drop_disk_in_turns(self, mouseX, mouseY):
    # Decide whose turns to drop a disk,
    # and then let the player drop a disk using the mouse,
    # or let the AI drop a disk automatically.
    # This method is to call other three methods


def test_when_mouse_released():
    """Test when_mouse_released method"""
    gc1 = GameController(2, 2, 100)
    gc2 = GameController(2, 2, 100)
    gc2.game_over = True

    assert gc1.when_mouse_released(150, 150) is False
    assert gc1.when_mouse_released(150, 50) is True
    assert gc2.when_mouse_released(150, 50) is False


def test_drop_a_disk():
    """Test the drop_a_disk method"""
    gc = GameController(2, 2, 100)

    assert gc.drop_a_disk(0) == [[1, 0], [0, 0]]
    assert gc.drop_a_disk(0) == [[1, 2], [0, 0]]
    assert gc.drop_a_disk(1) == [[1, 2], [1, 0]]


def test_board_is_full():
    """Test the board_is_full method"""
    gc1 = GameController(2, 2, 100)
    gc1.play_board = [[1, 2], [2, 1]]

    gc2 = GameController(2, 2, 100)
    gc2.play_board = [[1, 0], [0, 0]]

    assert gc1.board_is_full() is True
    assert gc2.board_is_full() is False


# def show_game_over(self):
    # After the last disk has stopped dropping,
    # show the "GAME OVER" on the screen
    # This method is to call two other methods.


# def one_player_win(self):
    # Check whether one player wins the game,
    # if so, show that play as the winner on the screen.
    # This method is to call two other methods.


# def show_one_player_win(self, player):
    # Show the winner on the screen


def test_check_for_win():
    """Test the check_for_win method"""
    gc1 = GameController(4, 4, 100)
    gc1.play_board = [[1, 1, 1, 1], [2, 2, 0, 0], [2, 2, 0, 0], [0, 0, 0, 0]]

    gc2 = GameController(4, 4, 100)
    gc2.play_board = [[2, 1, 1, 1], [2, 1, 0, 0], [2, 0, 0, 0], [2, 0, 0, 0]]

    gc3 = GameController(4, 4, 100)
    gc3.play_board = [[1, 2, 0, 0], [2, 1, 0, 0], [2, 1, 1, 0], [2, 2, 1, 1]]

    gc4 = GameController(4, 4, 100)
    gc4.play_board = [[1, 2, 1, 2], [1, 2, 2, 0], [1, 2, 1, 0], [2, 1, 0, 0]]

    gc5 = GameController(4, 4, 100)
    gc5.play_board = [[1, 1, 1, 0], [2, 2, 2, 0], [1, 1, 1, 0], [2, 2, 2, 0]]

    assert gc1.check_for_win(gc1.PLAYER1) is True
    assert gc2.check_for_win(gc2.AI) is True
    assert gc3.check_for_win(gc3.PLAYER1) is True
    assert gc4.check_for_win(gc4.AI) is True
    assert gc5.check_for_win(gc5.PLAYER1) is False


# def AI_drops_a_disk(self):
    # Find the best move by evaluating all possible valid columns.
    # AI drop a disk in that best column.
    # This method is to call other three methods


def test_AI_all_valid_cols():
    """Test the AI_all_valid_cols method"""
    gc1 = GameController(4, 4, 100)
    gc1.play_board = [[1, 1, 1, 2], [2, 2, 1, 0], [2, 2, 0, 0], [1, 0, 0, 0]]

    gc2 = GameController(2, 2, 100)
    gc2.play_board = [[1, 2], [2, 1]]

    assert gc1.AI_all_valid_cols() == [1, 2, 3]
    assert gc2.AI_all_valid_cols() == []


def test_AI_score_one_array():
    """Test the AI_score_one_array method"""
    gc = GameController(4, 4, 100)
    array1 = [2, 2, 2, 2]
    array2 = [2, 2, 2, 0]
    array3 = [2, 0, 2, 0]
    array4 = [1, 1, 0, 1]
    array5 = [1, 0, 1, 0]
    array6 = [0, 0, 0, 2]

    assert gc.AI_score_one_array(array1) == 1000000
    assert gc.AI_score_one_array(array2) == 10
    assert gc.AI_score_one_array(array3) == 2
    assert gc.AI_score_one_array(array4) == -100
    assert gc.AI_score_one_array(array5) == -50
    assert gc.AI_score_one_array(array6) == 0


def test_AI_score_one_move():
    """Test the AI_score_one_move method"""
    # Since this method includes loop comuptations,
    # it is too complicated to test all possible inputs and outputs.
    gc = GameController(4, 4, 100)
    temp_play_board1 = [[1, 2, 1, 0], [2, 2, 2, 0], [1, 0, 0, 0], [1, 0, 0, 0]]
    temp_play_board2 = [[1, 2, 1, 0], [2, 2, 2, 0], [1, 1, 1, 0], [1, 2, 2, 0]]
    temp_play_board3 = [[1, 2, 1, 1], [2, 2, 2, 2], [1, 1, 1, 0], [1, 2, 2, 0]]

    assert gc.AI_score_one_move(temp_play_board1) == 12
    assert gc.AI_score_one_move(temp_play_board2) == -90
    assert gc.AI_score_one_move(temp_play_board3) == 999900


def test_AI_evaluate_possible_moves():
    """Test the AI_evaluate_possible_moves method"""
    # Since this method includes loop comuptations,
    # it is too complicated to test all possible inputs and outputs.
    gc = GameController(4, 4, 100)
    gc.play_board = [[1, 2, 1, 0], [2, 2, 2, 0], [1, 1, 1, 0], [1, 2, 2, 0]]
    valid_cols = [0, 1, 2, 3]
    assert gc.AI_evaluate_possible_moves(valid_cols) == 1


# def prompt_player_for_name(self):
    # When game over, prompt the player for name


# def input(self, message=''):
    # Define an interactive text input


# def update_score_file(self):
    # If the player is the winner, update the score file
    # This method is to call the read_and_update_data method of
    # the Score_Record class.


def test_read_and_update_data():
    """Test the read_and_update_data of the Score_Record class"""

    f = open('test_scores', 'w')
    sr = Score_Record('test_scores', 'yue')
    sr2 = Score_Record('test_scores', 'sherry')
    sr3 = Score_Record('test_scores', 'sherry')

    assert sr.read_and_update_data() == [('yue', 1)]
    assert sr2.read_and_update_data() == [('yue', 1), ('sherry', 1)]
    assert sr3.read_and_update_data() == [('sherry', 2), ('yue', 1)]
