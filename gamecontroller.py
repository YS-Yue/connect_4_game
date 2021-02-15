from disk import Disk
import random
import copy
from score_record import Score_Record


class GameController:

    def __init__(self, rows, columns, unit):
        self.ROWS = rows
        self.COLUMNS = columns
        self.UNIT = unit
        self.play_board = self.init_play_board()
        self.game_over = False
        self.turns = 0
        self.disks = []
        self.PLAYER1 = 1
        self.AI = 2
        self.winner = 0
        self.wait = 0
        self.enter_name = 0
        self.wait_for_score = 1000

    def init_play_board(self):
        """Generate the nested list representing the play board"""
        return [[0] * self.ROWS for i in range(self.COLUMNS)]

    def refresh_frame(self):
        """Refresh and draw the screen"""
        self.show_whoes_turn_to_drop()
        self.display_all_disks()
        self.update()
        self.draw_board()
        self.one_player_win()
        self.board_is_full()
        if self.game_over:
            self.show_game_over()
        if self.wait_for_score == 0:
            self.prompt_player_for_name()

    def draw_board(self):
        """Draw the grid"""
        BLUE = (0, 0, 255)
        STROKE_WEIGHT = 16
        strokeWeight(STROKE_WEIGHT)
        stroke(*BLUE)

        for i in range(self.ROWS + 1):
            line(0, (i + 1) * self.UNIT, self.COLUMNS * self.UNIT,
                 (i + 1) * self.UNIT)
        for j in range(self.COLUMNS + 1):
            line(j * self.UNIT, self.UNIT, j * self.UNIT,
                 (self.ROWS + 1) * self.UNIT)

    def update(self):
        """
        Update all disks' positions in the screen, a disk will keep dropping
        until reaching its target Y position.
        Update the waittime for the AI's drops.
        Update the waittime for the score file input.
        """
        COUNTDOWN = 20
        MOVE_PER_FRAME = 20

        for disk in self.disks:
            if disk.y + disk.y_vel >= disk.y_to_stop:
                disk.y_vel = 0
                disk.y = disk.y_to_stop
                disk.landed = True
            else:
                disk.y_vel += MOVE_PER_FRAME
        if self.wait > 0:
            self.wait -= COUNTDOWN
        else:
            self.wait = 0
        if self.game_over:
            self.wait_for_score -= COUNTDOWN
            if self.wait_for_score < 0:
                self.wait_for_score = 0

    def display_all_disks(self):
        """Display all disks dropped"""
        for disk in self.disks:
            disk.draw_disk()

    def show_whoes_turn_to_drop(self):
        """Show it is the player's or AI's turn on the screen"""

        TEXTSIZE = 20
        WHITE = (255, 255, 255)

        if not self.game_over:
            textSize(TEXTSIZE)
            textAlign(CENTER)
            if self.turns % 2 == 0 and self.no_moving_disks():
                fill(*WHITE)
                text("PLAYER'S TURN", (self.COLUMNS)*self.UNIT/2,
                     self.UNIT/2)
            elif self.turns % 2 == 0 and not self.no_moving_disks():
                fill(*WHITE)
                text("AI'S TURN", (self.COLUMNS)*self.UNIT/2,
                     self.UNIT/2)
            elif self.turns % 2 == 1 and self.no_moving_disks():
                fill(*WHITE)
                text("AI'S TURN", (self.COLUMNS)*self.UNIT/2,
                     self.UNIT/2)
            elif self.turns % 2 == 1 and not self.no_moving_disks():
                fill(*WHITE)
                text("PLAYER'S TURN", (self.COLUMNS)*self.UNIT/2,
                     self.UNIT/2)

    def column_not_full(self, x):
        """Check whether a column is full of disks"""
        column_to_drop = max(0, x)
        column_to_drop = min(x, self.COLUMNS - 1)

        # If the last item of this list is not the original value O,
        # the column is already full
        if self.play_board[column_to_drop][-1] == 0:
            return True
        else:
            return False

    def get_open_row(self, column):
        """Find the lowest empty row of the column that a disk can locate"""
        for i in range(self.ROWS):
            if self.play_board[column][i] == 0:
                return i

    def no_moving_disks(self):
        """Check whether there is no moving disks showing on the screen"""
        for disk in self.disks:
            if disk.y_vel != 0 and disk.landed == 0:
                return False
        return True

    def is_ready_for_a_player_move(self, mouseX):
        """
        Then Check whether there is no moving disks showing on the screen,
        and the column above which the mouse locates is not full of disks
        """
        if mouseX >= 0 or mouseX <= self.COLUMNS*self.UNIT:
            if (self.no_moving_disks() and
                    self.column_not_full(mouseX // self.UNIT)):
                return True
            else:
                return False

    def mouse_above_grid(self, mouseX, mouseY):
        """Check whether the mouse is in the area above the grid"""
        if(mouseY <= self.UNIT and mouseX <= self.UNIT*self.COLUMNS
           and mouseX > 0):
            return True
        else:
            return False

    def draw_leading_circle(self, mouseX):
        """
        Show a leading circle above the column into which
        a player is going to drop a disk
        """
        RED = (255, 0, 0)

        if self.mouse_above_grid(mouseX, mouseY):
            if self.is_ready_for_a_player_move(mouseX):
                fill(*RED)
                noStroke()
                ellipse((mouseX // self.UNIT + 0.5) * self.UNIT, self.UNIT/2,
                        self.UNIT, self.UNIT)

    def drop_disk_in_turns(self, mouseX, mouseY):
        """
        Decide whose turns to drop a disk,
        and then let the player drop a disk using the mouse,
        or let the AI drop a disk automatically.
        """
        WAIT_TIME = 1000
        if self.turns % 2 == 0 and not self.game_over:
            if mousePressed:
                if self.mouse_above_grid(mouseX, mouseY):
                    self.draw_leading_circle(mouseX)
                    self.wait = WAIT_TIME

        elif self.turns % 2 == 1 and not self.game_over:
            if self.wait == 0:
                self.AI_drops_a_disk()

    def when_mouse_released(self, mouseX, mouseY):
        """
        If the mouse is in the valid position,
        and the game is not over,
        let the player drops a disk
        """
        if self.mouse_above_grid(mouseX, mouseY):
            if self.is_ready_for_a_player_move(mouseX) and not self.game_over:
                self.drop_a_disk(mouseX // self.UNIT)
                return True
        return False

    def drop_a_disk(self, x):
        """
        Determine the player and the color of disk of this turn,
        create a new disk, and resign of value of the item representing
        the position of this disk in the nest lists representing the playboard
        """
        RED = (255, 0, 0)
        YELLOW = (255, 255, 0)

        # Determine the player of this turn, and the color of new disk
        if self.turns % 2 == 0:
            color = RED
            player_move = self.PLAYER1
        else:
            color = YELLOW
            player_move = self.AI

        # Find the lowest empty row in the given column
        open_row = self.get_open_row(x)

        # Determine the target Y position for the new disk
        y_stop = (self.ROWS - open_row + 0.5)*self.UNIT

        # Create a new disk
        new_disk = Disk((x + 0.5) * self.UNIT, self.UNIT/2,
                        color, self.UNIT, y_stop)

        # Add the new disk to the list of all existing disks
        self.disks.append(new_disk)

        # Resign value to the item representing the position of
        # the new disk in the nest lists
        self.play_board[x][open_row] = player_move

        # Add 1 to the value of the turns of the game
        self.turns += 1

        return self.play_board

    def board_is_full(self):
        """Check whether the playboard is full, that means the game is over"""

        # If all the last item of lists representing the columns are not 0,
        # all the columns are already full
        for column in self.play_board:
            if column[-1] == 0:
                return False
        self.game_over = True
        return True

    def show_game_over(self):
        """
        After the last disk has stopped dropping,
        show the "GAME OVER" on the screen
        """

        TEXTSIZE = 30
        BLACK = (0, 0, 0)
        if self.no_moving_disks():
            fill(*BLACK)
            textSize(TEXTSIZE)
            textAlign(CENTER)
            text("GAME OVER", (self.COLUMNS)*self.UNIT/2,
                 self.UNIT/2)
            self.ready_for_score = 1

    def one_player_win(self):
        """
        Check whether one player wins the game,
        if so, show the winner on the screen
        """
        if self.no_moving_disks():
            if self.turns % 2 == 0:
                if self.check_for_win(self.AI):
                    self.winner = self.AI
                    self.game_over = True
                    self.show_one_player_win(self.AI)
            else:
                if self.check_for_win(self.PLAYER1):

                    self.winner = self.PLAYER1
                    self.game_over = True
                    self.show_one_player_win(self.PLAYER1)

    def show_one_player_win(self, player):
        """Show the winner on the screen"""

        TEXTSIZE = 80
        SIZE2 = 78
        SIZE3 = 76
        WHITE = (255, 255, 255)
        CYAN = (0, 255, 255)

        textSize(TEXTSIZE)
        textAlign(CENTER)
        if player == self.PLAYER1:
            fill(*WHITE)
            text("YOU WON!", (self.COLUMNS)*self.UNIT/2,
                 (self.ROWS + 1)*self.UNIT/2)
            textSize(SIZE2)
            text("YOU WON!", (self.COLUMNS)*self.UNIT/2,
                 (self.ROWS + 1)*self.UNIT/2)
            textSize(SIZE3)
            fill(*CYAN)
            text("YOU WON!", (self.COLUMNS)*self.UNIT/2,
                 (self.ROWS + 1)*self.UNIT/2)
        elif player == self.AI:
            fill(*WHITE)
            text("AI WON", (self.COLUMNS)*self.UNIT/2,
                 (self.ROWS + 1)*self.UNIT/2)
            textSize(SIZE2)
            text("AI WON", (self.COLUMNS)*self.UNIT/2,
                 (self.ROWS + 1)*self.UNIT/2)
            textSize(SIZE3)
            fill(*CYAN)
            text("AI WON", (self.COLUMNS)*self.UNIT/2,
                 (self.ROWS + 1)*self.UNIT/2)

    def check_for_win(self, PLAYER):
        """
        Check whether the player or the AI has four disks in a row
        horizontally, vertically, or diagonally
        """
        ARRAY_LEN = 4
        # Check vertically.
        for i in range(self.COLUMNS):
            for j in range(self.ROWS - ARRAY_LEN + 1):
                if (self.play_board[i][j] == PLAYER and
                    self.play_board[i][j + 1] == PLAYER and
                    self.play_board[i][j + 2] == PLAYER and
                        self.play_board[i][j + 3] == PLAYER):
                    return True

        # Check horizontally.
        for i in range(self.ROWS):
            for j in range(self.COLUMNS - ARRAY_LEN + 1):
                if (self.play_board[j][i] == PLAYER and
                    self.play_board[j + 1][i] == PLAYER and
                    self.play_board[j + 2][i] == PLAYER and
                        self.play_board[j + 3][i] == PLAYER):
                    return True

        # Check positive-slope diagonals.
        for i in range(self.COLUMNS - ARRAY_LEN + 1):
            for j in range(self.ROWS - ARRAY_LEN + 1):
                if (self.play_board[i][j] == PLAYER and
                    self.play_board[i + 1][j + 1] == PLAYER and
                    self.play_board[i + 2][j + 2] == PLAYER and
                        self.play_board[i + 3][j + 3] == PLAYER):
                    return True

        # Check negative-slope diagonals.
        for i in range(self.COLUMNS - ARRAY_LEN + 1):
            for j in range(ARRAY_LEN - 1, self.ROWS):
                if (self.play_board[i][j] == PLAYER and
                    self.play_board[i + 1][j - 1] == PLAYER and
                    self.play_board[i + 2][j - 2] == PLAYER and
                        self.play_board[i + 3][j - 3] == PLAYER):
                    return True
        return False

    def AI_drops_a_disk(self):
        """
        Find the best move by evaluating all possible valid columns.
        AI drop a disk in that best column.
        """
        valid_cols = self.AI_all_valid_cols()
        best_move = self.AI_evaluate_possible_moves(valid_cols)
        self.drop_a_disk(best_move)

    def AI_all_valid_cols(self):
        """Find all possible valid columns to drop a disk in."""
        vaild_cols = []
        for i in range(self.COLUMNS):
            if self.column_not_full(i):
                vaild_cols.append(i)
        return vaild_cols

    def AI_score_one_array(self, array):
        """Score the array which has a length of 4."""
        WIN_MOVE = 1000000
        GOOD_MOVE = 10
        OK_MOVE = 2
        UNDESIRED_MOVE = -50
        LOSE_MOVE = -100

        score_array = 0
        if array.count(self.AI) == 4:
            score_array = WIN_MOVE
        elif array.count(self.AI) == 3 and array.count(0) == 1:
            score_array = GOOD_MOVE
        elif array.count(self.AI) == 2 and array.count(0) == 2:
            score_array = OK_MOVE
        elif array.count(self.PLAYER1) == 3 and array.count(0) == 1:
            score_array = LOSE_MOVE
        elif array.count(self.PLAYER1) == 2 and array.count(0) == 2:
            score_array = UNDESIRED_MOVE

        return score_array

    def AI_score_one_move(self, temp_play_board):
        """
        Evaluate the outcome of one specific move by adding up
        the scores of all arrays with a length of 4.
        """
        score = 0
        ARRAY_LEN = 4

        # Add up scores of all vertical arrays.
        for i in range(self.COLUMNS):
            for j in range(self.ROWS - ARRAY_LEN + 1):
                array = [temp_play_board[i][j + k] for k in range(ARRAY_LEN)]
                score += self.AI_score_one_array(array)

        # Add up scores of all horizontal arrays.
        for i in range(self.ROWS):
            for j in range(self.COLUMNS - ARRAY_LEN + 1):
                array = [temp_play_board[j + k][i] for k in range(ARRAY_LEN)]
                score += self.AI_score_one_array(array)

        # Add up scores of all positive-slope diagonal arrays.
        for i in range(self.COLUMNS - ARRAY_LEN + 1):
            for j in range(self.ROWS - ARRAY_LEN + 1):
                array = [temp_play_board[i+k][j+k] for k in range(ARRAY_LEN)]
                score += self.AI_score_one_array(array)

        # Add up scores of all negative-slope diagonal arrays.
        for i in range(self.COLUMNS - ARRAY_LEN + 1):
            for j in range(ARRAY_LEN - 1, self.ROWS):
                array = [temp_play_board[i+k][j-k] for k in range(ARRAY_LEN)]
                score += self.AI_score_one_array(array)

        return score

    def AI_evaluate_possible_moves(self, valid_cols):
        """
        Evaluate outcomes of all possible valid columns,
        choose the column leading to the highest score.
        """

        best_col = random.choice(valid_cols)
        play_board_benchmark = copy.deepcopy(self.play_board)
        play_board_benchmark[best_col][self.get_open_row(best_col)] = self.AI
        best_score = self.AI_score_one_move(play_board_benchmark)

        for col in valid_cols:
            temp_play_board = copy.deepcopy(self.play_board)
            temp_play_board[col][self.get_open_row(col)] = self.AI
            temp_score = self.AI_score_one_move(temp_play_board)
            if temp_score > best_score:
                best_col = col
                best_score = temp_score

        return best_col

    def prompt_player_for_name(self):
        """When game over, prompt the player for name"""
        if not self.enter_name:
            name = self.input('Enter your name').lower()
            if name:
                self.enter_name = name
            self.update_score_file()

    def input(self, message=''):
        """Define an interactive text input"""
        from javax.swing import JOptionPane
        return JOptionPane.showInputDialog(frame, message)

    def update_score_file(self):
        """If the player is the winner, update the score file"""
        if self.winner == 1:
            sr = Score_Record('scores', self.enter_name)
            sr.read_and_update_data()
