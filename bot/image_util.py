from selenium import webdriver
from PIL import Image
from io import BytesIO
from os import path
from datetime import datetime

def screenshot_element(html_file):
    file_name = f'trending_stocks_{datetime.now().microsecond}.png'
    if html_file:
        with webdriver.Firefox() as fox:
            fox.get(html_file)
            table = fox.find_element_by_id('stockTable')
            location = table.location
            size = table.size
            png = fox.get_screenshot_as_png()

        img = Image.open(BytesIO(png))

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        img = img.crop((left,top,right,bottom))
        file_path = path.join('C:\\Users\\Apolinar\\stock_bot\\bot\\table_images',file_name) 
        img.save(file_path)
        return file_path
        
