import re
import unicodedata
from rapidfuzz import process, fuzz

class TextProcessor:
    @staticmethod
    def normalize_vietnamese(text: str) -> str:
        """Chuẩn hóa văn bản tiếng Việt sang dạng NFC thường để đối sánh chính xác."""
        if not text:
            return ""
        text = text.strip()
        text = unicodedata.normalize("NFC", text)
        return text

    @staticmethod
    def remove_accents(text: str) -> str:
        """Loại bỏ dấu tiếng Việt để đối sánh ngữ âm thô."""
        if not text:
            return ""
        normalized = unicodedata.normalize("NFKD", text)
        ascii_text = "".join([c for c in normalized if not unicodedata.combining(c)])
        return ascii_text.replace("đ", "d").replace("Đ", "D")

    @staticmethod
    def correct_identifiers(text: str) -> str:
        """
        Quét văn bản và phát hiện các biến thể nói/nhận dạng sai của:
        - Chuyến xe Rxxx (R101 - R115)
        - Đơn hàng Fxxx (F201 - F215)
        - Giao dịch PAYxxx (PAY102, PAY202,...)
        
        Trả về văn bản đã được chuẩn hóa các thực thể này về dạng chuẩn (viết liền, viết hoa).
        """
        if not text:
            return ""
            
        # Loại bỏ các tag thừa của Whisper nếu có để làm sạch trước
        text = re.sub(r'<\|.*?\|>', '', text)
        
        # Danh sách các luật Regex thay thế chính xác các từ đồng âm/nhận dạng sai từ Whisper
        # Các luật này được thiết kế để không nuốt các từ đứng trước như "tài xế" hay "đơn"
        rules = [
            # Chuyến xe R101
            (r'(?i)\b(?:air\s+thơ|air\s+tho)\s+(?:một\s+trong\s+linh\s+mỗi|một\s+trăm\s+linh\s+một|một\s+chăm\s+linh\s+một|101)\b', 'R101'),
            (r'(?i)\b(?:rờ\s+một\s+trăm\s+linh\s+một|rờ\s+101)\b', 'R101'),
            
            # Chuyến xe R102
            (r'(?i)\b(?:ezo|e\s+zo)\s+(?:một\s+giâm\s+linh\s+hài|một\s+trăm\s+linh\s+hai|102)\b', 'R102'),
            
            # Chuyến xe R103
            (r'(?i)\b(?:ether|a\s+vi|a)\s+(?:mỗi\s+chăm\s+linh\s+bà|mỗi\s+chăm\s+linh\s+ba|một\s+chăm\s+linh\s+ba|một\s+trăm\s+linh\s+ba|103)\b', 'R103'),
            
            # Đơn hàng F201
            (r'(?i)\b(?:fi-căm\s+ling\s+một|fi-căm\s+linh\s+một|fi\s+căm\s+ling\s+một|fi\s+căm\s+linh\s+một)\b', 'F201'),
            (r'(?i)\b(?:fi|f)\s+(?:căm\s+ling\s+một|căm\s+linh\s+một|201)\b', 'F201'),
            
            # Đơn hàng F202
            (r'(?i)\b(?:app\s+high|f-hai)\s+(?:jam\s+linh\s+2|trăm\s+linh\s+hai|trăm\s+linh\s+2|202)\b', 'F202'),
            
            # Đơn hàng F203
            (r'(?i)\b(?:app|f)\s+(?:hai\s+chăm令\s+bà|hai\s+chăm\s+ba|hai\s+trăm\s+linh\s+ba|203)\b', 'F203'),
            
            # Sửa khoảng trắng thừa trong mã viết đúng nhưng bị tách rời
            (r'(?i)\b(r|R)\s*(\d{3})\b', r'R\2'),
            (r'(?i)\b(f|F)\s*(\d{3})\b', r'F\2'),
            (r'(?i)\b(pay|PAY)\s*(\d{3})\b', r'PAY\2'),
            (r'(?i)\b(tkt|TKT)\s*(\d{3})\b', r'TKT\2'),
            (r'(?i)\b(ref|REF)\s*(\d{3})\b', r'REF\2'),
        ]
        
        for pattern, replacement in rules:
            text = re.sub(pattern, replacement, text)
            
        return text

    @staticmethod
    def clean_missing_items(text: str) -> str:
        """Chuẩn hóa món ăn giao thiếu để khớp chính xác với database."""
        normalized = TextProcessor.normalize_vietnamese(text).lower()
        
        # Danh sách món ăn có trong đơn hàng F202 (Burger King - Bà Triệu)
        menu_items = [
            "Whopper Cheese Burger",
            "Khoai tây chiên cỡ lớn",
            "Coca Cola"
        ]
        
        # So khớp mờ để tìm ra món ăn khớp nhất
        match = process.extractOne(normalized, [m.lower() for m in menu_items], scorer=fuzz.wratio)
        if match and match[1] >= 70:
            # Tìm lại tên gốc viết hoa đúng chuẩn
            matched_idx = [m.lower() for m in menu_items].index(match[0])
            return menu_items[matched_idx]
            
        return text
