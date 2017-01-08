import pygame,random,sys,math,Tkinter,tkFileDialog,copy
import pygame._view
from pygame.locals import *

WINWIDTH=640
WINHEIGHT=480
WINSIZE=(WINWIDTH,WINHEIGHT)
WINCENTER=(320,240)
NUMSTARS=150

#set up colors
BLACK=(0,  0,  0)
WHITE=(255,255,255)
YELLOW=(255,255,0)
RED=(255,   0,  0)
GREEN=( 0,255,  0)
BLUE=(  0,  0,255)
TRANSP_WHITE=(255,255,255, 0)
ORANGE=(250,100,50)
LOAD_BG=( 150,250,50)
PLAY_BG=(250,150,250)

#images
red_button=pygame.image.load('red_button.jpeg')
blue_button=pygame.image.load('blue_button.jpeg')
yellow_button=pygame.image.load('yellow_button.jpeg')


def terminate():
    pygame.quit()
    sys.exit()

def highlight(rect,color,width):
    pygame.draw.rect(SURFACE,color,rect,width)

def init_stars(wincenter):
    vel=25
    current_position=[wincenter for i in range(NUMSTARS)]
    return current_position,vel

def draw_stars(current_position,color):
    for current in current_position:
        if current[0]<WINWIDTH and current[1]<WINHEIGHT:
            SURFACE.set_at(current,color)
    

def move_stars(current_position,vel,color):
    angles=random.sample([i for i in range(360)],NUMSTARS)
    for angle in angles:
        angle=(angle*2.0*math.pi/180)
    draw_stars(current_position,color)
    next_position=[(int(current_position[i][0]+(vel*math.cos(angles[i]))),int(current_position[i][1]+(vel*math.sin(angles[i])))) for i in range(NUMSTARS)]
    return next_position

def start_animation(game_started):
    highlight_width=3
    mouseClicked=0
    sound_stopped=0
    wincenter=WINCENTER
    mousex,mousey=(0,0)
    font1_path=pygame.font.match_font('verdana',bold=True,italic=True)
    font2_path=pygame.font.match_font('timesnewroman',bold=True)
    fontObj1=pygame.font.Font(font1_path,40)
    fontObj2=pygame.font.Font(font2_path,20)
    fontObj1.set_italic(20)
    scrambler_txt=fontObj1.render('SCRAMBLER',True,YELLOW,WHITE)
    scrambler_txt.set_colorkey(WHITE)
    scrambler_txt.convert_alpha()
    new_game_txt=fontObj2.render('NEW GAME',True,YELLOW,WHITE)
    new_game_txt.set_colorkey(WHITE)
    new_game_txt.convert_alpha()
    quit_txt=fontObj2.render('QUIT',True,YELLOW,WHITE)
    quit_txt.set_colorkey(WHITE)
    quit_txt.convert_alpha()

    sound_img=pygame.image.load('sound_img.jpeg')
    sound_img=pygame.transform.scale(sound_img,(35,35))
    sound_img_rect=sound_img.get_rect(bottomright=(WINWIDTH-20,WINHEIGHT-20))
    scrambler_rect=scrambler_txt.get_rect(midbottom=(WINWIDTH/2,WINHEIGHT/2))
    new_game_rect=new_game_txt.get_rect(midtop=(WINWIDTH/2,(WINHEIGHT/2+80)))
    quit_rect=quit_txt.get_rect(midtop=(WINWIDTH/2,(WINHEIGHT/2+160)))
    current_position,vel=init_stars(wincenter)
    draw_stars(current_position,WHITE)
    while game_started==0:
        SURFACE.fill(BLACK)
        SURFACE.blit(scrambler_txt,scrambler_rect)
        SURFACE.blit(new_game_txt,new_game_rect)
        SURFACE.blit(quit_txt,quit_rect)
        SURFACE.blit(sound_img,sound_img_rect)
        current_position=move_stars(current_position,vel,WHITE)
        
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            elif event.type==MOUSEMOTION:
                mousex,mousey=event.pos
            elif event.type==MOUSEBUTTONUP:
                mousex,mousey=event.pos
                if new_game_rect.left<mousex<new_game_rect.right and new_game_rect.top<mousey<new_game_rect.bottom:
                    game_started=1
                elif quit_rect.left<mousex<quit_rect.right and quit_rect.top<mousey<quit_rect.bottom:
                    terminate()
                elif sound_img_rect.collidepoint(mousex,mousey):
                    if sound_stopped==0:
                        pygame.mixer.music.pause()
                        sound_stopped=1
                    elif sound_stopped==1:
                        pygame.mixer.music.unpause()
                        sound_stopped=0
                elif mousex<WINWIDTH and mousey<WINHEIGHT:
                    mouseClicked=1
                    wincenter=(mousex,mousey)
                    
        if new_game_rect.left<mousex<new_game_rect.right and new_game_rect.top<mousey<new_game_rect.bottom:
            highlight(new_game_rect,BLUE,highlight_width)
        elif quit_rect.left<mousex<quit_rect.right and quit_rect.top<mousey<quit_rect.bottom:
            highlight(quit_rect,BLUE,highlight_width)
        elif sound_img_rect.collidepoint(mousex,mousey):
            highlight(sound_img_rect,BLUE,highlight_width)
        if mouseClicked==1:
            current_position,vel=init_stars(wincenter)
            mouseClicked=0
        if sound_stopped==1:
            pygame.draw.line(SURFACE,RED,(sound_img_rect.left+4,sound_img_rect.top+4),(sound_img_rect.right-4,sound_img_rect.bottom-4),3)
            pygame.draw.line(SURFACE,RED,(sound_img_rect.right-4,sound_img_rect.top+4),(sound_img_rect.left+4,sound_img_rect.bottom-4),3)
        pygame.display.update()
        fpsClock.tick(FPS)
    return game_started

