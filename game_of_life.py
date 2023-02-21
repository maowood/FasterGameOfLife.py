import pygame
import numpy as np
import time

# 初始化Pygame
pygame.init()

# 设置画布大小
screen = pygame.display.set_mode((1440, 800))

# 设置细胞大小
cell_size = 5
cols, rows = int(screen.get_width() / cell_size), int(screen.get_height() / cell_size)

# 创建一个二维数组来表示细胞的状态，0表示死亡，1表示存活
board = np.zeros((rows, cols))

# 随机初始化细胞状态
for r in range(rows):
    for c in range(cols):
        board[r][c] = np.random.randint(2)

# 设置游戏循环
while True:
    # 绘制细胞状态
    for r in range(rows):
        for c in range(cols):
            color = (255, 255, 255) if board[r][c] == 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, (c * cell_size, r * cell_size, cell_size, cell_size))

    # 复制细胞状态，计算下一步状态
    next_board = np.copy(board)
    for r in range(rows):
        for c in range(cols):
            # 统计周围存活细胞的数量
            neighbors = (
                board[(r - 1) % rows][(c - 1) % cols] + board[(r - 1) % rows][c] + board[(r - 1) % rows][(c + 1) % cols] +
                board[r][(c - 1) % cols] + board[r][(c + 1) % cols] +
                board[(r + 1) % rows][(c - 1) % cols] + board[(r + 1) % rows][c] + board[(r + 1) % rows][(c + 1) % cols]
            )
            # 应用规则
            if board[r][c] == 1 and (neighbors < 2 or neighbors > 3):
                next_board[r][c] = 0
            elif board[r][c] == 0 and neighbors == 3:
                next_board[r][c] = 1

    # 更新细胞状态
    board = next_board

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # 刷新画面
    pygame.display.update()
    time.sleep(0.5)