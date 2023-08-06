

import pyautogui as pg
import time
import webbrowser as web

markx = 132
marky = 698
class Prank:

    def Earthquake(markx,marky):
        
        for load in range(10):
            time.sleep(0.02)
            print("*"*(load+1),10 * (load+1),"%")

        print('Let The Fun Begin!')

        while True:
            for i in range(50):
                pg.moveTo(markx + i,marky - i)
    
    def Open(url):
        for i in range(400):
            link = url
            web.open(link)
            print(i+1)