def load_image(image_loaded):
    mousex,mousey=(0,0)
    selected=0
    margin=20
    r=10
    load_new=0
    browse=0
    pic_file=''
    level=0
    path=0
    typing_txt=0
    game_started=1
    type_rect=pygame.Rect(0,0,0,0)
    picture=pygame.Surface((0,0))
    
    font3_path=pygame.font.match_font('centurygothic',bold=True,italic=True)
    font4_path=pygame.font.match_font('timesnewroman',bold=True)
    font5_path=pygame.font.match_font('centuryschoolbook')
    fontObj3=pygame.font.Font(font3_path,20)
    fontObj4=pygame.font.Font(font4_path,16)
    fontObj5=pygame.font.Font(font5_path,14)
    
    image_txt=fontObj3.render('Choose image:',True,BLACK,WHITE)
    
    example_txt=fontObj4.render('Play an example',True,BLACK,WHITE)
    load_new_txt=fontObj4.render('Load new image',True,BLACK,WHITE)
    browse_txt=fontObj4.render('...',True,BLACK,WHITE)

    difficulty_txt=fontObj3.render('Choose difficulty:',True,BLACK,WHITE)

    easy_txt=fontObj4.render('Easy',True,BLACK,WHITE)
    medium_txt=fontObj4.render('Medium',True,BLACK,WHITE)
    hard_txt=fontObj4.render('Hard',True,BLACK,WHITE)

    ok_txt=fontObj4.render('Ok',True,BLACK,WHITE)
    cancel_txt=fontObj4.render('Cancel',True,BLACK,WHITE)

    image_rect=image_txt.get_rect(topleft=(margin,margin))
    example_rect=example_txt.get_rect(midtop=(WINWIDTH/2,image_rect.bottom+margin))
    
    
    load_new_rect=load_new_txt.get_rect(midtop=(WINWIDTH/2,example_rect.bottom+margin))
    difficulty_rect=difficulty_txt.get_rect(topleft=(margin,WINHEIGHT/2+margin))
    easy_rect=easy_txt.get_rect(midtop=(WINWIDTH/2,difficulty_rect.bottom+margin))
    medium_rect=medium_txt.get_rect(midtop=(WINWIDTH/2,easy_rect.bottom+margin))
    hard_rect=hard_txt.get_rect(midtop=(WINWIDTH/2,medium_rect.bottom+margin))
    path_rect=pygame.Rect(load_new_rect.left,load_new_rect.bottom+margin/2,load_new_rect.width,load_new_rect.height)
    cancel_rect=cancel_txt.get_rect(bottomright=(WINWIDTH-2*margin,WINHEIGHT-margin))
    ok_rect=ok_txt.get_rect(bottomright=(cancel_rect.left-2*margin,WINHEIGHT-margin))
    
    texts=[image_txt,example_txt,load_new_txt,difficulty_txt,easy_txt,medium_txt,hard_txt,cancel_txt,ok_txt]
    rects=[image_rect,example_rect,load_new_rect,difficulty_rect,easy_rect,medium_rect,hard_rect,cancel_rect,ok_rect]
    buttons=[example_rect,load_new_rect,easy_rect,medium_rect,hard_rect,cancel_rect,ok_rect]
    button_image=[]
    
    for txt in texts:
        txt.set_colorkey(WHITE)
        txt.convert_alpha()

    for button in buttons:
        button.width=button.width+margin
        blue_b=pygame.transform.scale(blue_button,(button.width,button.height)).convert()
        blue_b.set_colorkey(WHITE)
        blue_b.set_alpha(192)
        blue_b.convert_alpha()
        button_image.append(blue_b)

    browse_rect=browse_txt.get_rect(topleft=(load_new_rect.topright))
    browse_rect.left=browse_rect.left+5

    
    while image_loaded==0:
        SURFACE.fill(LOAD_BG)
        for i in range(len(buttons)):
            SURFACE.blit(button_image[i],(buttons[i].left,buttons[i].top))
        for i in range(9):
            SURFACE.blit(texts[i],rects[i])
        
        
        easy_circle=pygame.draw.circle(SURFACE,WHITE,(easy_rect.left-(r+2),easy_rect.top+easy_rect.height/2),r)
        medium_circle=pygame.draw.circle(SURFACE,WHITE,(medium_rect.left-(r+2),medium_rect.top+medium_rect.height/2),r)
        hard_circle=pygame.draw.circle(SURFACE,WHITE,(hard_rect.left-(r+2),hard_rect.top+hard_rect.height/2),r)
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            elif event.type==MOUSEMOTION:
                mousex,mousey=event.pos
            elif event.type==MOUSEBUTTONUP:
                mousex,mousey=event.pos
                if example_rect.left<mousex<example_rect.right and example_rect.top<mousey<example_rect.bottom:
                    pic_file='example_pic.jpeg'
                    selected='example'
                    path=1
                elif load_new_rect.left<mousex<load_new_rect.right and load_new_rect.top<mousey<load_new_rect.bottom:
                    load_new=1
                    selected='load_new'
                    pic_file=''
                elif easy_rect.left<mousex<easy_rect.right and easy_rect.top<mousey<easy_rect.bottom:
                    level=1
                elif medium_rect.left<mousex<medium_rect.right and medium_rect.top<mousey<medium_rect.bottom:
                    level=2
                elif hard_rect.left<mousex<hard_rect.right and hard_rect.top<mousey<hard_rect.bottom:
                    level=3
                elif browse_rect.left<mousex<browse_rect.right and browse_rect.top<mousey<browse_rect.bottom and load_new==1:
                    browse=1
                    selected='browse'
                elif path_rect.left<mousex<path_rect.right and path_rect.top<mousey<path_rect.bottom:
                    pic_file=''
                    path=1
                    selected='path'
                elif cancel_rect.left<mousex<cancel_rect.right and cancel_rect.top<mousey<cancel_rect.bottom:
                    main()
                elif ok_rect.left<mousex<ok_rect.right and ok_rect.top<mousey<ok_rect.bottom and path==1 and level!=0:
                    image_loaded=1
                    
            elif event.type==KEYDOWN and load_new==1 and path==1 and selected=='path':
                pic_file=pic_file+(event.unicode)
                typing_txt=1

        if (example_rect.left<mousex<example_rect.right and example_rect.top<mousey<example_rect.bottom) or selected=='example':
            highlight(example_rect,BLUE,2)
        if (load_new_rect.left<mousex<load_new_rect.right and load_new_rect.top<mousey<load_new_rect.bottom) or selected=='load_new':
            highlight(load_new_rect,BLUE,2)
        if easy_rect.left<mousex<easy_rect.right and easy_rect.top<mousey<easy_rect.bottom:
            highlight(easy_rect,BLUE,2)
        if medium_rect.left<mousex<medium_rect.right and medium_rect.top<mousey<medium_rect.bottom:
            highlight(medium_rect,BLUE,2)
        if hard_rect.left<mousex<hard_rect.right and hard_rect.top<mousey<hard_rect.bottom:
            highlight(hard_rect,BLUE,2)
        if (browse_rect.left<mousex<browse_rect.right and browse_rect.top<mousey<browse_rect.bottom and load_new==1) or selected=='browse':
            highlight(browse_rect,BLUE,3)
        if ((type_rect.collidepoint(mousex,mousey)or path_rect.collidepoint(mousex,mousey)) and load_new==1) or selected=='path':
            if path_rect.width<type_rect.width:
                highlight(type_rect,BLUE,3)
            else:
                if path_rect.collidepoint(mousex,mousey) or selected=='path':
                    highlight(path_rect,BLUE,3)
        if cancel_rect.left<mousex<cancel_rect.right and cancel_rect.top<mousey<cancel_rect.bottom:
            highlight(cancel_rect,BLUE,2)
        if ok_rect.left<mousex<ok_rect.right and ok_rect.top<mousey<ok_rect.bottom and path==1 and level!=0:
            highlight(ok_rect,BLUE,2)
        if load_new==1:
            pygame.draw.rect(SURFACE,WHITE,path_rect)
            SURFACE.blit(browse_txt,browse_rect)
        if browse==1:
            pic_file=''
            root=Tkinter.Tk()
            root.withdraw()
            pic_file=tkFileDialog.askopenfilename(parent=root,title='Load image')
            path=1
            browse=0
            
        if typing_txt==1 or (selected=='browse' and path==1):
            type_txt=fontObj5.render(pic_file,True,BLACK,WHITE)
            type_rect=type_txt.get_rect(midbottom=path_rect.midbottom)
            SURFACE.blit(type_txt,type_rect)
            
        if selected=='path':
            type_rect=pygame.Rect(0,0,0,0)

        if level==1:
            pygame.draw.circle(SURFACE,RED,(easy_rect.left-(r+2),easy_rect.top+easy_rect.height/2),r-4)
        elif level==2:
            pygame.draw.circle(SURFACE,RED,(medium_rect.left-(r+2),medium_rect.top+medium_rect.height/2),r-4)
        elif level==3:
            pygame.draw.circle(SURFACE,RED,(hard_rect.left-(r+2),hard_rect.top+hard_rect.height/2),r-4)

        pygame.display.update()
        fpsClock.tick(FPS)
        if image_loaded==1:
            try:
                picture=pygame.image.load(pic_file)
            except:
                error_txt=fontObj4.render('Image not found or file incompatible',True,BLACK,WHITE)
                error_rect=error_txt.get_rect(midbottom=(WINWIDTH/2,WINHEIGHT/2))
                error_txt.set_colorkey(WHITE)
                error_txt.convert_alpha()
                SURFACE.blit(error_txt,error_rect)
                pygame.display.update()
                pygame.time.wait(1000)
                image_loaded=0
                pic_file=''
    return game_started,image_loaded,picture,level

