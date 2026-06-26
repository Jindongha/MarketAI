FOOD_IMAGES = {
    "과일":     "https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=400&h=400&fit=crop",
    "딸기":     "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400&h=400&fit=crop",
    "감귤":     "https://images.unsplash.com/photo-1547514701-42782101795e?w=400&h=400&fit=crop",
    "포도":     "https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=400&h=400&fit=crop",
    "채소":     "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=400&fit=crop",
    "육류":     "https://images.unsplash.com/photo-1544025162-d76694265947?w=400&h=400&fit=crop",
    "삼겹살":   "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=400&h=400&fit=crop",
    "닭":       "https://images.unsplash.com/photo-1604503468506-a8da13d11520?w=400&h=400&fit=crop",
    "수산물":   "https://images.unsplash.com/photo-1534482421-64566f976cfa?w=400&h=400&fit=crop",
    "연어":     "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400&h=400&fit=crop",
    "유제품":   "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=400&fit=crop",
    "달걀":     "https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=400&h=400&fit=crop",
    "라면":     "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=400&h=400&fit=crop",
    "냉동":     "https://images.unsplash.com/photo-1585704032915-c3400305e979?w=400&h=400&fit=crop",
    "만두":     "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=400&h=400&fit=crop",
    "음료":     "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=400&h=400&fit=crop",
    "커피":     "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400&h=400&fit=crop",
    "물":       "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400&h=400&fit=crop",
    "베이커리": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=400&fit=crop",
    "빵":       "https://images.unsplash.com/photo-1549931319-a545dcf3bc7c?w=400&h=400&fit=crop",
    "과자":     "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=400&fit=crop",
    "스낵":     "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=400&fit=crop",
    "견과류":   "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop",
    "간편식":   "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=400&h=400&fit=crop",
    "통조림":   "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=400&h=400&fit=crop",
    "김치":     "https://images.unsplash.com/photo-1583224964978-2257b8a0d4a5?w=400&h=400&fit=crop",
    "소스":     "https://images.unsplash.com/photo-1472476443507-c7a5948772fc?w=400&h=400&fit=crop",
    "기름":     "https://images.unsplash.com/photo-1474979153345-0a30baba6ff2?w=400&h=400&fit=crop",
}

def get_image(title: str, category: str = "") -> str:
    combined = title + " " + (category or "")
    for keyword, url in FOOD_IMAGES.items():
        if keyword in combined:
            return url
    return "https://images.unsplash.com/photo-1498654896293-37aacf113fd9?w=400&h=400&fit=crop"
