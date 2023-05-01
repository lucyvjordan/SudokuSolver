import pygame
import SudokuFunctions
import time



pygame.init()
win = pygame.display.set_mode((500,600))

class sudokuInterface():

    def __init__(self):

        self.sudokufunctions = SudokuFunctions.Sudoku()
        self.quitting = False

        self.font = pygame.font.SysFont('Consolas', 25, bold=False)
        self.textfont = pygame.font.SysFont('Consolas', 16, bold=True)        
        self.boldfont = pygame.font.SysFont('Consolas', 25, bold=True)
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)  
        self.white = (255, 255, 255)
        self.backgroundcolour = (102, 153, 155)  

        self.origin = [25,125]
        # origin is the top left of the grid
        # defines this so that the grisd can be moved without manually changing the location of all drawn elements


    def input(self):
        running = True
        valid = True
        while running:
            pygame.display.set_caption("Sudoku Solver")
            win.fill(self.backgroundcolour)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    valid = True
                    # error message about invalid grid is removed

                    mousex, mousey = pygame.mouse.get_pos()
                    if self.origin[0] < mousex < self.origin[0] + (9*50) and self.origin[1] < mousey < self.origin[1] + (9*50):
                        # if the mouse has been clicked within the grid
                        xposition = int((mousex - self.origin[0]) / 50)
                        yposition = int((mousey - self.origin[1]) / 50)
                        # finds which box is being clicked
                    
                        if self.sudokufunctions.grid[yposition][xposition] == 9:
                            self.sudokufunctions.grid[yposition][xposition] = 0
                            self.sudokufunctions.gridfixed[yposition][xposition] = 0
                            # if it already contains 9, loop back to the start and make the box empty
                        else:
                            self.sudokufunctions.grid[yposition][xposition] += 1
                            self.sudokufunctions.gridfixed[yposition][xposition] = 1
                            # otherwise increase the box value by 1

            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                valid = self.sudokufunctions.checkGrid()
                if valid:
                    return
            # if 's' is pressed and all the entered values follow sudoku rules, the grid is allowed 

            if not valid:
                invalidtext = self.textfont.render("The values you have entered create an invalid grid.", False, self.white)
                invalidtext_rect = invalidtext.get_rect(center=(pygame.display.get_surface().get_width()/2, 100))
                win.blit(invalidtext, invalidtext_rect) 
            # if invalid values have been entered, an error message is shown

            screentext = self.textfont.render("Input your known values, and then press 'S' to solve.", False, self.black)

            self.drawgrid(screentext)

            pygame.display.update()


    def solving(self):
        start_time = time.time()
        solution = self.sudokufunctions.dryrun()

        running = True
        while running:
            pygame.display.set_caption("Sudoku Solver")
            win.fill(self.backgroundcolour)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_c] and not self.sudokufunctions.solving:
                self.resetgrid()

            if not solution:
                self.sudokufunctions.grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]]
                screen_text = self.textfont.render("No Solution. Press 'C' to reset.", False, self.blue)
            # if no solution is found - it has already reset, but this is so that the grid is empty when it shows the 'no solution' message

            else:
                if self.sudokufunctions.solving:
                    self.sudokufunctions.solve()
                    screen_text = self.textfont.render("Solving...", False, self.blue)
                # if the program is in the process of solving the sudoku

                else:
                    screen_text = self.textfont.render("Solution Found. Press 'C' to reset.", False, self.blue)
                    print("time: %s" %(time.time()-start_time))
                # if the program has solved the sudoku


            self.drawgrid(screen_text)

            pygame.display.update()
    

    def drawgrid(self, screen_text):

        title_text = self.font.render("Sudoku Solver", False, self.white)
        title_text_rect = title_text.get_rect(center=(pygame.display.get_surface().get_width()/2, 35))
        win.blit(title_text, title_text_rect)

        for y in range(len(self.sudokufunctions.grid)):
            for x in range(len(self.sudokufunctions.grid[y])):
                # goes through every element of the grid
                box = pygame.draw.rect(win, self.black, (self.origin[0]+(x*50) , self.origin[1]+(y*50), 50, 50), 0)
                win.fill(self.white, box.inflate(-1, -1))

                # draws each elements box
                if self.sudokufunctions.grid[y][x] != 0:
                    if self.sudokufunctions.grid[y][x] != 0:
                        if self.sudokufunctions.gridfixed[y][x] == 1:
                            text = self.boldfont.render(str(self.sudokufunctions.grid[y][x]), False, self.black)
                        else:
                            text = self.font.render(str(self.sudokufunctions.grid[y][x]), False, self.black)
                        # the number will be bold if it is fixed
                    text_rect = text.get_rect(center=(self.origin[0]+25+(x*50) , self.origin[1]+25+(y*50)))
                    win.blit(text, text_rect)
                    # draws each elements number if it is not supposed to be empty

        for y in range(3):
            for x in range(3):
                pygame.draw.rect(win, self.black, (self.origin[0]+(x*150), self.origin[1]+(y*150), 150, 150), 4)
                # draws the thicker 3x3 boxes

        screen_text_rect = screen_text.get_rect(center=(pygame.display.get_surface().get_width()/2, 75))
        win.blit(screen_text, screen_text_rect)


    def resetgrid(self):
        # resets the grid to empty
        self.sudokufunctions = SudokuFunctions.Sudoku()
        sudoku.input()
        sudoku.solving()


if __name__ == "__main__":
    # this is true when the program starts running
    sudoku = sudokuInterface()
    sudoku.resetgrid()
    # keeps the menu running