def init_game(puzzle_pieces,boxes):
    puzzle_pieces[boxes-1][boxes-1]=None
    return puzzle_pieces

def generate_board(puzzle_pieces,level):
    global data
    data=[puzzle_pieces]
    randomise={1:20,2:25,3:30}
    move=None
    i=0
    while i<randomise[level]:
        move=get_random_move(move,puzzle_pieces)
        blankx,blanky=get_blank(puzzle_pieces)
        if move=='Up':
            puzzle_pieces[blanky][blankx]=puzzle_pieces[blanky-1][blankx]
            puzzle_pieces[blanky-1][blankx]=None
        elif move=='Down':
            puzzle_pieces[blanky][blankx]=puzzle_pieces[blanky+1][blankx]
            puzzle_pieces[blanky+1][blankx]=None
        elif move=='Left':
            puzzle_pieces[blanky][blankx]=puzzle_pieces[blanky][blankx-1]
            puzzle_pieces[blanky][blankx-1]=None
        elif move=='Right':
            puzzle_pieces[blanky][blankx]=puzzle_pieces[blanky][blankx+1]
            puzzle_pieces[blanky][blankx+1]=None
        data.append([puzzle_pieces,move])
        #print data[i+1][1]
        i=i+1
    return puzzle_pieces

def get_random_move(move,puzzle_pieces):
    moves=['Up','Down','Left','Right']
    if move=='Up' or (not isValidmove(puzzle_pieces,'Down')):
        moves.remove('Down')
    if move=='Down' or (not isValidmove(puzzle_pieces,'Up')):
        moves.remove('Up')
    if move=='Left' or (not isValidmove(puzzle_pieces,'Right')):
        moves.remove('Right')
    if move=='Right' or (not isValidmove(puzzle_pieces,'Left')):
        moves.remove('Left')
    move=random.choice(moves)
    return move
    
