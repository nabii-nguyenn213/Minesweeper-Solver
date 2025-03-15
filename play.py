from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
from models.heuristic import Heuristic
import joblib
from data_generator.processing import extract_feature
import time

HIDDEN_CELL = -0.5
MINE_CELL = -2
FLAG_CELL = -1

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--incognito")

driver = webdriver.Chrome(options=options)
driver.set_window_size(700, 700)
driver.set_window_position(10, 10)
driver.set_page_load_timeout(30)

minesweeper_url = 'https://minesweeperonline.com/#beginner'
# ! open minesweeper page
driver.execute_script(f'window.open("{minesweeper_url}")', 'blank')
driver.switch_to.window(driver.window_handles[-1])
time.sleep(2)
# playButton = driver.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div[4]/block-component/div/div[1]/div[1]/div/div/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div')
# playButton.click()

def get_current_board():
    num_row = 9
    num_col = 9
    current_board = np.zeros((num_row, num_col), dtype=object)
    for r in range(num_row):
        for c in range(num_col):
            grid_id = f'//*[@id="{r+1}_{c+1}"]'
            grid = driver.find_element(By.XPATH, grid_id)
            get_current_state = grid.get_attribute("class")
            if get_current_state == 'square bombflagged':
                current_board[r, c] = FLAG_CELL
            elif get_current_state == 'square blank':
                current_board[r, c] = HIDDEN_CELL
            elif get_current_state == 'square bombdeath':
                current_board[r, c] = MINE_CELL
            else:
                number = float(get_current_state[-1])
                current_board[r, c] = number
    return current_board

def reset_board():
    resetid = '//*[@id="face"]'
    resetButton = driver.find_element(By.XPATH, resetid)
    resetButton.click()
    
def game_over():
    face_id = '//*[@id="face"]'
    face = driver.find_element(By.XPATH, face_id)
    get_current_state = face.get_attribute("class")
    # ! when lose the class will be : "facedead"
    # ! otherwise "facewin"
    if get_current_state == 'facedead':
        return -1
    if get_current_state == 'facewin': 
        return 1
    return 0
    
def optimal_move(current_board, mlp, rf):
    min_probability = 101
    min_index = (None, None)
    features = extract_feature(current_board)
    for r in range(len(current_board)):
        for c in range(len(current_board[r])):
            if current_board[r, c] == HIDDEN_CELL:
                feature = features[r*len(current_board)+c].reshape((1, 27))
                proba_mlp = mlp.predict_proba(feature)[:, 1]
                proba_rf = rf.predict_proba(feature)[:, 1]
                mean = proba_mlp + proba_rf / 2
                if mean < min_probability:
                    min_probability = mean
                    min_index = (r, c)
    return min_index

def heuristic_solve(current_board): 
    heuristic = Heuristic(board=current_board)
    safes, mines = heuristic.solve()
    return safes, mines
        
def play():
    number_of_time_playing = 5
    
    mlp = joblib.load('models/mlp_model.pkl')
    rf = joblib.load('models/dt_model.pkl')
    wins = 0
    time.sleep(2)
    for _ in range(number_of_time_playing):
        print(f'Game {_ + 1} :', end=' ')
        time.sleep(1)
        game_over_ = game_over()
        while game_over_ == 0:
            time.sleep(1)
            current_board = get_current_board()
            safes, mines = heuristic_solve(current_board=current_board)
            if safes == [] and mines == []:
                r, c = optimal_move(current_board, mlp, rf)
                cell_id = f'//*[@id="{r+1}_{c+1}"]'
                cell = driver.find_element(By.XPATH, cell_id)
                cell.click()
            else:
                if safes:
                    for r, c in safes:
                        cell_id = f'//*[@id="{r+1}_{c+1}"]'
                        cell = driver.find_element(By.XPATH, cell_id)
                        cell.click()
                if mines:
                    for r, c in mines:
                        cell_id = f'//*[@id="{r+1}_{c+1}"]'
                        cell = driver.find_element(By.XPATH, cell_id)
                        get_current_state = cell.get_attribute('class')
                        if 'flag' not in get_current_state:
                            actions = ActionChains(driver)
                            actions.context_click(cell).perform()
            game_over_ = game_over()
        time.sleep(3) 
        reset_board()
        if game_over_ == 1:
            wins += 1
            print('Win')
        else:
            print('Lose')
        print()
    
    win_rate = (wins / number_of_time_playing) * 100
    
    print(f'win_rate : {win_rate}%')
    
play()