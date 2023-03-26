import random
import turtle
import copy
import math

random_color = ["red", "orange", "green", "blue", "purple", "gold", "orange red",
                             "medium slate blue", "medium violet red", "turquoise", "dark olive green",
                             "peach puff", "tomato", "dim gray", "papaya whip"] # all the colors
class Node:
    def __init__(self, pos, dir):
        self.pos = pos  # save the position of the node
        self.dir = dir  # save the direction of the node
    def __str__(self):
        return "pos: " + str(self.pos) + ", dir: " + str(self.dir) + ";"    # return the position and direction of the node
class Maze:
    def __init__(self, pos, size, dir, life_circle, main_color = ""):
        self.offset = 20 # set the margin
        size[0] += self.offset  # update the margin
        size[1] -= self.offset
        size[2] += self.offset
        size[3] -= self.offset
        self.size = size    # the size of the pattern
        pos[0] += self.offset   # update the margin
        pos[1] -= self.offset
        self.init_pos = pos # the position where the turtle starts
        self.init_dir = dir # the direction where the turtle starts
        self.node_li = [Node(self.init_pos, self.init_dir)] # the node array
        self.random_color = copy.copy(random_color)
        if main_color:  # if color is given, that increaing its possibility of being picked
            for _ in range(14): self.random_color.append(main_color)
        self.width = abs(self.size[1] - self.size[0])   # the width of the pattern
        self.height = abs(self.size[3] - self.size[2])  # the height of the pattern
        self.random_bg_size_li = (self.width / 10, self.width / 8, self.width / 6, self.width / 4)  # the sizes of the rect shape
        self.random_length_li = (self.width / 56, self.width / 48, self.width / 40, self.width / 32,
                                 self.width / 24, self.width / 18, self.width / 12)  # the lengths of the path
        self.random_len = random.choice(self.random_length_li)  # the length of the first path
        self.random_degree_li = (-90, 90, -45, 45)  # the angle of the path change
        self.pensize_line = [1, 3]
        self.shape_scale = 0.6
        self.index = [0, 0] # it saves the data of the lifecircle of the pattern
        self.random_num = 1 # variable used in generate_shape()
        self.finish_draw = False    # determine if the current node still alive
        self.life_circle = life_circle  # determine how many paths in this pattern
        self.is_finish_setup = False    # determine if it is the first loop
        # move to first node
        turtle.pu()
        turtle.setheading(self.node_li[0].dir)
        turtle.goto(self.node_li[0].pos[0], self.node_li[0].pos[1])
    def set_main_color(self, color):
        for _ in range(14): self.random_color.append(color)
    def generate_bg_shape(self, num):
        for _ in range(num):
            rec_x_size = random.choice(self.random_bg_size_li)  # choose the width
            rec_y_size = random.choice(self.random_bg_size_li)  # choose the height
            rec_x_range = self.width - rec_x_size   # the range where x can be placed
            rec_y_range = self.height - rec_y_size  # the range where y can be placed
            rec_x_pos = random.uniform(self.size[0], self.size[0] + rec_x_range)    # x position
            rec_y_pos = random.uniform(self.size[2], self.size[2] + rec_y_range)    # y position
            # draw the rect shape
            turtle.begin_fill()
            turtle.color(random.choice(self.random_color))
            self.draw_a_rect([rec_x_pos, rec_y_pos, rec_x_size, rec_y_size])
            turtle.end_fill()
    def draw_a_rect(self, rect, pensize = 3, color = ""):
        turtle.pu()
        turtle.setheading(0)
        turtle.goto(rect[0], rect[1])   # rect contains four data: x, y, width, height
        if not bool(color): color = random.choice(self.random_color)
        turtle.color(color)
        turtle.pd()
        turtle.pensize(pensize)
        for i in range(4):
            if i % 2 == 0: turtle.forward(rect[2])
            else: turtle.forward(rect[3])
            turtle.left(90)
        turtle.pu()
    def show(self):
        def display():
            if not self.is_finish_setup: # only excute once
                self.is_finish_setup = True
                # self.draw_a_rect([self.size[0]-self.offset, self.size[2]-self.offset, self.width+self.offset*2, self.height+self.offset*2])
                if random.random() > 0.7: self.generate_bg_shape(random.randint(1, 3))    # draw the rect shapes in the background
            if not self.is_finish():
                curr_node = copy.deepcopy(self.node_li[0])  # copy1 of the current node
                new_node = copy.deepcopy(self.node_li[0])   # copy2 of the current node
                self.random_len = random.choice(self.random_length_li)  # pick the length of the next path
                saver_node = self.update_pos(new_node.pos, new_node.dir, self.random_len)   # get a data holder
                self.check_alive(saver_node)   # check if the current node exceeds the boundary
                if self.finish_draw:    # if the current node will exceed the boundary
                    self.node_li.pop(0) # remove the current node
                    self.index[0] += 1  # update the lifecircle
                    random.shuffle(self.node_li)    # shuffle the nodes
                    self.finish_draw = False    # reset
                    if random.random() > 0.96: self.generate_bg_shape(1)    # draw rect shape
                else:
                    self.node_li[0].pos = saver_node  # update the data
                    self.draw_main(curr_node.pos,self.node_li[0].pos, curr_node.dir)    # draw the path
                    # generate a new node
                    if random.random() > 0.3:
                        self.node_li.append(Node(self.node_li[0].pos,
                                                 self.node_li[0].dir + random.choice(self.random_degree_li)))
            else:
                turtle.pu()

        # draw itself
        while not self.is_finish():
            display()
        # if finish drawing, delete itself
        else:
            del self
            # print("finish")
    def check_alive(self, pos): # check if the pos is out of the boundary
        # print(self.size[0], pos[0],self.size[1], self.size[2],pos[1],self.size[3])
        if self.size[0] <= pos[0] <= self.size[1] and self.size[2] <= pos[1] <= self.size[3]:
            return
        else:
            self.finish_draw = True
    def generate_shape(self, odd_pos, new_pos): # draw the random shape
        def draw_shapes(size, poly, fill):
            if fill: turtle.begin_fill()
            for _ in range(poly):
                turtle.forward(size*self.shape_scale)
                turtle.left(360/poly)
            if fill: turtle.end_fill()
            turtle.pu()
        self.random_num = random.randint(1, 18)
        # self.random_num = 3
        match self.random_num:  # possibility
            # shape1
            case 1:
                for i in range(random.randint(1, 3)):
                    turtle.right(random.uniform(-45, 45))
                    turtle.forward(self.width*self.shape_scale / 10)
                # turtle.circle(random.randint(1, 3))
                draw_shapes(random.randint(1, 3), random.randint(1, 5), False)
            # shape2
            case 2:
                # Generate the spiral path
                for i in range(random.randint(1, 3)):
                    turtle.right(random.uniform(-40, 40))
                    turtle.forward(i * 2*self.shape_scale)
                    # turtle.begin_fill()
                    turtle.color(random.choice(self.random_color))
                    turtle.circle(i * 3)
                    # turtle.end_fill()
            # shape3
            case 3:
                for i in range(3):
                    turtle.right(random.uniform(5, 20))
                    # turtle.forward(i * 2)
                    # generate filled shapes along the path
                    if random.random() > 0.85:
                        turtle.begin_fill()
                        for j in range(random.randint(3, 8)):
                            turtle.forward(random.randint(1, 4)*self.shape_scale)
                            turtle.right(360 / random.randint(3, 8))
                        turtle.end_fill()
                        turtle.penup()
                        turtle.forward(self.width*self.shape_scale / random.randint(12, 24))
                        turtle.pendown()
            # shape4
            case 4 | 5:
                if random.random() > 0.2: turtle.pu()
                if_fill = True if random.random() > 0.8 else False
                for i in range(random.randint(2, 4)):
                    turtle.right(random.uniform(-65, 65))
                    turtle.forward(random.randint(3, 14)*self.shape_scale)
                turtle.pd()
                draw_shapes(random.randint(1, 3), random.randint(3, 10), if_fill)
            case _:
                pass
    def generate_line(self, odd_pos, new_pos):
        match random.randint(1, 8):
            #dash path
            case 1:
                turtle.pensize(random.randint(self.pensize_line[0], self.pensize_line[1]))
                turtle.color("black")
                steps = random.randint(2, 4)
                dash_length = self.random_len / steps
                for _ in range(int(steps)):
                    turtle.forward(dash_length * 0.5)
                    turtle.up()
                    turtle.forward(dash_length * 0.5)
                    turtle.down()
                remaining_distance = self.random_len % dash_length
                turtle.forward(remaining_distance)
            #bezier path
            case 2:
                turtle.pensize(random.randint(self.pensize_line[0], self.pensize_line[1]))
                steps = random.randint(2, 5)
                for i in range(steps):
                    turtle.goto(
                        (1 - i / steps) ** 3 * odd_pos[0] + 3 * (1 - i / steps) ** 2 * i / steps * (odd_pos[0]+random.uniform(-20, 20)) + 3 * (
                                1 - i / steps) * (i / steps) ** 2 * (new_pos[0]+random.uniform(-20, 20)) + (i / steps) ** 3 * new_pos[0],
                        (1 - i / steps) ** 3 * odd_pos[1] + 3 * (1 - i / steps) ** 2 * i / steps * (odd_pos[1]+random.uniform(-20, 20)) + 3 * (
                                1 - i / steps) * (i / steps) ** 2 * (new_pos[1]+random.uniform(-20, 20)) + (i / steps) ** 3 * new_pos[1]
                    )
            # normal path
            case _:
                turtle.pensize(random.randint(self.pensize_line[0], self.pensize_line[1]))
                turtle.color(random.choice(self.random_color))
                turtle.goto(new_pos[0], new_pos[1])
    def draw_main(self, odd_pos, new_pos, dir): # draw the path
        turtle.goto(odd_pos[0], odd_pos[1]) # reset the position
        turtle.setheading(dir)
        turtle.pd()
        self.generate_line(odd_pos, new_pos)
        self.generate_shape(odd_pos, new_pos)
        turtle.pu()
    def update_pos(self, old_pos, dir, length): # update the position
        def get_2d_vector(yaw, length):
            # Convert the angle to radians
            yaw_rad = math.radians(yaw)

            # Calculate the x and y components of the vector
            x = length * math.sin(yaw_rad)
            y = length * math.cos(yaw_rad)

            # Return the vector as a tuple
            return (x, y)
        # print("dir: ",dir)
        v = get_2d_vector(yaw=dir, length=length)
        # Calculate the new point by adding the vector to the point
        old_pos = [p_i + v_i for p_i, v_i in zip(old_pos, v)]
        # if dir < 0: # find the current facing direction
        #     res = (360 - abs(dir)) % 360
        # else: res = dir % 360
        # match res:
        #     case 0:
        #         old_pos[0] += length
        #     case 45:
        #         old_pos[0] += length * (2 ** 0.5)
        #         old_pos[1] += length * (2 ** 0.5)
        #     case 90:
        #         old_pos[1] += length
        #     case 135:
        #         old_pos[0] -= length * (2 ** 0.5)
        #         old_pos[1] += length * (2 ** 0.5)
        #     case 180:
        #         old_pos[0] -= length
        #     case 225:
        #         old_pos[0] -= length * (2 ** 0.5)
        #         old_pos[1] -= length * (2 ** 0.5)
        #     case 270:
        #         old_pos[1] -= length
        #     case 315:
        #         old_pos[0] += length * (2 ** 0.5)
        #         old_pos[1] -= length * (2 ** 0.5)
        return old_pos
    def is_finish(self): # check if the lifecircle ends
        return True if not bool(self.node_li) or self.index[0] == self.life_circle else False