def get_blank(puzzle_pieces):
    for i in range(len(puzzle_pieces)):
        for j in range(len(puzzle_pieces)):
            if puzzle_pieces[i][j]==None:
                return (j,i)
    
def isValidmove(puzzle_pieces,move):
    valid=False
    blankx,blanky=get_blank(puzzle_pieces)
    if move=='Up':
        valid=(blanky-1>=0)
    if move=='Down':
        valid=((blanky+1)<len(puzzle_pieces))
    if move=='Right':
        valid=((blankx+1)<len(puzzle_pieces))
    if move=='Left':
        valid=(blankx-1>=0)
    return valid
        
def draw_border(border,size):
    border_rect=pygame.Rect((0,0),(size))
    border_rect.right=WINWIDTH
    pygame.draw.rect(SURFACE,RED,border_rect,border)

def draw_outlines(border,size,boxes):
    width=WINHEIGHT/boxes
    height=WINHEIGHT/boxes
    for i in range(boxes):
        for j in range(boxes):
            outline_rect=pygame.Rect((j*width)+(WINWIDTH-WINHEIGHT),(i*height),width,height)
            pygame.draw.rect(SURFACE,ORANGE,outline_rect,border+1)
            pygame.draw.rect(SURFACE,WHITE,outline_rect,border)

