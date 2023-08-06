from adnar_scraper.utility.data_loader import DataLoader
from adnar_scraper.utility.database_controller import DatabaseController

d = DatabaseController(selected_database='item').get_all_data_in_path(db_name='naver_image_scraper/2020_12_16_14_286/')
DataLoader.save_pickle_data(data=d, file_path='E:/databases/ver_1/local_database/item_database/separated_category_items/separated_items_with_images/패션의류&여성의류&티셔츠')

