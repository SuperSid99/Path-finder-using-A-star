import random
import math
import numpy as np

class bcolors:
    DEST = '\033[92m' #GREEN
    SRC = '\033[93m' #YELLOW
    PATH = '\033[91m' #RED
    SPACES='\033[97m' #WHITE
    WALLS='\033[96m' #light cyan
    RESET = '\033[0m' #RESET COLOR
    NO_PATH='\033[95m' #PURPLE

def Get_Input():
    while True:
        grid_x = int(input('\nenter no. of rows(less than 20):'))
        grid_y = int(input('\nenter no. of cols(less than 20):'))
        
        if grid_x <= 20 and grid_y <= 20:
            break
        else:
            print("\nplease enter a grid of less thatn 20x20")
    return(grid_x,grid_y)
    
def Create_Grid(grid_x,grid_y):
    a=[]
    b=[]
    
    for x in range(grid_y):
        a.append(x)
    for y in range(grid_x):
        b.append(a)
    return b


def Get_Goal_Cord(grid_x,grid_y):
    
    while True:
        
        g_x_cord = (int(input('\nenter the x coordinate of goal (between 1 and no of rows)  '))-1)
        g_y_cord = (int(input('\nenter the y coordinate of goal (between 1 and no of cols)  '))-1)
        
        if g_x_cord <= grid_x and g_y_cord <= grid_y and 0 <= g_x_cord and 0 <= g_y_cord:
            break
        else:
            print("\nplease enter a Coordinate within the grid")
    
    return(g_x_cord,g_y_cord)



def Get_Start_Cord(grid_x,grid_y):
    
    while True:
        s_x_cord = (int(input('\nenter the x coordinate of start (between 1 and no of rows)  '))-1)
        s_y_cord = (int(input('\nenter the y coordinate of start (between 1 and no of cols)  '))-1)

        if s_x_cord <= grid_x and s_y_cord <= grid_y and 0 <= s_x_cord and 0 <= s_y_cord:
            break
    else:
        print("\nplease enter a Coordinate within the grid")

    return(s_x_cord,s_y_cord)
    


def Get_Walls(g_x_cord,g_y_cord):
    Replay='bhbhb'
    walls=[]
    while not (Replay=='YES' or Replay=='NO'):
        Replay=input('\nDo you want random walls? (yes/no) :').upper()
    if Replay=='YES' :

        
        blocks = int(input('\nhow many blocks do you want?: '))
        for r in range(blocks):
            block_wall = random.randint(0,grid_x-1), random.randint(0,grid_y-1)
            walls.append(block_wall)
    
    else:
        while True:
            w_x_cord = int(input('\nenter the x coordinate of wall  '))
            w_y_cord = int(input('\nenter the y coordinate of wall  '))
            
            if w_x_cord <= grid_x and w_y_cord <= grid_y and 0 <= w_x_cord and 0 <= w_y_cord and w_x_cord != g_x_cord and w_y_cord != g_y_cord:
                walls.append((w_x_cord,w_y_cord))
                ssup=input('\nDo you want to add more walls? (yes/no) :').upper()
                if ssup=='YES' :
                    pass
                else:
                    break
                
            else:
                print("\nplease enter a Coordinate within the grid")
    return(walls)

def Get_Heuristic(b,g_x_cord,g_y_cord):
    docfg={}
    for x in range(len(b)):
        x_dist = (g_x_cord-x)
        for y in range(len(b[x])):
            y_dist = (g_y_cord-y)
            docfg[x,y]=abs(x_dist)+abs(y_dist)
    return(docfg)


def check_in_wall(x,y):
    # checks if the next state is a wall or not
    if (x,y) in walls:
        pass
    else:
        return(x,y)

def expand(x,y):
    # gives the next states
    a=[]
    if y!=0:
        if check_in_wall(x,y-1) != None :
            a.append(check_in_wall((x,y-1),(x,y)))
    if y!=grid_y-1:
        if check_in_wall(x,y+1) != None :
            a.append(check_in_wall((x,y+1),(x,y)))
    if x!=0:
        if check_in_wall(x-1,y) != None :
            a.append(check_in_wall((x-1,y),(x,y)))
    if x!=grid_x-1:
        if check_in_wall(x+1,y) != None :
            a.append(check_in_wall((x+1,y),(x,y)))
    return(a)

def Sort_Tuple(tup): 
    
    return(sorted(tup, key = lambda x: x[1]))

def calculate_f(x,y,g,x_old,y_old):
    g_new=g+1
    h= docfg[x,y]
    docfg[x,y]=docfg[x,y]+5;
    f=g+h
    return(((x,y),(x_old,y_old)),f,g_new)

def goal_test(x,y):
    if x==g_x_cord and y==g_y_cord:
        goal=True
        return('Goal has been reached')
    else:
        return(expand(x,y))
    
    
