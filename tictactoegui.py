import copy
import tkinter as tk
from tkinter import messagebox
from collections import deque


class TicTacToe:
    def __init__(self, arr, player):
        self.node = arr
        self.friends = []
        self.who_played = player


def create_state_space(root,arr, player):
    queue = deque()
    tic = TicTacToe(root.node, player)
    queue.append(root)

    while queue:
        n = queue.popleft()
        print(n.node)
        temp_arr = copy.deepcopy(n.node)
        if n.who_played == 'X':
            next_player = 'O'
        else:
            next_player = 'X'

        if not check_winner2(n.node):
            for i in range(len(n.node)):
                for j in range(len(n.node[i])):
                    if n.node[i][j] == "":
                        temp_arr[i][j] = next_player
                        tic2 = TicTacToe(copy.deepcopy(temp_arr), next_player)
                        n.friends.append(tic2)
                        queue.append(tic2)
                        temp_arr[i][j] = ""


def is_terminal(board):
    return check_winner(board, "O") or check_winner(board, "X") or all(cell != "" for row in board for cell in row)


def evaluate(board):
    if check_winner(board, "X"):
        return 10
    elif check_winner(board, "O"):
        return -10
    else:
        return 0


def max_depth(root):
    if root is None:
        return 0
    elif not root.friends:
        return 1
    else:
        child_depths = [max_depth(child) for child in root.friends]
        return max(child_depths) + 1


def check_winner(arr, player):
    for i in range(3):
        if arr[i][0] == arr[i][1] == arr[i][2] == player:
            return True
        if arr[0][i] == arr[1][i] == arr[2][i] == player:
            return True
    if arr[0][0] == arr[1][1] == arr[2][2] == player:
        return True
    if arr[0][2] == arr[1][1] == arr[2][0] == player:
        return True
    return False


def check_winner2(arr):
    for i in range(3):
        if arr[i][0] == arr[i][1] == arr[i][2] != "":
            return True
        if arr[0][i] == arr[1][i] == arr[2][i] != "":
            return True
    if arr[0][0] == arr[1][1] == arr[2][2] != "":
        return True
    if arr[0][2] == arr[1][1] == arr[2][0] != "":
        return True
    return False


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.player = "O"
        self.ai = "X"
        self.arr = [["", "", ""],
                    ["", "", ""],
                    ["", "", ""]]

        self.buttons = []

        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = tk.Button(self.root, text="", font=('Helvetica', 20), width=6, height=3,
                                command=lambda i=i, j=j: self.on_button_click(i, j))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def on_button_click(self, i, j):
        if self.arr[i][j] == "":
            self.buttons[i][j].config(text=self.player)
            self.arr[i][j] = self.player
            self.check_game_status()
            self.ai_move()
            print(self.arr)
            self.check_game_status()

    def ai_move(self):
        root = TicTacToe(self.arr, self.player)
        create_state_space(root,self.arr, self.player)
        print(root.friends)
        best_score = float('-inf')
        best_move = None
        for child in root.friends:
            score = minimax2(child, 0, False)
            print(f"Move: {child.node}, Score: {score}")  # Debug print statement
            if score > best_score:
                best_score = score
                best_move = child
        if best_move:
            print(best_move)
            self.arr = copy.deepcopy(best_move.node)
            self.update_buttons()

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.arr[i][j])
        print("Board updated:", self.arr)  # Debug print statement

    def check_game_status(self):
        if check_winner(self.arr, "X"):
            messagebox.showinfo("Game Over", "AI wins!")
            self.reset_game()
        elif check_winner(self.arr, "O"):
            messagebox.showinfo("Game Over", "You win!")
            self.reset_game()
        elif all(cell != "" for row in self.arr for cell in row):
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_game()

    def reset_game(self):
        self.arr = [["", "", ""],
                    ["", "", ""],
                    ["", "", ""]]
        self.update_buttons()


def minimax2(board, depth, maximizing_player):
    if is_terminal(board.node):
        return evaluate(board.node)

    if maximizing_player:
        max_eval = float('-inf')
        for child in board.friends:
            eval = minimax2(child, depth + 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for child in board.friends:
            eval = minimax2(child, depth + 1, True)
            min_eval = min(min_eval, eval)
        return min_eval


if __name__ == '__main__':
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
