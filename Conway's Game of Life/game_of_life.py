'''
Copyright 2018 LiquidFox1776 LiquidFox1776@gmail.com
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Python Version:    3.x
License:           MIT
Description:  A simple implementation of Conway's Game of Life
'''

import pygame
import random

def debug_print(string) :
        '''
	used to print debug strings
        '''
        if 1==0 :
                print(string)
        
def in_bounds(list_to_check, index) :
        '''
	checks if an index is within the bounds of a list
        '''
        if (index > -1) and (index < len(list_to_check)) :
                return True
        else :
                return False
    
class Cell :
        '''
	basic unit inside of the game
        '''
        width = 10 # width of the cell
        height = 10 # height of the cell
        alive_color = (0,255,0) # green
        dead_color = (0,0,0) # black
    
        def __init__(self,x,y) :
                self.x = x
                self.y = y
                self.alive = False

        def draw_cell(self,screen) :
                '''
                draws either a living or dead cell
                '''
                if self.alive == True :
                    pygame.draw.rect(screen,
                                     self.alive_color,
                                     pygame.Rect(self.x, self.y, self.width, self.height)) # draw a 'live' cell
                else :
                    pygame.draw.rect(screen,
                                     self.dead_color,
                                     pygame.Rect(self.x, self.y, self.width, self.height)) # draw a 'dead' cell
        def kill_cell(self) :
                self.alive = False

        def revive_cell(self) :
                self.alive = True

        def is_alive(self) :
                return self.alive
        

class World :
        '''
        our drawing board
        '''
        def __init__(self, width, height) :
                self.width = width # screen width
                self.height = height # screen height
                self.screen = None
                self.finished = False
                self.cells = [] # holds a list of Cell objects
    
                try :
                    self.row_width = int(self.width / Cell.width)
                    if float(self.row_width).is_integer() == False :
                        raise('Error initializing world')
                except :
                    raise('Error initializing world')
            
        def create(self) :
                for y in range(0,self.height, Cell.height): # populate board
                    for x in range(0,self.width, Cell.width):
                        self.cells.append(Cell(x,y))
                        if random.randint(0,1) == 1 : # randomly set a cell to either be living or dead
                            self.cells[-1].alive = True
                        else :
                            self.cells[-1].alive = False
                
                pygame.init()
                self.screen = pygame.display.set_mode((self.width, self.height))
    
        def draw_cells(self):
                '''
		iterate over all of the cells and draw them
                '''
                for cell in self.cells :
                    cell.draw_cell(screen=self.screen)

        def get_neighbor_count(self, index) :
                '''
		counts the number of living neighbors adjacent to a cells position
		TODO might refactor later
                '''
                nc = 0 # neighbor count
                x = self.cells[index].x
                y = self.cells[index].y

                
                if (in_bounds(self.cells, index - 1) and
                (self.cells[index - 1].y == y) and
                (self.cells[index - 1].x == x - Cell.width) and
                (self.cells[index - 1].alive == True)) : # left
                    debug_print('LEFT')
                    nc += 1
          
                if (in_bounds(self.cells, index + 1) and
                    (self.cells[index + 1].y == y) and
                    (self.cells[index + 1].x == x + Cell.width) and
                    (self.cells[index + 1].alive == True)): # right
                    debug_print('RIGHT')
                    nc += 1

                if (in_bounds(self.cells, index - self.row_width) and
                    (self.cells[index - self.row_width].x == x) and
                    (self.cells[index - self.row_width].y == y - Cell.height) and
                    (self.cells[index - self.row_width].alive == True)): # top
                    debug_print('TOP')
                    nc += 1
                    
                if (in_bounds(self.cells, index - self.row_width - 1) and
                    (self.cells[index - self.row_width - 1].x == x - Cell.width) and
                    (self.cells[index - self.row_width - 1].y == y - Cell.height) and
                    (self.cells[index - self.row_width - 1].alive == True)): # top left
                    debug_print('TOP LEFT')
                    nc += 1
                    
                if (in_bounds(self.cells, index - self.row_width + 1) and
                    (self.cells[index - self.row_width + 1].x == x + Cell.width) and
                    (self.cells[index - self.row_width + 1].y == y - Cell.height) and
                    (self.cells[index - self.row_width + 1].alive == True)): # top right
                    debug_print('TOP right')
                    nc += 1
                    
                if (in_bounds(self.cells, index + self.row_width) and
                    (self.cells[index + self.row_width].x == x) and
                    (self.cells[index + self.row_width].y == y + Cell.height) and
                    (self.cells[index + self.row_width].alive == True)): # bottom
                    debug_print('BOTTOM')
                    nc += 1
                    
                if (in_bounds(self.cells, index + self.row_width - 1) and
                    (self.cells[index + self.row_width - 1].x == x - Cell.width) and
                    (self.cells[index + self.row_width - 1].y == y + Cell.height) and
                    (self.cells[index + self.row_width - 1].alive == True)): # bottom left
                    debug_print('BOTTOM LEFT')
                    nc += 1
                    
                if (in_bounds(self.cells, index + self.row_width + 1) and
                    (self.cells[index + self.row_width + 1].x == x + Cell.width) and
                    (self.cells[index + self.row_width + 1].y == y + Cell.height) and
                    (self.cells[index + self.row_width + 1].alive == True)): # bottom right
                    debug_print('BOTTOM RIGHT')
                    nc += 1

                return nc
    
        def update_cells(self) :
                '''
		updates the living and dead status of a cell
                        '''
                tmp_cells = []

                
                for index in range(0,len(self.cells)) : # loop to create a temporary copy of the current living and dead states of every cell
                    tmp_cells.append(self.cells[index].alive)
                    nc = self.get_neighbor_count(index)

                    if nc < 2 : # dies as if by underpopulation
                        tmp_cells[index] = False
                    #elif (nc == 2) or (nc ==3) : # lives on to the next generation
                    #    tmp_cells[index].alive = True # if statement included just to list all of the rules
                    elif nc > 3 : # dies as if by overpopulation
                        tmp_cells[index] = False
                    elif nc == 3 : # comes back to life as if by reproduction
                        tmp_cells[index] = True
                
                for i in range(0,len(self.cells)) :  # transfer the cell state to the cells 
                    self.cells[i].alive = tmp_cells[i]
            
        def run(self) :
                '''
		runs the game of life
                '''
                while not self.finished: # loop intil we get a QUIT signal
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.finished = True
                            pygame.quit()
                    
                    self.draw_cells() # draws the world
                    pygame.display.flip() # updates the screen
                    self.update_cells() # calculate the next generation
            

if __name__ ==  '__main__' :
        world = World(600,600) # Width, Height of the world/screen
        world.create() # create / initialize the world
        world.run() # run the world
