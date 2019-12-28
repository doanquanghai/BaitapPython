import math
import random
import pygame
import tkinter as tk
import turtle
from tkinter import messagebox



class cube(object):
    rows = 20
    w = 600
    def __init__(self,start,dirnx=1,dirny=0,color=(0,0,128)):
        #ban đầu dinx là 1  để khối đi từ đầu và không cần nhấp
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
 
       
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        #thay đổi vị trí tùy theo hướng di chuyển.
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
 
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        #+1 và -2 điểm là để xem các đường các hình khối của cơ thể rắn
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            #vẽ mắt không cần xD và màu các kiểu...
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
       
 
 
 
class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        #append head muôn thêm vào vị trí cuối cùng của body
        self.dirnx = 0
        self.dirny = 1
     #hàm dịch chuyển rắn
    def move(self):
        for event in pygame.event.get():
            #nhận sự kiện từ hàng đợi
            if event.type == pygame.QUIT:
                #lấy giá trị của thuộc tính type của dt eventvaf kiểm tra xem có bằng
                #với hằng số dc định nghĩa pygame.Quit
                pygame.quit()
 
            keys = pygame.key.get_pressed()
            #trạng thái từ các nut bàn phím
            
        #hướng di chuyen được xác đinh tùy thuộc vào nút
 
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
        for i, c in enumerate(self.body):#ham
            p = c.pos[:] #định vị các khối lập phương trong cơ thể rắn
            if p in self.turns:#nếu có một góc trong vị trí khối này
                turn = self.turns[p]
                c.move(turn[0],turn[1])#xoắn khối lập phương
                if i == len(self.body)-1:
                    self.turns.pop(p)
                    #sau tất cả các hình khối sẽ sắp vào vị trị cuối đẻ không cặn 
            else:
                #kiểm tra nó có giống trên ko nếu không thì tiến hành di chuyển
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)
    

    
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
 
 
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        #thêm khối lập phương vào vị trí hướng của đuôi
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
 
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
       
 
    def draw(self, surface):
        #vẽ mắt
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)#nếu đầu thì vẽ mắt
            else:
                c.draw(surface)#vẽ một hình khối lập phương
 
 
def drawGrid(w, rows, surface):
    #vẽ ma trận 
    #tham số hàng và cột
    sizeBtwn = w // rows
    #chia khoogn có phần thập phân
    #khoảng cách giữa mỗi dòng
  
    x = 0
    y = 0
    for l in range(rows):
        #Trong pham vi 20
        x = x + sizeBtwn
        y = y + sizeBtwn

        #màu cho ma trân lưới đen
        pygame.draw.line(surface, (0,0,0), (x,0),(x,w))
        pygame.draw.line(surface, (0,0,0), (0,y),(w,y))
       
 
def redrawWindow(surface):
    #Tạo bảng window
    global rows, width, s, snack
    #sửa biến toàn cục
    surface.fill((255,255,255))#bẩng trắng
    #tạo ra bảng màu nền
    s.draw(surface)
    snack.draw(surface)#vẽ đồ ăn của rắn
    drawGrid(width,rows, surface)
    #gọi lên drawGrid để tạo ra lưới
    pygame.display.update()
 
 
def randomSnack(rows, item):
 
    positions = item.body
 
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        #kiểm tra xem có nằm trong thân rắn ko?
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
       
    return (x,y)
 
 
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
 
 
def main():
    global width, rows, s, snack
    width = 600
    rows = 20
    win = pygame.display.set_mode((width, width))
    #tao ma trân ô

    score =0
    s = snake((255,0,0), (0,0))
    snack = cube(randomSnack(rows, s), color=(0,0,0))#màu khối
    #thêm cude nơi ngẫu nhiên để bắt đầu
    flag = True
 
    clock = pygame.time.Clock()
    #tạo một đối tượng để quản lí thời gian.
   
    while flag:
        pygame.time.delay(50)#càng nhiều thì chạy càng nhanh.......
        
        clock.tick(8)#cập nhật đồng hồ #càng ít, càng chậm lai...
        s.move()
        if s.body[0].pos == snack.pos:#để kiếm ăn
            s.addCube()#add vào
            snack = cube(randomSnack(rows, s), color=(0,255,0))#khối ngẫu nhiên mới
            #add vô thì thành lại màu xanh
    
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                #kiểm tra xem nó đả vào body chưa
                print('Score: ', len(s.body))
                message_box('Ban da thua!', 'Choi lai...')
                s.reset((10,10))
                break
 
           
        redrawWindow(win)
        #vẽ ma trận....
 
       
 
 
 
main()

