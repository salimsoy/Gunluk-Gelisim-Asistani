import json
import os
from datetime import datetime
from config import MAX_LOG_SIZE_MB, DAILY_LIMIT, LOG_FILE


class LogCheck:
    def __init__(self):
        self.filename = LOG_FILE
    
    def log_size_check(self):
        # maksimum dosya boyutuna ulaşılıp ulaşılmadığını kontrol eder
        try:
            file_size = os.path.getsize(self.filename)
            if MAX_LOG_SIZE_MB * (1024 * 1024) <= file_size:
                raise ValueError(f"Dosya maksimum {MAX_LOG_SIZE_MB} mb olabilir")
            return True
        except ValueError:
            return False
    

    def daily_limit_check(self):
        # günlük limit değeri aşıp aşmadığını kontrol eder
        date_str = datetime.now().strftime('%Y-%m-%d')
        counter = 0
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
              
            # satırları tersten kontrol eder tarihleri bu gün ile aynı olanları kontrol eder ve ilk farklı tarihle karşılaşınca çıkar 
            for line in reversed(lines):   
                if line:
                    log_data = json.loads(line)
                    registration_date = log_data["tarih"]
                    if date_str == registration_date:
                        counter += 1
                    else:
                        break

            if counter >= DAILY_LIMIT:
                return False
            return True

        except Exception as e:
            print(f"Hata: {e}")
        return None