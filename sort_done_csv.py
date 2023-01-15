import csv
import pandas as pd
import numpy as np
import random

chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
section = input('Введите название категории которую будем сортировать: ')
razdel = int(input('Введите название номер раздела от 29: '))
tags = []

sort_csv = pd.read_csv(f'{section}/info.csv', sep=';')
sort_csv = sort_csv.sort_values(by='number', ascending=True, inplace=False)
sort_csv.to_csv(f'{section}/info_sort.csv', sep=';', encoding='utf-8', index=False)


with open(f'{section}/info_db.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter=';', dialect='excel')
    writer.writerow(['id', 'user_id', "category_id", 'image_name', 'thumb', 'file', 'track_id', 'title', 'date', 'resolution', 'image_width',  'image_height', 'extensions', 'description', 'tags', 'colors', 'price', 'total_like', 'is_free', 'is_featured', 'attribution', 'total_view', 'total_downloads','is_active', 'status', 'reason', 'admin_id', 'reviewer_id', 'created_at', 'updated_at'])

with open(f'{section}/info_sort.csv', 'r', encoding='utf-8', newline='') as file:
    reader = csv.DictReader(file, delimiter=';')
    id = 0
    for row in reader:
        imahe_height = row['resolution'][:-3].split('x')
        track_id = ''
        for j in range(12):
            track_id += random.choice(chars)
        with open(f'{section}/info_db.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';', dialect='excel')
            writer.writerow([id, 4, razdel, f'{section}_{row["number"]}.jpg', f'preview_{section}/preview_{section}_{row["number"]}.jpg', f'main_{section}/{section}_{row["number"]}.jpg', track_id, row['name'].capitalize(), '2023-01-12', row['resolution'][:-3], imahe_height[0][:-1], imahe_height[1][1:], '["jpg"]', row['name'].capitalize(),  row['tags'].replace("'", '"'), '["ffffff"]', 0.00000000, 0, 1, 0, 1, 0, 0, 1, 1, 'NULL', 1, 0, '2023-01-12', '2023-01-13'])