from ursina import *
import time

app = Ursina()
#소리
coin_sound = Audio('sound/app_alert_tone_033.mp3', autoplay=False)
game_over_sound = Audio('sound/PM_BlurryDreams_123_252.mp3', autoplay=False)
life_damage_sound = Audio('sound/zapsplat_multimedia_game_sound_fantasy_magical_impact_hit_strike_crash_74048.mp3',autoplay=False)
game_play_sound = Audio('sound/Alan Walker - Faded (EDM Remix).mp3',autoplay=False)
game_start_sound = Audio('sound/stranger-things-124008.mp3',autoplay=False)

'''게임 전 화면에 들어가는 변수'''

game_active = False
stage_selected = False
current_stage = None


#시작창
start_button = None
stage_buttons = []
game_objects = []
shop_button = None
restart_button = None
exit_button = None

def show_start_screen():
    global start_button
    if not game_active:
        game_start_sound.play()
    start_button = Button(
        text= 'game start',
        font = r'font/강원교육모두 Bold.ttf',

        scale=(0.2, 0.1), 
        position=(0, -0.4), 
        color= color.brown
        )
    start_button.on_click = show_stage_selection_screen
def show_stage_selection_screen():
    global stage_buttons, shop_button
    destroy_start_screen_objects()
    stage_buttons = []
    for q in range(1, 4):  
        button = Button(
            text=f'Stage {q}',
            font = r'font/강원교육모두 Bold.ttf',

            scale=(0.2, 0.05),
            position=(q*0.3 - 0.9, -0.3),
            color=color.orange
        )
        def speed():
            q
        
        button.on_click = Func(start_game, q)
        stage_buttons.append(button)

        
    shop_button = Button(
        text=f'shop',
        font = r'font/강원교육모두 Bold.ttf',

        scale=(0.2, 0.05),
        position=(0.5, -0.3),
        color=color.red
    )
    shop_button.on_click = open_shop
    stage_buttons.append(shop_button)
        
def open_shop():
    global stage_buttons, shop_button
    for button in stage_buttons:
        destroy(button)

    # 샵 화면 텍스트 추가
    shop_text = Text(
        text='Welcome to the Shop!',
        position=(-0.25, 0.45),
        scale=2
    )

    # 돌아가기 버튼 추가
    back_button = Button(
        text='Back',
        font = r'font/강원교육모두 Bold.ttf',

        scale=(0.2, 0.1),
        position=(0, -0.45),
        color=color.blue
    )
    back_button.on_click = lambda: close_shop(shop_text, back_button)

def close_shop(shop_text, back_button):
    # 샵 화면 관련 객체 삭제
    destroy(shop_text)
    destroy(back_button)

    # 이전 화면으로 돌아가기 버튼 표시
    show_stage_selection_screen()




def game_over():
    global game_active
    game_active = False
    game_play_sound.stop()
    game_over_sound.play()

    # 게임에서 사용된 객체들을 숨김
    player1.visible = False
    set_ground_visible(False)
    set_game_objects_visible(False)

    clear_text.visible = True

    # 게임 오버 텍스트를 잠시 보여주고, 이후 스테이지 선택 화면으로 돌아가기
    invoke(reset_game_state, delay=3)
    invoke(show_stage_selection_screen, delay=3.5)

def reset_game_state():
    global score, life
    # 점수 및 목숨 초기화
    score = 0
    life = 5
    score_text.text = f'Score: {score}'
    life_text.text = f'lives : {life}'
    
    # 게임에서 사용된 객체들을 초기화
    for coin in coins:
        coin.visible = False  # 코인들을 다시 숨김

    for stick in stick_instance:
        stick.visible = False
def check_life():
    global life
    if life <= 0:
        life = 0  # 생명이 음수로 내려가지 않도록 고정
        game_over()





#치트키
def input (key):
    global life
    global score
    if key == 'k':
        score += 10
        life += 3
        life_text.text = f'lives : {life}'
        score_text.text = f'Score: {score}'


def quit_game():
    game_over_sound.play()
    invoke(application.quit,delay = 2)


def destroy_start_screen_objects():
    """ 시작 화면 관련 버튼 삭제 """
    global start_button  # 전역 변수로 선언
    if start_button is not None:  # start_button이 있을 때만 파괴
        destroy(start_button)
    start_button = None  # 삭제 후 None으로 설정


# 게임 객체의 가시성 설정
def set_game_objects_visible(visible):
    """ 게임에 사용되는 객체의 가시성 설정 """
    for stick1 in stick_instance:
        stick1.visible = visible
    for coin in coins:
        coin.visible = visible

# 땅의 가시성 설정
def set_ground_visible(visible):
    """ 바닥의 가시성 설정 """
    ground1.visible = visible
    ground2.visible = visible
    ground3.visible = visible
    ground4.visible = visible
    ground5.visible = visible
    ground6.visible = visible
#게임 오버 텍스트
clear_text = Text(
    text='Game Over!',
    font = r'font/강원교육모두 Bold.ttf',
    scale=7,
    origin=(0, 0),
    visible=False
)

