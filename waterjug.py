import tkinter as tk
from tkinter import messagebox
from collections import deque


# ---------- LOGIC PART (BFS WITH ACTIONS) ----------

def get_neighbors(state, cap_a, cap_b):
    x, y = state
    moves = []

    moves.append(((cap_a, y), "Fill Jug A"))
    moves.append(((x, cap_b), "Fill Jug B"))
    moves.append(((0, y), "Empty Jug A"))
    moves.append(((x, 0), "Empty Jug B"))

    pour = min(x, cap_b - y)
    if pour > 0:
        moves.append(((x - pour, y + pour), "Pour Jug A → Jug B"))

    pour = min(y, cap_a - x)
    if pour > 0:
        moves.append(((x + pour, y - pour), "Pour Jug B → Jug A"))

    return moves


def bfs_water_jug(cap_a, cap_b, target):
    start = (0, 0)
    q = deque([start])
    visited = {start}
    parent = {start: None}
    action = {start: "Start"}

    while q:
        state = q.popleft()
        x, y = state

        if x == target or y == target:
            return reconstruct_path(parent, action, state)

        for nxt, act in get_neighbors(state, cap_a, cap_b):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = state
                action[nxt] = act
                q.append(nxt)

    return None


def reconstruct_path(parent, action, state):
    path = []
    while state is not None:
        path.append((state, action[state]))
        state = parent[state]
    return path[::-1]


# ---------- GUI PART ----------

class WaterJugGUI:
    def __init__(self, root):
        self.root = root
        root.title("Advanced Water Jug Simulation (BFS)")

        tk.Label(root, text="Jug A Capacity").grid(row=0, column=0)
        tk.Label(root, text="Jug B Capacity").grid(row=1, column=0)
        tk.Label(root, text="Target").grid(row=2, column=0)

        self.ea = tk.Entry(root)
        self.eb = tk.Entry(root)
        self.et = tk.Entry(root)

        self.ea.grid(row=0, column=1)
        self.eb.grid(row=1, column=1)
        self.et.grid(row=2, column=1)

        tk.Button(root, text="Solve", command=self.solve).grid(row=3, column=0, columnspan=2, pady=5)

        self.canvas = tk.Canvas(root, width=420, height=260, bg="white")
        self.canvas.grid(row=4, column=0, columnspan=2)

        self.status = tk.Label(root, text="Ready")
        self.status.grid(row=5, column=0, columnspan=2)

        self.path = []
        self.step = 0


    def solve(self):
        try:
            self.cap_a = int(self.ea.get())
            self.cap_b = int(self.eb.get())
            self.target = int(self.et.get())
        except:
            messagebox.showerror("Error", "Enter valid integers")
            return

        if self.target > max(self.cap_a, self.cap_b):
            messagebox.showerror("Error", "Target exceeds jug capacity")
            return

        self.path = bfs_water_jug(self.cap_a, self.cap_b, self.target)

        if not self.path:
            self.status.config(text="No solution found")
            return

        self.step = 0
        self.status.config(text=f"Solution found in {len(self.path)-1} steps")
        self.animate()


    # ---------- ANIMATION CONTROL ----------

    def animate(self):
        if self.step >= len(self.path):
            return

        (state, action) = self.path[self.step]
        prev_state = self.path[self.step - 1][0] if self.step > 0 else state

        if "Pour" in action:
            self.animate_pour(prev_state, state, action)
        else:
            self.draw_state(state, action)

        self.step += 1
        self.root.after(900, self.animate)


    # ---------- DRAWING ----------

    def draw_state(self, state, action):
        self.canvas.delete("all")
        x, y = state

        goal = (x == self.target or y == self.target)
        outline = "green" if goal else "black"

        # Jug A
        self.canvas.create_rectangle(60, 40, 140, 210, outline=outline, width=2)
        ha = int((x / self.cap_a) * 150) if self.cap_a else 0
        self.canvas.create_rectangle(60, 210-ha, 140, 210, fill="deepskyblue")
        self.canvas.create_text(100, 225, text=f"A: {x}/{self.cap_a}")

        # Jug B
        self.canvas.create_rectangle(260, 40, 340, 210, outline=outline, width=2)
        hb = int((y / self.cap_b) * 150) if self.cap_b else 0
        self.canvas.create_rectangle(260, 210-hb, 340, 210, fill="lightgreen")
        self.canvas.create_text(300, 225, text=f"B: {y}/{self.cap_b}")

        # Step text
        self.canvas.create_text(
            210, 20,
            text=f"Step {self.step}/{len(self.path)-1}: {action}",
            font=("Arial", 11, "bold")
        )

        if goal:
            self.canvas.create_text(
                210, 245,
                text="🎯 TARGET ACHIEVED!",
                fill="green",
                font=("Arial", 12, "bold")
            )


    # ---------- POUR ANIMATION ----------

    def animate_pour(self, start, end, action):
        sx, sy = start
        ex, ey = end
        frames = 10

        for i in range(frames + 1):
            x = sx + (ex - sx) * i / frames
            y = sy + (ey - sy) * i / frames

            self.canvas.delete("all")
            self.draw_jugs(x, y)

            # Pour stream
            if "A → B" in action:
                self.canvas.create_line(140, 100, 260, 100, fill="purple", width=3)
            else:
                self.canvas.create_line(260, 100, 140, 100, fill="purple", width=3)

            self.canvas.create_text(
                210, 20,
                text=f"Step {self.step}/{len(self.path)-1}: {action}",
                font=("Arial", 11, "bold")
            )

            self.root.update()
            self.root.after(60)


    def draw_jugs(self, x, y):
        # Jug A
        self.canvas.create_rectangle(60, 40, 140, 210, width=2)
        ha = int((x / self.cap_a) * 150) if self.cap_a else 0
        self.canvas.create_rectangle(60, 210-ha, 140, 210, fill="deepskyblue")

        # Jug B
        self.canvas.create_rectangle(260, 40, 340, 210, width=2)
        hb = int((y / self.cap_b) * 150) if self.cap_b else 0
        self.canvas.create_rectangle(260, 210-hb, 340, 210, fill="lightgreen")


# ---------- RUN ----------

if __name__ == "__main__":
    root = tk.Tk()
    WaterJugGUI(root)
    root.mainloop()