def getbox(mousex,mousey,boxes):
    for i in range(boxes):
        for j in range(boxes):
            try:
                box=pygame.Rect((WINWIDTH-WINHEIGHT)+(j*pic.get_width()/boxes),i*pic.get_height()/boxes,pic.get_width()/boxes,pic.get_height()/boxes)
            except:
                continue
            if box.collidepoint(mousex,mousey):
                return j,i

def move_box(boxx,boxy,direction,puzzle_pieces):
    moving_done=0
    border=3
    blankx,blanky=get_blank(puzzle_pieces)
    boxes=len(puzzle_pieces)
    width=pic.get_width()/boxes
    height=pic.get_height()/boxes
    moving_rect=puzzle_pieces[boxy][boxx]
    top=boxy*height
    left=boxx*width
    puzzle_pieces[boxy][boxx]=None
    while moving_done==0:
        if direction=='Up':
            top=top-1
        elif direction=='Down':
            top=top+1
        elif direction=='Left':
            left=left-1
        elif direction=='Right':
            left=left+1

        for i in range(boxes):
            for j in range(boxes):
                if puzzle_pieces[i][j]==None:
                    black_rect=pygame.Rect((j*width)+(WINWIDTH-WINHEIGHT),(i*height),width,height)
                    pygame.draw.rect(SURFACE,BLACK,black_rect)
                else:
                    SURFACE.blit(pic,((j*width)+(WINWIDTH-WINHEIGHT),(i*height)),puzzle_pieces[i][j])
                    highlight((((j*width)+(WINWIDTH-WINHEIGHT),(i*height)),(width,height)),ORANGE,4)
                    highlight((((j*width)+(WINWIDTH-WINHEIGHT),(i*height)),(width,height)),WHITE,3)
                    

        SURFACE.blit(pic,(left+(WINWIDTH-WINHEIGHT),top),moving_rect)
        highlight(((left+(WINWIDTH-WINHEIGHT),top),(width,height)),ORANGE,4)
        highlight(((left+(WINWIDTH-WINHEIGHT),top),(width,height)),WHITE,3)

        draw_border(border,pic.get_size())
        
        if left==(boxx*width)+width or left==(boxx*width)-width or top==(boxy*height)+height or top==(boxy*height)-height:
            moving_done=1
            puzzle_pieces[blanky][blankx]=moving_rect


        
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            
        pygame.display.update()
        fpsClock.tick(FPS+70)
    return puzzle_pieces