def Get_Path(s_x_cord,s_y_cord,docfg):
    frontier=[(((s_x_cord,s_y_cord),(-1,-1)),docfg[s_x_cord,s_y_cord],0)]
    goal=False
    path=[]
    count=0
    while ((goal==False and count<2000) and len(frontier)>0):
        hold = goal_test(frontier[0][0][0][0],frontier[0][0][0][1])
        if type(hold)== str:
            print("Yay The Goal Has been Reached")
            count=count+1
            path.append(frontier[0])
            frontier.pop(0)
            goal=True
        else:
            for _ in hold:
                frontier.append(calculate_f(_[0][0],_[0][1],frontier[0][2],_[1][0],_[1][1]))
            count=count+1
            path.append(frontier[0])
            frontier.pop(0)
            frontier=Sort_Tuple(frontier)
    if count==2000 or len(frontier)==0:
        path = "no path found"
    else:
        path.reverse()
    return(path)


def Get_Way(g_x_cord,g_y_cord,path):
    
    if type(path)== str:
        way=path
    else:
        way=[(g_x_cord,g_y_cord)]
        _=0
        while path[_][0][1]!=(-1, -1):
            if path[_][0][1]==path[_+1][0][0]:
                way.append(path[_+1][0][0])
                _=_+1
            else:
                path.pop(_+1)
    return(way)


def meshMaze(grid_x,grid_y,g_x_cord,g_y_cord,s_x_cord,s_y_cord,walls):
    

    x = np.linspace(1, 1, grid_y)
    y = np.linspace(1, 1, grid_x)

    maze, solved_maze = np.meshgrid(x, y)

    maze[g_x_cord][g_y_cord] = 8;
    maze[s_x_cord][s_y_cord] = 0;

    a=0
    for i in range(len(walls)):
        maze[walls[a][0]][walls[a][1]] = 4
        a=a+1

    return (maze)

def edit_Maze(solved_maze,way,b):
    if type(way)==str:
        for _ in range (len(b)):
            for yo in range (len(b[_])):
                solved_maze[_][yo]=7
        print(f"{bcolors.PATH} NO PATH FOUND {bcolors.RESET}")
                
    else:
        way.pop(0)
        way.pop(-1)
        for x in range(len(way)):
            solved_maze[way[x][0]][way[x][1]] = 5
    return (solved_maze)

def Print_Maze(print_maze):
    var=[]
    if type(print_maze)==str:
        pass
    else:
        ans = []
        
        i = 0
        count=0

        for a in range(len(print_maze)):
            for i in range(len(print_maze[a])):
                k = print_maze[a][i]
                if print_maze[a][i] == 1:
                    k=(f"{bcolors.SPACES}   {bcolors.RESET}")
                elif print_maze[a][i] == 4:
                    k =(f"{bcolors.WALLS} # {bcolors.RESET}")
                elif print_maze[a][i] == 0:
                    k =(f"{bcolors.SRC} S {bcolors.RESET}")
                elif print_maze[a][i] == 8:
                    k=(f"{bcolors.DEST} D {bcolors.RESET}")
                elif print_maze[a][i] == 5:
                    k=(f"{bcolors.PATH} * {bcolors.RESET}")
                elif print_maze[a][i] == 7:
                    k=(f"{bcolors.NO_PATH} X {bcolors.RESET}")
                ans.append(k)
                count+=1
                if count == grid_y:   
                    var.append(ans)
                    ans=[]
                    count=0
        return (var)   

    


#taking input
(grid_x,grid_y) = Get_Input()
b = Create_Grid(grid_x,grid_y)
(g_x_cord,g_y_cord) = Get_Goal_Cord(grid_x,grid_y)
(s_x_cord,s_y_cord)=Get_Start_Cord(grid_x,grid_y)
walls = Get_Walls(g_x_cord,g_y_cord)

#creating maze in the form of meshgrid
initial_maze = meshMaze(grid_x,grid_y,g_x_cord,g_y_cord,s_x_cord,s_y_cord,walls);

#converting it to colored
c_initial_maze = Print_Maze(initial_maze)
#printing maze
for i in c_initial_maze:   
    str1 = "" 
    for ele in i: 
        str1 += ele  
    print(str1) 

#dictionary of all points and their distances from goals
docfg= Get_Heuristic(b,g_x_cord,g_y_cord)

path=Get_Path(s_x_cord,s_y_cord,docfg)

way=Get_Way(g_x_cord,g_y_cord,path)

solved_maze = edit_Maze(initial_maze,way,b)

solution=Print_Maze(solved_maze)

for i in solution:   
    str1 = "" 
    for ele in i: 
        str1 += ele  
    print(str1) 
