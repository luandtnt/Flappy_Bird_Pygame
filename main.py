from distutils.command.clean import clean

from venv import create
import pygame,sys,random
# hàm khởi tạo 2 cái sàn nối tiếp nhau
def draw_floor():
    screen.blit(floor,(floor_x_pos,580))
    screen.blit(floor,(floor_x_pos+400,580))
# tạo ra hình chữ nhật bao quanh những cái ống
def create_pipe(): 
    random_pipe_pos=random.choice(pipe_height)
    bottom_pipe=pipe_surface.get_rect(midtop=(200,random_pipe_pos))
    top_pipe=pipe_surface.get_rect(midtop=(200,random_pipe_pos-750)) # ý tưởng để cái khoảng cách trừ đi cũng trong 1 list random
    return bottom_pipe , top_pipe
# tạo hàm cho sự di chuyển của những cái ống
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
# tạo hàm để vẽ những cái ống lên màn hình
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 680:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
# Tạo hàm xử lý va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe): # Khi va chạm
            hit_sound.play()
            return False
    if bird_rect.top<=-65 or bird_rect.bottom>=600: # Khi đi quá màn hình game
        return False
    return True
# Khởi tạo hàm để có hiệu ứng xoay con chim
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*4,1)
    return new_bird
# Hàm tạo hiệu ứng đập cánh cho chim
def bird_animation():
    new_bird=bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center= (100, bird_rect.centery))
    '''
        tạo một con chim mới là 1 trong số những con chim được thêm vào list sau đó lại tạo rect bao quanh
        con chim mới đó
    '''
    return new_bird,new_bird_rect
# Tạo hàm tính điểm cho trò chơi
def score_display(game_state): 
    if game_state== 'main game':
        score_surface = game_font.render(f'Score : {int(score)}',True,(255,255,255))
        score_rect=score_surface.get_rect(center = (197,100))
        screen.blit(score_surface,score_rect)
    if game_state== 'game_over':
        score_surface = game_font.render(f'Score : {int(score)}',True,(255,255,255))
        score_rect=score_surface.get_rect(center = (197,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High_Score : {int(high_score)}',True,(255,255,255))
        high_score_rect =high_score_surface.get_rect(center = (197,500))
        screen.blit(high_score_surface,high_score_rect)
# hàm cập nhật điểm cao nhất
def update_core(score,high_score):
    if score>high_score:
        high_score=score
    return high_score
# khởi tạo game
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
# khởi tạo cửa sổ màn hình game
screen = pygame.display.set_mode((400,680))
# khởi tạo FPS(tốc độ) cho game
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40) # thêm font vào cửa sổ trò chơi
# Biến cho trò chơi
# tạo trọng lực cho con chim
gravity = 0.25 
bird_movement = 0 # tạo biến cho sự di chuyển của con chim
game_active=True # Biến cho sự hoạt động của trò chơi
score = 0
high_score = 0
# thêm background cho cửa sổ game
bg = pygame.image.load('assets/background-night.png') # load ảnh
bg = pygame.transform.scale2x(bg) # tăng kích thước của ảnh lên gấp đôi
# thêm sàn vào screen
floor = pygame.image.load('assets/floor.png')
floor = pygame.transform.scale2x(floor)
# khởi tạo giá trị tọa độ của sàn sao cho sàn chạy lùi
floor_x_pos = 0
# tạo con chim
bird_down = pygame.image.load('assets/yellowbird-downflap.png')
bird_mid = pygame.image.load('assets/yellowbird-midflap.png')
bird_up = pygame.image.load('assets/yellowbird-upflap.png')
bird_list = [bird_down,bird_mid,bird_up]
bird_index = 0
bird=bird_list[bird_index]
bird_rect=bird.get_rect(center = (120,340))
# tạo timer cho bird
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap,200)
# tạo ống
pipe_list=[]
pipe_surface=pygame.image.load('assets/pipe-green.png')
pipe_surface=pygame.transform.scale2x(pipe_surface)

# tạo timer
'''
    hiệu ứng xuất hiện cái ông là do cứ sau 1 khoảng thời gian nhất định thì sẽ có 1 cái ống mới được 
    tạo ra và cái ống cũ bị xóa bỏ, nên ở đây chúng ta cần tạo ra khoảng thời gian đó
'''
spawnpipe=pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1200) # nghĩa là sau 1.2 giây thì sẽ có 1 cái ống mới được tạo ra
pipe_height=[370, 350, 360 ,380 ,390, 340]
# Tạo màn hình kết thúc
game_over_surface = pygame.image.load('assets/message.png')
game_over_surface_rect = game_over_surface.get_rect(center=(200,340))
# Trèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
# While loop của trò chơi
while True:
    for event in pygame.event.get():
        # tạo nút tắt cho game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # tạo event khi click vào space thì con chim sẽ đi lên 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active :
                '''
                    khi click vào space thì trọng lực sẽ trở về 0 và sau đó -7 có nghĩa là giảm trọng lực
                    đi 7 => con chim sẽ đi lên vì trong pygame đi lên thì giảm y 
                '''
                bird_movement = 0
                bird_movement = -7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False : # Xử lý việc chơi lại
                game_active = True # gán lại biến bằng True
                pipe_list.clear() # xóa hết các ống đã tạo
                bird_rect.center = (120,340) # Đặt lại vị trí của con chim như mới bắt đầu trò chơi
                bird_movement = 0 # đặt lại sự di chuyển của con chim (trọng lực = 0)
                score=0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
                # tạo hiệu ứng đập cánh bằng cách, chạy lần lượt qua 3 trạng thái của chim đó là down,up,mid
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
    # thêm background vào screen
    screen.blit(bg,(0,0))
    if game_active:
        #CHIM
        bird_movement += gravity # do lúc đầu con chim chưa di chuyển nên là càng lúc P càng tăng
        # cho cái sàn có hiệu ứng chạy lùi
        bird_rect.centery += bird_movement # trong pygame đi xuống thì tăng y
        screen.blit(rotate_bird(bird),bird_rect)
        game_active = check_collision(pipe_list) # nếu có va chạm thì biến duy trì trò chơi return về False
        #ỐNG
        pipe_list=move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.012
        score_display('main game')
        score_sound_countdown -= 1
        # if score_sound_countdown <=0 :
        #     score_sound.play()
    else: 
        high_score=update_core(score,high_score)
        score_display('game_over')
        screen.blit(game_over_surface,game_over_surface_rect)
        
    #SÀN
    floor_x_pos -= 1
    draw_floor()
    ''' thuật toán sao cho sau khi cái sàn số 1 chạy hết khung của chiều rộng sẻ nhảy lên trên chiếc sàn
    số 2 rồi cứ thế chạy liên tục'''
    if floor_x_pos <= -400:
        floor_x_pos = 0
    
    pygame.display.update()
    clock.tick(60) 