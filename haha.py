import pandas as pd
import os
import shutil

# Thay đổi thư mục hình ảnh của bạn ở đây
image_directory = "E:\zzzzzzzzz\IT\zz Tai lieu hoc tap\Data Mining\images"

# Thay đổi thư mục đầu ra của bạn ở đây
output_directory = "E:\zzzzzzzzz\IT\zz Tai lieu hoc tap\Data Mining\image"

# Đọc tập tin csv và lấy các id
dataframe = pd.read_csv("E:\zzzzzzzzz\IT\zz Tai lieu hoc tap\Data Mining\web_flask\dataset.csv")
ids = list(dataframe["u_id"])
# Duyệt qua các tập tin hình ảnh và di chuyển nếu tên file trùng với id
for filename in os.listdir(image_directory):
    filepath = os.path.join(image_directory, filename)
    image_id = filename.replace(".jpg","") # bỏ phần mở rộng ".jpg" để chỉ lấy id
    if image_id in ids:
        output_filepath = os.path.join(output_directory, filename)
        shutil.copy(filepath, output_filepath)