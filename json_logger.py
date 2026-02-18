import json
import os
from datetime import datetime
from config import LOG_FILE

class JsonLogger:
    def __init__(self):
        self.filename = LOG_FILE
    

    def log_access(self, res_json):
        # Veriyi hazırlayıp kaydeder
        try:
            # Kayıt verisini hazırla
            entry = {
                "tarih": datetime.now().strftime('%Y-%m-%d'),
                "saat": datetime.now().strftime('%H:%M'),
                "ozet": res_json.get('ozet', ''),
                "etiketler": res_json.get('etiketler', []),
                "yorum": res_json.get('yorum', ''),
                "oneri": res_json.get('oneri', '')
            }
            with open(self.filename, 'a', encoding='utf-8') as f:
                json_record = json.dumps(entry, ensure_ascii=False)
                f.write(json_record + "\n")
            #başarıyla kaydedildiği için true döner
            return True
        except Exception as e:
            print(f"HATA: {e}")
            #hata aldığı için false döner 
            return False   
    

    def load_data(self):
        # JSONL dosyasındaki tüm verileri okur ve liste olarak döner.
        data = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue # Bozuk satır varsa atlar
        return data