from django.shortcuts import render
from ORDER.models import OrderItem
from SHOES.models import Shoes, Tag, Brand  
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def prepare_data():
    # Lấy thông tin user, shoe và order từ OrderItem
    orders = OrderItem.objects.all().values('order__user', 'shoe', 'order__id')
    df = pd.DataFrame(orders)
    if df.empty:
        return pd.DataFrame()  
    # Tạo user-item matrix
    user_item_matrix = df.pivot_table(index='order__user', columns='shoe', aggfunc='size', fill_value=0)
    return user_item_matrix

def recommend_shoes(user_id, user_item_matrix, n=5):
    if user_item_matrix.empty or user_id not in user_item_matrix.index:
        return []  
    
    # Tính toán ma trận độ tương đồng cosine giữa người dùng
    similarity_matrix = cosine_similarity(user_item_matrix)
    similarity_df = pd.DataFrame(similarity_matrix, index=user_item_matrix.index, columns=user_item_matrix.index)

    # Lấy danh sách người dùng tương tự
    similar_users = similarity_df[user_id].sort_values(ascending=False)
    
    # Lấy danh sách ID của người dùng tương tự
    similar_user_ids = similar_users.index[1:n+1]  # Loại bỏ chính người dùng hiện tại
    
    # Tổng hợp các sản phẩm mà những người dùng tương tự đã mua
    similar_users_items = user_item_matrix.loc[similar_user_ids].sum(axis=0)
    
    # Lọc ra các sản phẩm mà người dùng hiện tại chưa mua
    user_items = user_item_matrix.loc[user_id]
    recommendations = similar_users_items[user_items == 0].sort_values(ascending=False)

    # Nếu không có sản phẩm nào để đề xuất, trả về danh sách trống
    if recommendations.empty:
        return []

    # Lấy danh sách shoe IDs của các sản phẩm được đề xuất
    recommended_shoe_ids = recommendations.index[:n]

    # Lấy danh sách tag và brand của các đôi giày mà người dùng đã mua
    user_shoes = Shoes.objects.filter(id__in=user_items[user_items > 0].index)
    user_tags = Tag.objects.filter(shoes__in=user_shoes).distinct()
    user_brands = Brand.objects.filter(shoes__in=user_shoes).distinct()

    # Truy vấn giày dựa trên tag và brand của người dùng hiện tại
    tag_based_recommendations = Shoes.objects.filter(tag__in=user_tags).exclude(id__in=user_shoes).distinct()
    brand_based_recommendations = Shoes.objects.filter(brand__in=user_brands).exclude(id__in=user_shoes).distinct()

    # Kết hợp các gợi ý từ người dùng tương tự, tag, và brand
    final_recommendations = list(recommended_shoe_ids) + list(tag_based_recommendations.values_list('id', flat=True)) + list(brand_based_recommendations.values_list('id', flat=True))
    final_recommendations = list(dict.fromkeys(final_recommendations))  # Loại bỏ các sản phẩm trùng lặp
    
    # Lấy danh sách tên giày từ các shoe IDs được đề xuất
    recommended_shoes = Shoes.objects.filter(id__in=final_recommendations[:n]).values_list('name', flat=True)

    return recommended_shoes