# 점수 & 목숨
score = 0
score_text = Text(
    text=f'Score: {score}', 
    position=(-0.85, 0.45),
    scale=2,
    visible = False,
    )
life = 5
life_text = Text(
    text =f' lives : {life}',
    position = (-0.55, 0.45), 
    scale = 2,
    visible = False,
)

    

#플레이어 설정
player = EditorCamera()

player1 = Entity(
    model =r'models_compressed/Enemy.obj',
    scale = 0.75,
    texture = r'textures/EnemyTexture.png',
    position = (0,-1.3,50),
    collider = 'box',
    visible = False,

)

#하늘& 땅
'''sky1 = Entity(
    model = 'cube',
    color = color.green,
    scale = (1500,1,1000),
    position = (0,50,0),
    texture = 'textures/textures/rocky_terrain_diff_4k.jpg',
    visible = True,
)'''
ground1 = Entity(
    model = 'cube',
    color = color.green,
    scale = (500,1,500),
    position = (0,-5,0),
    texture = 'textures/textures/rocky_terrain_diff_4k.jpg',
    visible = False,

)

ground2 = Entity(
    model = 'cube',
    color = color.green,
    scale = (500,1,500),
    position = (0,-5,500),
    texture =  'textures/textures/rocky_terrain_diff_4k.jpg',
    visible = False,

)
ground3 = Entity(
    model = 'cube',
    color = color.green,
    scale = (500,1,500),
    position = (500,-5,500),
    texture =  'textures/textures/rocky_terrain_diff_4k.jpg',
    visible = False,

)
ground4 = Entity(
    model = 'cube',
    color = color.green,
    scale = (500,1,500),
    position = (500,-5,0),
    texture =  'textures/textures/rocky_terrain_diff_4k.jpg',
    visible = False,

)
ground5 = Entity(
    model = 'cube',
    color = color.green,
    scale = (500,1,500),
    position = (-500,-5,500),
    texture = 'textures/textures/rocky_terrain_diff_4k.jpg',
    visible = False,

)
ground6 = Entity(
    model = 'cube',
    color = color.green,
    scale = (500,1,500),
    position = (-500,-5,0),
    texture =  'textures/textures/rocky_terrain_diff_4k.jpg',
    visible = False,
)

#코인
class coin1(Entity):
              def __init__(self):
                 super().__init__(
                    model = 'sphere',
                    color = color.yellow,
                    scale = (10,10,3),
                    position = (random.uniform(750,-750),0,random.uniform(500,-500)),
                    collider = 'box',
                    visible = False,
                 )
                 self.player = player1

              def update(self):
               if game_active:
                    self.set_position((self.position.x,self.position.y,self.position.z - 100 * time.dt))
                    if self.z <= -500:
                        self.z = 500
                    if self.x <= -1000:
                        self.x = 500
                    if self.x >= 1000:
                        self.x = -50
                    if held_keys['a']:
                       self.x +=  held_keys['a'] * time.dt * 50
                    if held_keys['d']:
                       self.x -=  held_keys['d'] * time.dt * 50
                    self.rotation_y += time.dt * 100
                    self.check_collisions()
              def check_collisions(self):
                   global score
                   if self.intersects(player1).hit:
                        print("충돌 발생!")
                        score += 1  
                        score_text.text = f'Score: {score}'
                        destroy(self)
                        coin_sound.play()
                        
                        #application.quit()      
coin1_instance = coin1()   
coins = [coin1() for _ in range(50)]

stick_instance = []

#장애물
sticks =[
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],






]
class stick1(Entity):
              def __init__(self,i,j):
                 super().__init__(
                    model = 'cube',
                    color = color.blue,
                    scale = (10,100,10),
                    position = (i*50-1400 + j*20, random.uniform(0,-500), j*75-1000),
                    collider = 'box',
                    visible = False,
                    texture =  r'textures/textures/rocky_terrain_diff_4k.jpg',
                 )
                 
                 self.player = player1

              #장애물 업데이트   
              def update(self):
                  if game_active:  
                    self.set_position((self.position.x,self.position.y + 25 * time.dt,self.position.z - 100 * time.dt))
                    if self.z <= -500:
                        self.z = 500
                    if self.x <= -1000:
                        self.x = 500
                    if self.x >= 1000:
                        self.x = -500
                    if self.y >= 45:
                       self.y = random.uniform(-55,-250)
                    if held_keys['a']:
                       self.x +=  held_keys['a'] * time.dt * 50
                    if held_keys['d']:
                       self.x -=  held_keys['d'] * time.dt * 50
                    self.check_collisions()

              #장애물 충돌      
              def check_collisions(self):
                   if self.intersects(player1).hit:
                        global life,score,game_active
                        print("충돌 발생!")
                        self.color = color.red
                        life -= 1
                        life_text.text = f'lives : {life}'
                        destroy(self)
                        life_damage_sound.play()
                        if life<=0:
                           if score>=10:
                               show_buttons()
                               game_active = False
                           else:   
                            clear_text.visible = True
                            game_over_sound.play()
                            invoke(self.hide_clear_text, delay=2)
                            invoke(self.end_game, delay=1.5) 
                
              def hide_clear_text(self):
                     clear_text.visible = False
              def end_game(self):
                     application.quit()
