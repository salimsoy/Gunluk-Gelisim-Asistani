import google.generativeai as genai
import json
from config import MODEL_NAME

class AIService:
    def __init__(self, API_KEY):
        genai.configure(api_key=API_KEY) 
    
    def model_selection(self):
        # modeli oluşturur
        model = genai.GenerativeModel(MODEL_NAME)
        return model

    def prompter(self, user_input):
        #verilecek promptu oluşturur
        prompt = f"""
                Sen bir öğrenme analizi yapan yapay zekâ asistanısın.
                Görevin: Kullanıcının "Bugün ne öğrendim?" metnini analiz etmek.
                ÇIKTI KURALLARI (ÇOK KRİTİK):
                - SADECE geçerli JSON döndür.
                - JSON dışında TEK BİR KELİME bile yazma.
                - Açıklama, yorum, giriş cümlesi yazma.
                - Alan adlarını ASLA değiştirme.
                - Etiket sayısı TAM OLARAK 3 olmalı.
                - Cevaplar net ve Türkçe olmalı.
                İstenen JSON formatı:
                {{
                    "ozet": "Öğrenilen bilginin kısa özeti",
                    "etiketler": ["etiket1", "etiket2", "etiket3"],
                    "yorum": "Basit bir geri bildirim yorumu",
                    "oneri": "Kısa gelişim önerisi"
                }}
                Kullanıcı metni:{user_input}
                """
        return prompt
    
    def regulator(self, response):
        # json metnini temizletip anlamlı hale getirir
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        try:
            res_json = json.loads(clean_text)
        except json.JSONDecodeError:
            raise ValueError("Model geçerli JSON döndürmedi.")
        return res_json
        
    
    def main(self, user_input):
        model = self.model_selection()

        prompt = self.prompter(user_input)

        response = model.generate_content(prompt)

        res_json = self.regulator(response)

        return res_json

