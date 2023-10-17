import tkinter
import tkinter.font
from PIL import Image, ImageTk
from collections import deque

root = tkinter.Tk()
root.title("Maze Visualizer")
root.resizable(False, False)
root.geometry("850x550")

canvas = tkinter.Canvas(
    width=850,
    height=550,
    bg="alice blue"
)
canvas.place(x=0,y=45)
#canvas.pack()

#--------------------------help-------------------------#

def help():
    newWindow = tkinter.Toplevel(root, width=550, height=735)
    photo = tkinter.PhotoImage(file='help.png')
    canvas2 = tkinter.Canvas(newWindow, width=550, height=735)
    canvas2.place(x=0, y=0)
    canvas2.create_image(0, 0, image=photo, anchor=tkinter.NW)
    newWindow.mainloop()


btn_help = tkinter.Button(
    text="Help",
    font=("Times New Roman", 18),
    width=10,
    command=help,
)

btn_help.place(x=0, y=0)
#--------------------------------------------------------#
#-------------------------rest--------------------------#

def reset():
    for y in range(1,11):
        for x in range(1,21):
            tag = str(y)+'-'+str(x)
            color = canvas.itemcget(tag, 'fill')
            if color == 'orange':
                canvas.itemconfig(tag, fill='white')

btn_reset = tkinter.Button(
    text="Reset",
    font=("Times New Roman", 18),
    width=10,
    command=reset,
)

btn_reset.place(x=140, y=0)

#--------------------------------------------------------#
#------------------------allreset------------------------#

def allreset():
    global s_flag
    global g_flag
    
    for y in range(1,11):
        for x in range(1,21):
            tag = str(y)+'-'+str(x)
            canvas.itemconfig(tag, fill="white")
            maze[y-1][x-1] = 0
    
    s_flag = 0
    g_flag = 0

btn_allreset = tkinter.Button(
    text="All Reset",
    font=("Times New Roman", 18),
    width=10,
    command=allreset,
)

btn_allreset.place(x=280, y=0)

#-------------------------------------------------------#
#--------------------------Reverse-------------------------#

def reverse():
    for y in range(1,11):
        for x in range(1,21):
            tag = str(y)+'-'+str(x)
            color = canvas.itemcget(tag, 'fill')
            if color == 'white' or color == 'gray':
                if maze[y-1][x-1] == 1:
                    canvas.itemconfig(tag, fill='white')
                    maze[y-1][x-1] = 0
                elif maze[y-1][x-1] == 0:
                    canvas.itemconfig(tag, fill='gray')
                    maze[y-1][x-1] = 1
            elif color == 'orange':
                canvas.itemconfig(tag, fill='white')

btn_reset = tkinter.Button(
    text="Reverse",
    font=("Times New Roman", 18),
    width=10,
    command=reverse,
)

btn_reset.place(x=420, y=0)

#--------------------------------------------------------#

#------------------------exe-----------------------------#
def exe():
    global exe_flag
    exe_flag = 1
    sx, sy, gx, gy = 0, 0, 0, 0
    if s_flag == 0 or g_flag == 0:
        terminal['fg'] = 'red'
        terminal['text'] = 'Set start and goal point.'
        exe_flag = 0
        return

    for i in range(10):
        for j in range(20):
            if maze[i][j] == 2:
                sy = i
                sx = j
            elif maze[i][j] == 3:
                gy = i
                gx = j
            
            tag = str(i+1) + '-' + str(j+1)
            color = canvas.itemcget(tag, 'fill')
            if color == 'orange':
                canvas.itemconfig(tag, fill='white')
    
    dist = [[10**3 for _ in range(20)] for _ in range(10)]
    dist[sy][sx] = 0
    que = deque()
    que.append([sy, sx])
    d = [[1,0], [-1,0], [0,1], [0,-1]]

    while que:
        y, x = que.popleft()
        
        for i, j in d:
            if y+i >= 10 or y+i < 0 or x+j >= 20 or x+j < 0:
                continue
            if maze[y+i][x+j] == 1:
                continue
            if dist[y+i][x+j] != 10**3:
                continue

            dist[y+i][x+j] = dist[y][x]+1
            que.append([y+i, x+j])
    
    if dist[gy][gx] == 10**3:
        terminal['fg'] = 'lime green'
        terminal['text'] = 'Unreachable'
        exe_flag = 0
        return
    else:
        terminal['fg'] = 'lime green'
        terminal['text'] = 'The shortest route, which is indicated by orange squares  is ' + str(dist[gy][gx]) + ' steps.'

    terminal.update()
    now = [gy, gx]
    
    while now != [sy, sx]:
        y, x = now
        for i, j in d:
            if 0 <= y+i <= 9 and 0 <= x+j <= 19:
                if dist[y+i][x+j] == dist[y][x]-1:
                    now = [y+i, x+j]
                    if now == [sy, sx]:
                        exe_flag = 0
                    else:
                        tag = str(y+i+1)+'-'+str(x+j+1)
                        canvas.itemconfig(tag, fill="orange")
                    break
        



btn_exe = tkinter.Button(
    text="Execute",
    font=("Times New Roman", 18),
    width=10,
    command=exe,
)

btn_exe.place(x=560, y=0)
#--------------------------------------------------------#

terminal = tkinter.Label(
    text="You could change the wall or the aisle by pressing <B>.",
    font=("Times New Roman", 18),
    bg="gray20",
    fg="lime green",
    width=65,
    height=2,
)