for i in range(len(sticks)):
    for j in range(len(sticks[i])):
        if sticks[i][j]:
           stick_instance.append(stick1(i, j))

#버튼
restart_button = None
exit_button = None         

def show_buttons():
    global restart_button, exit_button
    restart_button = Button(
        text="continue",
        font = r'font/강원교육모두 Bold.ttf',
        scale=(0.2, 0.1),
        position=(-0.2, 0), 
        color=color.azure
        )

    exit_button = Button(
        text="quit",
        font = r'font/강원교육모두 Bold.ttf',
        scale=(0.2, 0.1),
        position=(0.2, 0),
        color=color.red
        )
    
    restart_button.on_click = restart_game
    exit_button.on_click = quit_game

def hide_buttons():
    global restart_button, exit_button
    if restart_button:
        destroy(restart_button)
    if exit_button:
        destroy(exit_button)

def restart_game():
    global score, life,game_active
    hide_buttons()
    score -= 10
    life += 1
    score_text.text = f'Score: {score}'
    life_text.text = f'lives : {life}'
    clear_text.visible = False    
    game_active = True       
           
'''def quit_game():
    global game_active
    game_over_sound.play()
    game_active = False
    for button in stage_buttons:
        destroy(button)
    destroy(shop_button)
    invoke(show_stage_selection_screen, delay=2)'''
               
    

#땅, 플레이어 업데이트
def update():
 if game_active:
   global speed
   player1.rotation_y = 0
   player1.rotation_x = 0
   if held_keys['a']:
        player1.rotation_y = -60
        ground1.x +=  held_keys['a'] * time.dt * 50
        ground2.x +=  held_keys['a'] * time.dt * 50
        ground3.x +=  held_keys['a'] * time.dt * 50
        ground4.x +=  held_keys['a'] * time.dt * 50
        ground5.x +=  held_keys['a'] * time.dt * 50
        ground6.x +=  held_keys['a'] * time.dt * 50
     
   if held_keys['d']:
      player1.rotation_y = 60
      ground1.x -=  held_keys['d'] * time.dt * 50
      ground2.x -=  held_keys['d'] * time.dt * 50
      ground3.x -=  held_keys['d'] * time.dt * 50
      ground4.x -=  held_keys['d'] * time.dt * 50
      ground5.x -=  held_keys['d'] * time.dt * 50
      ground6.x -=  held_keys['d'] * time.dt * 50
   

   ground1.set_position((ground1.position.x,ground1.position.y,ground1.position.z - 100 * time.dt))
   ground2.set_position((ground2.position.x,ground2.position.y,ground2.position.z - 100 * time.dt))
   ground3.set_position((ground3.position.x,ground3.position.y,ground3.position.z - 100 * time.dt))
   ground4.set_position((ground4.position.x,ground4.position.y,ground4.position.z - 100 * time.dt))
   ground5.set_position((ground5.position.x,ground5.position.y,ground5.position.z - 100 * time.dt))
   ground6.set_position((ground6.position.x,ground6.position.y,ground6.position.z - 100 * time.dt))

   if ground1.z <= -500:
       ground1.z = 500
   if ground2.z <= -500:
    ground2.z = 500
   if ground3.z <= -500:
      ground3.z = 500
   if ground4.z <= -500:
      ground4.z = 500
   if ground5.z <= -500:
      ground5.z = 500
   if ground6.z <= -500:
      ground6.z = 500


   if ground1.x <= -1000:
      ground1.x = 500
   if ground1.x >= 1000:
      ground1.x = -500
   if ground2.x <= -1000:
      ground2.x = 500
   if ground2.x >= 1000:
      ground2.x = -500
   if ground3.x <= -1000:
      ground3.x = 500
   if ground3.x >= 1000:
      ground3.x = -500
   if ground4.x <= -1000:
      ground4.x = 500
   if ground4.x >= 1000:
      ground4.x = -500
   if ground5.x <= -1000:
      ground5.x = 500
   if ground5.x >= 1000:
      ground5.x = -500
   if ground6.x <= -1000:
      ground6.x = 500
   if ground6.x >= 1000:
      ground6.x = -500
def start_game(stage):
    global current_stage, game_active, stage_selected, score_text, life_text, player1, ground1, ground2,ground3,ground4,ground5,ground6
    game_active = True
    current_stage = stage
    for button in stage_buttons:
        destroy(button)

    player1.visible = True
    ground1.visible = True
    ground2.visible = True
    ground3.visible = True
    ground4.visible = True
    ground5.visible = True
    ground6.visible = True

    if stick_instance:
        for stick in stick_instance:
            stick.visible = True
    else:
        print("stick_instance가 비어 있습니다.")

    for coin in coins:
        coin.visible = True

    score_text.visible = True
    life_text.visible = True
    game_start_sound.stop()
    game_play_sound.play()
show_start_screen()

app.run()