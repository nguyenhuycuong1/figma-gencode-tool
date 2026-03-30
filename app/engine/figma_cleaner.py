
from app.contanst import UNNECESSARY_KEYS_FOR_FIGMA_CLEANER

class FigmaCleaner:
    @staticmethod
    def clean_node_data(node_id: str, node_data: dict):
        # node_id hiện tại chưa dùng, nhưng có thể giữ lại cho logging
        return FigmaCleaner.remove_unnecessary_data(node_data)
    
    @staticmethod
    def remove_unnecessary_data(node_data: dict):
        # Chuyển list keys thành set để tra cứu cực nhanh
        keys_to_set = set(UNNECESSARY_KEYS_FOR_FIGMA_CLEANER)
        
        # Cách xóa nhanh và Pythonic hơn
        for key in keys_to_set:
            node_data.pop(key, None) # Xóa nếu tồn tại, không lỗi nếu thiếu
        
        # Xử lý đệ quy cho con
        children = node_data.get('children', [])
        if isinstance(children, list):
            for child in children:
                FigmaCleaner.remove_unnecessary_data(child)
                
        return node_data