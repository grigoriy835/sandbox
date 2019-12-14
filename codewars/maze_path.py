a = "\n".join([
  ".W.",
  ".W.",
  "..."
])


def path_finder(maze: str):
    normaze = list(map(lambda x: list(map(lambda y: float("inf") if y == '.' else -1, list(x))), maze.split('\n')))
    n = len(normaze)-1
    queue = [[0, 0]]
    if len(normaze) < 2:
        return 0
    normaze[0][0] = 0
    while len(queue):
        x, y = queue.pop()
        steps = normaze[x][y]
        if x < n and normaze[x+1][y] > (steps+1):
            normaze[x + 1][y] = steps+1
            queue.insert(0, [x+1, y])
        if x > 0 and normaze[x-1][y] > (steps+1):
            normaze[x-1][y] = steps+1
            queue.insert(0, [x-1, y])

        if y < n and normaze[x][y+1] > (steps+1):
            normaze[x][y+1] = steps+1
            queue.insert(0, [x, y+1])
        if y > 0 and normaze[x][y-1] > (steps+1):
            normaze[x][y-1] = steps+1
            queue.insert(0, [x, y-1])
        if normaze[-1][-1] < float("inf"):
            return normaze[-1][-1]

    return False



#////////////////////---------------------------------------------best


def path_finder1(maze):
    lst = maze.split('\n')
    X, Y = len(lst) - 1, len(lst[0]) - 1
    seen = {(x, y) for x, row in enumerate(lst) for y, c in enumerate(row) if c == 'W'} | {(0, 0)}
    end, bag, turn = (X, Y), {(0, 0)}, 0

    while bag and end not in bag:
        bag = {(a, b) for a, b in {(x + dx, y + dy) for x, y in bag for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))}
               if 0 <= a <= X and 0 <= b <= Y} - seen
        seen |= bag
        turn += 1

    return bool(bag) and turn


res = path_finder(a)