def solve(scrambled_pieces):
    boxes=len(scrambled_pieces)
    width=pic.get_width()/boxes
    height=pic.get_height()/boxes
    
    for i in range(len(data)-1,0,-1):
        blankx,blanky=get_blank(scrambled_pieces)
        direction=data[i][1]
        if direction=='Up':
            boxx=blankx
            boxy=blanky+1
        elif direction=='Down':
            boxx=blankx
            boxy=blanky-1
        elif direction=='Left':
            boxx=blankx+1
            boxy=blanky
        elif direction=='Right':
            boxx=blankx-1
            boxy=blanky
        scrambled_pieces=move_box(boxx,boxy,direction,scrambled_pieces)
        fpsClock.tick(FPS+35)


def restart():
    margin=20
    pygame.time.wait(1000)
    mousex,mousey=(0,0)
    font8_path=pygame.font.match_font('magneto',bold=True,italic=True)
    fontObj8=pygame.font.Font(font8_path,50)
    font9_path=pygame.font.match_font('georgia',italic=True,bold=True)
    fontObj9=pygame.font.Font(font9_path,28)
    fontObj10=pygame.font.Font(font9_path,32)

    fin_txt=fontObj8.render('Fin',True,RED,WHITE)
    wanna_txt=fontObj9.render('Wanna try again?',True,BLACK,WHITE)
    yes_txt1=fontObj9.render('Yes',True,GREEN,WHITE)
    no_txt1=fontObj9.render('No',True,RED,WHITE)

    yes_txt2=fontObj10.render('Yes',True,BLUE,WHITE)
    no_txt2=fontObj10.render('No',True,ORANGE,WHITE)

    fin_rect=fin_txt.get_rect(midbottom=(WINWIDTH/2,WINHEIGHT/2-margin))
    wanna_rect=wanna_txt.get_rect(midtop=(WINWIDTH/2,WINHEIGHT/2+(2*margin)))
    yes_rect1=yes_txt1.get_rect(bottomleft=(wanna_rect.left,wanna_rect.bottom+(2*margin)))
    no_rect1=no_txt1.get_rect(bottomright=(wanna_rect.right,wanna_rect.bottom+(2*margin)))

    yes_rect2=yes_txt2.get_rect(bottomleft=(wanna_rect.left,wanna_rect.bottom+(2*margin)))
    no_rect2=no_txt2.get_rect(bottomright=(wanna_rect.right,wanna_rect.bottom+(2*margin)))

    texts=[yes_txt1,no_txt1,fin_txt,wanna_txt,yes_txt2,no_txt2]
    rects1=[yes_rect1,no_rect1,fin_rect,wanna_rect]

    for txt in texts:
        txt.set_colorkey(WHITE)
        txt.convert_alpha()
    while True:
        SURFACE.fill(YELLOW)

        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            elif event.type==MOUSEMOTION:
                mousex,mousey=event.pos
            elif event.type==MOUSEBUTTONUP:
                mousex,mousey=event.pos
                if yes_rect2.collidepoint(mousex,mousey):
                    main()
                elif no_rect2.collidepoint(mousex,mousey):
                    terminate()
        if yes_rect2.collidepoint(mousex,mousey):
            SURFACE.blit(yes_txt2,yes_rect2)
        elif no_rect2.collidepoint(mousex,mousey):
            SURFACE.blit(no_txt2,no_rect2)
            
        for i in range(len(rects1)):
            SURFACE.blit(texts[i],rects1[i])

        pygame.display.update()
        fpsClock.tick(FPS)


