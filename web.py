from flask import Flask, render_template, request
import math
import pandas as pd


app = Flask(__name__)
products_df = pd.read_csv('E:\zzzzzzzzz\IT\zz Tai lieu hoc tap\Data Mining\dataset.csv')
products = list()
for index, row in products_df.iterrows():
    temp = {'u_id': str(row["u_id"]), 
            'name': str(row["name"]), 
            'price': '{:.2f}'.format(row["original_price"]/ 100), 
            'total_ratings': str(row["total_ratings"]),
            'rating': str(row["rating"]),
            'description': str(row["description"])}
    products.append(temp)

def paginate(products, page):
    total_pages = math.ceil(len(products) / 30)
    start_index = (page - 1) * 30
    end_index = start_index + 30
    current_products = products[start_index:end_index]
    return current_products, total_pages



@app.route('/')
def main():
    page = int(request.args.get('page', 1))
    current_products, total_pages = paginate(products, page)
    print(total_pages)
    return render_template('index.html', current_products=current_products, total_pages=total_pages, page=page)


if __name__ == "__main__":
    app.run()