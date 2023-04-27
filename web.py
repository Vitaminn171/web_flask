from flask import Flask, render_template, request
import math
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)
products_df = pd.read_csv('dataset.csv')
products = list()

for index, row in products_df.iterrows():
    temp = {'u_id': str(row["u_id"]), 
            'name': str(row["name"]), 
            'price': '{:.2f}'.format(row["original_price"]/ 100), 
            'total_ratings': str(row["total_ratings"]),
            'rating': str(row["rating"]),
            'description': row["description"]}
    products.append(temp)


"""
Hệ thống đề xuất sử dụng ma trận tần suất TF-IDF (term frequency-inverse document frequency) và độ đo tương đồng cosine để tìm kiếm các sản phẩm liên quan trong một bộ dữ liệu.

Đầu tiên, TfidfVectorizer được sử dụng để khởi tạo một thể hiện của lớp chứa các thông số cho việc mã hóa tài liệu thành ma trận TF-IDF. Khi được gọi với không có tham số nào, các giá trị mặc định được sử dụng. Bạn cũng có thể chỉ định một số tham số để điều chỉnh các thông số khác như kích cỡ của từ vựng, loại bỏ từ dừng và xác định chiến lược mã hóa (bi-gram hay tri-gram).

Sau đó, phương thức fit_transform được gọi trên danh sách các tên sản phẩm (products_df['name']) để biến đổi chúng thành một ma trận TF-IDF.

Cuối cùng, phương thức cosine_similarity được áp dụng lên ma trận TF-IDF để tính toán độ đo tương đồng cosine giữa tất cả các cặp sản phẩm. Kết quả là một ma trận vuông trong đó giá trị ở hàng i, cột j là độ đo tương đồng cosine giữa sản phẩm i và sản phẩm j.
"""

# Tạo ma trận tần xuất
tfidf_vectorizer = TfidfVectorizer()

# gọi danh sách các tên sản phẩm (products_df['name']) để biến đổi thành một ma trận tần xuất
tfidf_matrix = tfidf_vectorizer.fit_transform(products_df['name'])

# tính điểm cosine giữa tất cả các cặp sản phẩm
cosine_sim = cosine_similarity(tfidf_matrix)

def recommend_products(product_name, cosine_sim=cosine_sim):
    # tìm vị trí của sản phẩm trong dataframe và tính điểm cosine similarity với tất cả các sản phẩm khác
    # df_sub = products_df[products_df['name'].str.contains(product_name, case=False)] tìm theo thông số hoặc tùy mình nhập, vd: asus hoặc 8GB/ 512GB SSD
    #idx = df_sub.index[0]

    idx = products_df[products_df['name'] == product_name].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # sắp xếp danh sách sản phẩm theo điểm cosine similarity giảm dần
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # lấy danh sách top 10 sản phẩm có điểm cosine similarity cao nhất và trả về
    product_indices = [i[0] for i in sim_scores[1:6]] # lấy 5 sản phẩm có điểm cao nhất bỏ đi sản phẩm đầu tiên do là chính nó
    product_scores = [i[1] for i in sim_scores[1:6]] # lấy điểm của 5 sản phẩm cao nhất
    return products_df.loc[product_indices, ["u_id"]].assign(similarity_score=product_scores)

def paginate(products, page):
    total_pages = math.ceil(len(products) / 32)
    start_index = (page - 1) * 32
    end_index = start_index + 32
    current_products = products[start_index:end_index]
    return current_products, total_pages

def find_by_id(list_id,result_list,products_list):
    for id in list_id:
        temp = next(item for item in products_list if str(item["u_id"]) == id)
        result_list.append(temp) 
    return result_list

@app.route('/')
def main():
    page = int(request.args.get('page', 1))
    current_products, total_pages = paginate(products, page)
    return render_template('index.html', current_products=current_products, total_pages=total_pages, page=page)


@app.route('/detail/<string:product_id>', methods=['GET', 'POST'])
def detail(product_id):
    product_detail = next(item for item in products if str(item["u_id"]) == product_id)
    product_detail['description'] = eval(product_detail['description'])
    name = str(product_detail['name'])

    # get recommend products
    recommendations = recommend_products(name)

    # get products by recommend_id
    related_products = list()
    related_products = find_by_id(recommendations["u_id"],related_products,products)
    print(related_products)
    
    
    return render_template('detail.html', product=product_detail, related_products=related_products)

if __name__ == "__main__":
    app.run()