def game_over_animation():
    start_time=pygame.time.get_ticks()
    #pygame.mixer.music.stop()
    pygame.mixer.music.load('winner.mp3')
    pygame.mixer.music.play(-1,0.0)
    mouseClicked=0
    wincenter=WINCENTER
    font11_path=pygame.font.match_font('magneto',bold=True,italic=True)
    fontObj11=pygame.font.Font(font11_path,40)
    you_won_txt=fontObj11.render('YOU WON!!!',True,YELLOW,WHITE)
    you_won_txt.set_colorkey(WHITE)
    you_won_txt.convert_alpha()

    you_won_rect=you_won_txt.get_rect(midbottom=(WINWIDTH/2,WINHEIGHT/2))
    current_position,vel=init_stars(wincenter)
    draw_stars(current_position,WHITE)
    while pygame.time.get_ticks()<start_time+6500:
        SURFACE.fill(BLACK)
        SURFACE.blit(you_won_txt,you_won_rect)
        current_position=move_stars(current_position,vel,WHITE)
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            elif event.type==MOUSEMOTION:
                mousex,mousey=event.pos
            elif event.type==MOUSEBUTTONUP:
                mousex,mousey=event.pos
                if mousex<WINWIDTH and mousey<WINHEIGHT:
                    mouseClicked=1
                    wincenter=(mousex,mousey)
        if mouseClicked==1:
            current_position,vel=init_stars(wincenter)
            mouseClicked=0
        pygame.display.update()
        fpsClock.tick(FPS)
    pygame.mixer.music.stop()
    
