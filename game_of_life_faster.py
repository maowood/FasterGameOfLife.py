import pygame
import numpy as np
from numpy.fft import fft2, ifft2


pygame.init()

width, height = 1440, 800
cell_size = 1
BOARD_SHAPE = (width // cell_size, height // cell_size)

# 创建画布
screen = pygame.display.set_mode((width, height))

# 频域卷积核
KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=complex)
KERNEL_FFT = fft2(KERNEL, s=BOARD_SHAPE)

# 初始化随机状态
board = np.random.randint(2, size=BOARD_SHAPE)
board[..., :BOARD_SHAPE[1]//3] = 0
board[..., BOARD_SHAPE[1]//3*2:] = 0

# 游戏循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # 计算下一步状态
    ## 计算卷积
    board_pad = np.pad(board, [(1, 1), (1, 1)], 'wrap')
    board_fft = fft2(board_pad, s=BOARD_SHAPE)
    neighbors_tmp = np.real(ifft2(board_fft * KERNEL_FFT))
    
    neighbors = np.roll(neighbors_tmp, (-2, -2), axis=(0, 1))[:BOARD_SHAPE[0], :BOARD_SHAPE[1]]
    neighbors = np.round(neighbors)

    next_board = np.zeros(BOARD_SHAPE, dtype=int)

    #next_board[(board == 1) & (neighbors == 2)] = 1
    #next_board[neighbors == 3] = 1

    live_idxs = np.nonzero(np.bitwise_or(np.bitwise_and((board == 1), (neighbors == 2)), (neighbors == 3)))
    next_board[live_idxs] = 1

    board = next_board

    # 将细胞状态转换成RGBA格式的像素数组
    board_show = np.kron(board, np.ones((cell_size, cell_size)))
    gray_board = np.zeros((width, height, 3), dtype=np.uint8)
    gray_board[..., :] = 255 * ~ board_show[..., None].astype(bool)
    
    # 将像素数组转换成Surface对象
    surface = pygame.Surface((width, height))
    pygame.surfarray.blit_array(surface, gray_board)

    # 将Surface对象绘制到屏幕上
    screen.blit(surface, (0, 0))

    # 刷新屏幕
    pygame.display.flip()