terminal.place(x=0, y=45)

maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,0,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,0,1,1],
    [1,0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,1,0,1,1],
    [1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,1,1,1,0,0,1,1,1,1,0,1,1,1,0,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,0,1,1,1,1],
    [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

arr = []

for y in range(10):
    for x in range(20):
        if maze[y][x] == 1:
            canvas.create_rectangle(
                (x+0.5)*40,
                (y+2)*40,
                (x+0.5)*40+40,
                (y+2)*40+40,
                fill="gray",
                #width=3,
                tag=str(y+1)+'-'+str(x+1),
            )
        elif maze[y][x] == 0:
            canvas.create_rectangle(
                (x+0.5)*40,
                (y+2)*40,
                (x+0.5)*40+40,
                (y+2)*40+40,
                fill="white",
                #width=3,
                tag=str(y+1)+'-'+str(x+1),
            )

canvas.create_rectangle(
    (0.5)*40,
    (2)*40,
    (0.5)*40+40,
    (2)*40+40,
    width=3,
    outline="magenta",
    tag="aaa",
)

def focus2tags():
    loc = canvas.bbox("aaa")
    loc = list(loc)
    ids = canvas.find_enclosed(*loc)
    tags = []
    for id in ids:
        tags.append(canvas.itemcget(id, "tag"))

    return tags

def lclick(event):
    x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    
    l = [canvas.itemcget(obj, 'tags') for obj in canvas.find_overlapping(x,y,x,y)]
    space = l[0].find(' ')
    if space == -1:
        return
    nxt = l[0][:space]
    loc = canvas.bbox(nxt)
    canvas.delete('aaa')
    canvas.create_rectangle(
        *loc,
        width=3,
        outline="magenta",
        tag="aaa",
    )

s_flag = 0
g_flag = 0
exe_flag = 0

def key_handler(e):
    global s_flag
    global g_flag
    global exe_flag

    if exe_flag == 1:
        return

    if e.keycode == 66: #b
        now = focus2tags()[0]
        space = now.find(' ')
        if space != -1:
            now = now[:space]
        hyphen = now.find('-')
        y = int(now[:hyphen])-1
        x = int(now[hyphen+1:])-1
        if maze[y][x] == 1:
            maze[y][x] = 0
            canvas.itemconfig(now, fill="white")
        elif maze[y][x] == 0:
            maze[y][x] = 1
            canvas.itemconfig(now, fill="gray")
    
    elif e.keycode == 83: #start
        now = focus2tags()[0]
        space = now.find(' ')
        if space != -1:
            now = now[:space]
        hyphen = now.find('-')
        y = int(now[:hyphen])-1
        x = int(now[hyphen+1:])-1
        if maze[y][x] == 0:
            if s_flag == 0:
                s_flag = 1
                maze[y][x] = 2
                canvas.itemconfig(now, fill="blue")
        elif maze[y][x] == 2:
            s_flag = 0
            maze[y][x] = 0
            canvas.itemconfig(now, fill="white")

    elif e.keycode == 71: #goal
        now = focus2tags()[0]
        space = now.find(' ')
        if space != -1:
            now = now[:space]
        hyphen = now.find('-')
        y = int(now[:hyphen])-1
        x = int(now[hyphen+1:])-1
        if maze[y][x] == 0:
            if g_flag == 0:
                g_flag = 1
                maze[y][x] = 3
                canvas.itemconfig(now, fill="red")
        elif maze[y][x] == 3:
            g_flag = 0
            maze[y][x] = 0
            canvas.itemconfig(now, fill="white")

    elif e.keycode == 37: #left
        now = focus2tags()[0]
        space = now.find(' ')
        if space != -1:
            now = now[:space]
        loc = list(canvas.bbox(now))
        canvas.delete("aaa")
        loc[0] -= 40
        if loc[0] < 19:
            loc[0] = 780
        loc[2] = loc[0]+40
        canvas.create_rectangle(
            *loc,
            width=3,
            outline="magenta",
            tag="aaa",
        )
    elif e.keycode == 39: #right
        now = focus2tags()[0]
        space = now.find(' ')
        if space != -1:
            now = now[:space]
        loc = list(canvas.bbox(now))
        canvas.delete("aaa")
        loc[0] += 40
        if loc[0] > 781:
            loc[0] = 20
        loc[2] = loc[0]+40
        canvas.create_rectangle(
            *loc,
            width=3,
            outline="magenta",
            tag="aaa",
        )
    elif e.keycode == 38: #top
        now = focus2tags()[0]
        space = now.find(' ')
        if space != -1:
            now = now[:space]
        loc = list(canvas.bbox(now))
        canvas.delete("aaa")
        loc[1] -= 40
        if loc[1] < 79:
            loc[1] = 440
        loc[3] = loc[1]+40
        canvas.create_rectangle(
            *loc,
            width=3,
            outline="magenta",
            tag="aaa",
        )
    elif e.keycode == 40: #down
        now = focus2tags()[0]
        space = now.find(' ')
        if space != -1:
            now = now[:space]
        loc = list(canvas.bbox(now))
        canvas.delete("aaa")
        loc[1] += 40
        if loc[1] > 441:
            loc[1] = 80
        loc[3] = loc[1]+40
        canvas.create_rectangle(
            *loc,
            width=3,
            outline="magenta",
            tag="aaa",
        )

root.bind("<KeyPress>", key_handler)
canvas.bind('<Button-1>', lclick)
root.mainloop()