def play_game(level):
    game_ended=0
    mousex,mousey=(0,0)
    direction=None
    boxx,boxy=(None,None)
    scrambled=0
    margin=20
    selected=0
    border=3
    scrambled_pieces=[]
    piece_no={1:4,2:5,3:6}
    boxes=piece_no[level]
    width=pic.get_width()/boxes
    height=pic.get_height()/boxes
    puzzle_pieces=[[(j*width,i*height,width,height)for j in range(boxes)]for i in range(boxes)]
                
    font6_path=pygame.font.match_font('ebrima',bold=True,italic=True)
    font7_path=pygame.font.match_font('centuryschoolbook',italic=True)
    fontObj6=pygame.font.Font(font6_path,20)
    fontObj6.set_italic(10)
    fontObj7=pygame.font.Font(font7_path,16)
    
    
    scramble_txt=fontObj6.render('SCRAMBLE',True,YELLOW,WHITE)
    scramble_txt.set_colorkey(WHITE)
    scramble_txt.convert_alpha()
    scramble_rect=scramble_txt.get_rect(midbottom=((WINWIDTH-WINHEIGHT)/2,WINHEIGHT-margin))
    scramble_rect.width=scramble_rect.width+margin
    scramble_rect.left=scramble_rect.left-margin/2
    red_b=pygame.transform.scale(red_button,(scramble_rect.width,scramble_rect.height))
    red_b.set_colorkey(WHITE)
    red_b.set_alpha(192)
    red_b.convert_alpha()

    show_img_txt=fontObj6.render('Show Image',True,BLACK,WHITE)
    generating_txt=fontObj7.render('generating....',True,YELLOW,WHITE)
    generating_txt.set_colorkey(WHITE)
    generating_txt.convert_alpha()
    solve_txt=fontObj6.render('SOLVE',True,RED,WHITE)
    quit_txt=fontObj6.render('QUIT',True,RED,WHITE)

    generating_rect=generating_txt.get_rect(topleft=((0,margin/2)))
    show_img_rect=show_img_txt.get_rect(midtop=((WINWIDTH-WINHEIGHT)/2,generating_rect.bottom+(2*margin)))
    solve_rect=solve_txt.get_rect(midtop=((WINWIDTH-WINHEIGHT)/2,show_img_rect.bottom+margin))
    quit_rect=quit_txt.get_rect(midtop=((WINWIDTH-WINHEIGHT)/2,solve_rect.bottom+margin))

    texts=[show_img_txt,quit_txt,solve_txt]
    rects=[show_img_rect,quit_rect,solve_rect]
    for txt in texts:
        txt.set_colorkey(WHITE)
        txt.convert_alpha()

    buttons=[]
    for rect in rects:
        rect.width=rect.width+margin
        yellow_b=pygame.transform.scale(yellow_button,(rect.width,rect.height)).convert()
        yellow_b.set_colorkey(WHITE)
        yellow_b.convert_alpha()
        buttons.append(yellow_b)
    

    while game_ended==0:
        SURFACE.fill(PLAY_BG)
        for i in range(boxes):
            for j in range(boxes):
                if puzzle_pieces[i][j]==None:
                    black_rect=pygame.Rect((j*width)+(WINWIDTH-WINHEIGHT),(i*height),width,height)
                    pygame.draw.rect(SURFACE,BLACK,black_rect)
                else:
                    SURFACE.blit(pic,((j*width)+(WINWIDTH-WINHEIGHT),(i*height)),puzzle_pieces[i][j])

        for i in range(len(texts)):
            SURFACE.blit(buttons[i],rects[i])
            SURFACE.blit(texts[i],rects[i])
        draw_outlines(border,pic.get_size,boxes)
        draw_border(border,pic.get_size())
        if scrambled==0:
            SURFACE.blit(red_b,(scramble_rect.left,scramble_rect.top))
            SURFACE.blit(scramble_txt,scramble_rect)
        else:
            blankx,blanky=get_blank(puzzle_pieces)

        if scrambled==1:
            if puzzle_pieces==INIT_PIECES:
                game_over_animation()
                restart()
        
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            elif event.type==MOUSEMOTION:
                mousex,mousey=event.pos
            elif event.type==MOUSEBUTTONUP:
                mousex,mousey=event.pos
                if scramble_rect.collidepoint(mousex,mousey):
                    SURFACE.blit(generating_txt,generating_rect)
                    pygame.display.update()
                    puzzle_pieces=init_game(puzzle_pieces,boxes)
                    INIT_PIECES=copy.deepcopy(puzzle_pieces)
                    puzzle_pieces=generate_board(puzzle_pieces,level)
                    SCRAMBLED_PIECES=copy.deepcopy(puzzle_pieces)
                    scrambled=1
                elif quit_rect.collidepoint(mousex,mousey):
                    terminate()
                elif show_img_rect.collidepoint(mousex,mousey):
                    SURFACE.blit(pic,(WINWIDTH-WINHEIGHT,0))
                    draw_border(border,pic.get_size())
                    pygame.display.update()
                    pygame.time.wait(2000)
                elif solve_rect.collidepoint(mousex,mousey) and scrambled==1:
                    solve(SCRAMBLED_PIECES)
                    restart()
                elif (getbox(mousex,mousey,boxes))!=None and scrambled==1:
                    boxx,boxy=getbox(mousex,mousey,boxes)
                    if boxx==blankx+1 and boxy==blanky:
                        direction='Left'
                    elif boxx==blankx-1 and boxy==blanky:
                        direction='Right'
                    elif boxx==blankx and boxy==blanky+1:
                        direction='Up'
                    elif boxx==blankx and boxy==blanky-1:
                        direction='Down'
                    else:
                        direction=None
                    if direction!=None:
                        move_box(boxx,boxy,direction,puzzle_pieces)
            
        if scramble_rect.collidepoint(mousex,mousey) and scrambled==0:
            highlight(scramble_rect,YELLOW,border)
        elif quit_rect.collidepoint(mousex,mousey):
            highlight(quit_rect,ORANGE,border)
        elif show_img_rect.collidepoint(mousex,mousey):
            highlight(show_img_rect,ORANGE,border)
        elif solve_rect.collidepoint(mousex,mousey) and scrambled==1:
            highlight(solve_rect,ORANGE,border)
        elif (getbox(mousex,mousey,boxes))!=None:
            boxx,boxy=getbox(mousex,mousey,boxes)
            highlight(((WINWIDTH-WINHEIGHT)+boxx*width,boxy*height,width,height),ORANGE,border-1)
                
                    
        pygame.display.update()
        fpsClock.tick(FPS)




def main():
    pygame.init()
    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.play(-1,0.0)
    pygame.mixer.music.set_volume(0.20)
    global fpsClock,FPS,SURFACE,pic
    fpsClock=pygame.time.Clock()
    FPS=20

    #set up window
    SURFACE=pygame.display.set_mode((WINWIDTH,WINHEIGHT),0,32)
    pygame.display.set_caption('Scrambler')

    #iitializations
    game_started=0
    image_loaded=0

    #game loop
    while True:
        if game_started==0:
            game_started=start_animation(game_started)
        elif image_loaded==0:
            game_started,image_loaded,pic,level=load_image(image_loaded)
            pic=pygame.transform.scale(pic,(WINHEIGHT,WINHEIGHT))
        else:
            play_game(level)

        pygame.display.update()
        fpsClock.tick(FPS)


if __name__=='__main__':
    main()
    
