import random
import maze
import turtle

def draw_matrix(size, pos, loop):
    matrix_width = loop[0] * size[0] # convert size
    matrix_height = loop[1] * size[1]
    init_pos = [pos[0] - matrix_width/2, pos[1] + matrix_height/2]  # find the position of the left top corner
    box_color = {}  # build a dic for boxcolor {index: "color"}
    for i in range(len(maze.random_color)):
        box_color[i] = maze.random_color[i]
    box_offset = 4  # the box offset
    for i in range(5):
        index = i % loop[0]
        for j in range(5):
            new_j = (j) % loop[1] + index
            random_y_offset = random.uniform(size[1]*0.35, size[1]*0.65)
            main_color = box_color[new_j]   # get the color
            m = maze.Maze([init_pos[0] + size[0] * i, init_pos[1] - size[1] * j - random_y_offset],
                          [init_pos[0]+size[0]*i, (init_pos[0]+size[0]*i)+size[0], (init_pos[1]-size[1]*j)-size[1], init_pos[1]-size[1]*j],
                          0, random.randint(50, 100), main_color=main_color)
            # m.set_main_color(main_color)
            m.draw_a_rect([init_pos[0]+size[0]*i-box_offset/2, init_pos[1]-size[1]*j - size[1]-box_offset/2, size[0]-box_offset, size[1]-box_offset],
                          pensize=3,
                          color=main_color) # draw the box
            m.show()    # main function


turtle.setup(1000, 1000)
turtle.speed(0)
turtle.tracer(0)
draw_matrix([190, 190], [0, 0], [5, 5])
turtle.tracer(1)
turtle.exitonclick()
