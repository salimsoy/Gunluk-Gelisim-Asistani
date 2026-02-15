
# Günlük Gelişim Asistanı

## Proje Tanıtımı
Bu Proje, her gün öğrendiğimiz, fark ettiğimiz ya da düşündüğümüz şeyleri tek bir arayüzde toplayıp, bunu yapay zekâ ile özetleyen, etiketleyen ve üzerine yorumlar yapan bir sistemdir.

## Streamlit
Projenin kullanıcı arayüzü ve web tabanlı etkileşimi **Streamlit** kütüphanesi kullanılarak geliştirilmiştir.
Streamlit, özellikle veri bilimi ve makine öğrenmesi projeleri için tasarlanmış, saf Python kodu ile hızlı ve etkileşimli web uygulamaları oluşturmayı sağlayan açık kaynaklı bir kütüphanedir.
Bunu tercih edilmesinin sebebi ise HTML/CSS veya JavaScript bilgisine ihtiyaç duymadan, Python'daki veri yapılarını doğrudan görselleştirebilmesi ve modüler yapısı sayesinde projenin geliştirme sürecini hızlandırmıştır.


## Çalışma Mantığı ve Çıktıları

Sistemin süreci şu adımlardan oluşur:

### 1. Veri Girişi
Kullanıcı, arayüz üzerinden o gün öğrendiği teknik veya teorik bilgiyi metin formatında girer.

### 2. AI İşleme
Girilen metin, özel olarak tasarlanmış bir **Prompt** ile sarmalanarak Gemini API'ye iletilir. Model, metni analiz ederken JSON formatına sadık kalmaya zorlanır.

### 3. Yapılandırılmış Çıktılar 
Sistem, her giriş için aşağıdaki 4 veriyi üretir ve ekrana basar:
* **Özet:** Girilen uzun metnin, temel yetkinlikleri vurgulayan kısa ve net özeti.
* **Etiketleme:** İçerikten çıkarılan, aranabilirliği sağlayan 3 adet anahtar kelime.
* **AI Yorumu:** Öğrenilen konunun önemine dair yapay zeka tarafından üretilen bağlamsal geri bildirim.
* **Gelişim Önerisi:** Kullanıcının bir sonraki adımda ne öğrenmesi veya araştırması gerektiğine dair aksiyon odaklı tavsiye.

### 4. Veri Saklama (Storage)
Üretilen tüm bu çıktılar, JSON Lines (.jsonl) formatında yerel diskte saklanır.

---

## Modüller

Sistem, **Sorumlulukların Ayrılığı (Separation of Concerns)** ilkesine göre tasarlanmış olup, Ana Modüller ve Alt Modüller olarak ikiye ayrılmıştır.

### 1. Ana Modüller (Arayüz Katmanı)
* **`Main (App)` Modülü:** Uygulamanın giriş noktasıdır. Navigasyonu ve sayfa yönlendirmelerini yönetir.
* **`NewRegistration` Modülü:** Kullanıcının veri girişi yaptığı ve anlık analiz aldığı ekrandır.
* **`PastRegistration` Modülü:** Eski verilerin görüntülendiği ve yönetildiği ekrandır.

### 2. Alt Modüller (Servis Katmanı)
* **`AIService`:** Yapay zeka ile iletişimi sağlayan servis.
* **`JsonLogger`:** Log işlemlerini yöneten sınıf.

---

##  Ana Modüller

### 1. Main (App) Modülü
Uygulamanın omurgasını oluşturur. Yan menü üzerinden kullanıcıyı "Yeni Kayıt" veya "Geçmiş Analizler" sayfalarına yönlendirir.
Şu şekilde çalışır: `Streamlit` `sidebar.selectbox` bileşenini kullanarak kullanıcının seçimini dinler ve duruma göre ilgili sınıfın (`NewRegistration` veya `HistoryManager`) `main` metodunu tetikler.

### 2. NewRegistration Modülü
Kullanıcıdan "Bugün ne öğrendin?" sorusuna cevap alır, bu metni işler ve yapay zeka analiz sonuçlarını ekrana kartlar halinde basar.
* **Nasıl Çalışır?**
    * Kullanıcı metni girip butona bastığında `AIService` modülünü çağırır.
    * Gelen JSON formatındaki yanıtı (Özet, Etiketler, Yorum, Öneri) ayrıştırır.
    * Sonuçları `JsonLogger` modülü aracılığıyla kaydeder.
    * Aynı gün içinde mükerrer kayıt yapılmasını engellemek için tarih kontrolü yapar.

### 3. PastRegistration Modülü
* **Ne Yapar?** Kaydedilmiş tüm verileri tarih sırasına göre (yeniden eskiye) listeler. Her kaydın detayını açılır/kapanır (Accordion) bir yapıda sunar ve silme imkanı tanır.
* **Nasıl Çalışır?**
    * JSONL dosyasını satır satır okur.
    * `st.expander` kullanarak her kaydı bir başlık altında gizler.

---

## ⚙️ Alt Modüllerin Detaylı Açıklaması

### 1. AIService 
* **Görevi:** Google Gemini API ile uygulama arasındaki köprüdür.
* **İşleyişi:**
    * API anahtarını yapılandırır ve modeli (`gemini-2.5-flash`) hazırlar.
    * **Prompt Engineering:** Kullanıcı girdisini, sistemin beklediği JSON formatına zorlayan bir Prompt ile sarmalar.
    * Gelen ham metin yanıtını temizler ve Python sözlük yapısına dönüştürür.

### 2. JsonLogger (Veri Yöneticisi)
* **Görevi:** Verilerin kalıcı olarak saklanmasından ve okunmasından sorumludur.
* **İşleyişi:**
    * **Kayıt:** Verileri `JSON Lines (JSONL)` formatında, her satıra bir JSON objesi gelecek şekilde `append` (ekleme) modunda yazar. UTF-8 kodlaması ile Türkçe karakter sorununu çözer.
    * **Okuma:** Dosyayı satır satır okuyarak bellek dostu bir işlem gerçekleştirir ve uygulamanın istedği bu gün analiz yapıldı mı kontrolünün yapılması için en son eklenen veririn tarihini bize verir.

---

## 1. Sistem Ana Modülü (main.py):
```python
import streamlit as st
from new_record import NewRegistration
from past_record import PastRegistration

class App:
    def main(self):
        st.set_page_config(page_title="Gelişim Asistanı")

        # Sol menü oluşturma
        sayfa = st.sidebar.selectbox("Gidilecek Sayfa", ["Yeni Kayıt", "Geçmiş Analizler"])

        if sayfa == "Yeni Kayıt":
            #yeni günlük gelişim analizi yapılacak kısma yönlendirir
            new_negistration = NewRegistration()
            new_negistration.main()

        elif sayfa == "Geçmiş Analizler":
            #geçmiş kayıtların görülebileceği ekrana yönlendirir 
            past_registration = PastRegistration()
            past_registration.main()

           

if __name__ == "__main__":
    islem = App()
    islem.main()
```
## 2. Yeni Kayıt Modülü (new_record.py):
```python
import streamlit as st
from datetime import datetime
from ai_service import AIService
from json_logger import JsonLogger

class NewRegistration:
    def __init__(self):
        self.API_KEY = "API"
    

    def analysis_result(self, res_json):
        st.divider()
        st.subheader("Analiz Sonuçları")
        
        st.info(f"**Özet:**\n\n{res_json['ozet']}")

        # Yorum ve öneriyi yan yana iki kolon halinde gösterir
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**AI Yorumu:**\n\n{res_json['yorum']}")
        with col2:
            st.success(f"**Gelişim Önerisi:**\n\n{res_json['oneri']}")

        st.info(f"**Etiketler:**\n\n{', '.join(res_json['etiketler'])}")


    def main(self):
        # Sınıfları ve tarih değişkenini başlat
        ai_manager = AIService(self.API_KEY)
        logger = JsonLogger()
        date_str = datetime.now().strftime('%Y-%m-%d')

        # Sayfa başlığı
        st.title("Günlük Gelişim Asistanı")
        st.markdown("Bugün öğrendiklerini yaz, AI analiz etsin")

        # Kullanıcıdan veri girişi alır
        user_input = st.text_area("Bugün ne öğrendin?", height=150, placeholder="Örn: Bugün OpenCV kütüphanesini öğrendim...")

        # Bugün zaten kayıt yapılmış mı kontrol eder
        if logger.get_last_log_efficient() == date_str:
            st.markdown("Bu gün analiz yaptın geçmiş kayıtları kontrol et.")
        else:
            if st.button("Analiz Et"):
                if user_input:
                    #burada kullanıcıya sistemin arka planda çalıştığını göstermek için beklemesi gerektiğini anlaması için yüklenme ibaresi koyar
                    with st.spinner("Gemini düşünüyor..."):
                        try:
                            # Metni ai servisine gönderir
                            res_json = ai_manager.main(user_input)

                            # Gelen sonucu json olarak kaydeder
                            inspection = logger.log_access(res_json)

                            if inspection:
                                print("Veriler başarıyla Kaydedildi")
                            else:
                                "Verier Kaydedilemedi"

                            # Analiz Sonuçlarını gösterir
                            self.analysis_result(res_json)

                        except Exception as e:
                            print(f"Hata: {e}")

                else:
                    st.warning("Lütfen önce bir şeyler yazın!")


```
## 3. Geçmiş Kayıtlar Modülü (past_record.py)
```python
import streamlit as st
from json_logger import JsonLogger


class PastRegistration:
    def __init__(self, filename='gelisim_verileri.jsonl'):
        self.filename = filename
    

    def analysis_result(self, tarih, saat, ozet, yorum, oneri, etiketler):
        # bir analizin detaylarını açılır kapanır kutu içinde gösteririlir
        heading = f"{tarih} | {saat}"
        # açılır kapanır kutu
        with st.expander(heading):
            
            st.divider()
            
            st.info(f"**Özet:**\n\n{ozet}")
            # Yorum ve öneriyi yan yana iki sütunda göster
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**AI Yorumu:**\n\n{yorum}")
            with col2:
                st.success(f"**Gelişim Önerisi:**\n\n{oneri}")

            st.info(f"**Etiketler:**\n\n{', '.join(etiketler)}")


    def main(self):

        st.title("Geçmiş Analizler")
        st.markdown("")

        logger = JsonLogger()

        # Kayıtlı verileri dosyadan yükler
        records = logger.load_data()

        # hiç kayıt yoksa uyarı ver ve sistemi durdurur
        if not records:
            st.info("Geçmiş bir kayıt yok.")
            return
        
        # kayıtları sondan başa olacak şekilde döngüye alır
        for record in reversed(records):
            # Bütüm veri ayrılır
            tarih = record.get("tarih", "Tarih Yok")
            saat = record.get("saat", "Saat Yok")
            ozet = record.get("ozet", "Özet Yok")
            etiketler = record.get("etiketler", [])
            yorum = record.get("yorum", "")
            oneri = record.get("oneri", "")

            # verilerde analiz detaylarının gösterileceği kısma götürür
            self.analysis_result(tarih, saat, ozet, yorum, oneri, etiketler)

```
### 4. Yapay Zeka Servisi (ai_sevice.py)

```python
import google.generativeai as genai
import json

class AIService:
    def __init__(self, API_KEY):
        genai.configure(api_key=API_KEY) 
    
    def model_selection(self):
        # modeli oluşturur
        model = genai.GenerativeModel('gemini-2.5-flash')
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
        res_json = json.loads(clean_text)
        return res_json
    
    def main(self, user_input):
        model = self.model_selection()

        prompt = self.prompter(user_input)

        response = model.generate_content(prompt)

        res_json = self.regulator(response)

        return res_json

```
### 5. Log Yöneticisi (json_logger.py)
```python
import json
import os
from datetime import datetime

class JsonLogger:
    def __init__(self, filename='gelisim_verileri.jsonl'):
        self.filename = filename
    
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
    

    def get_last_log_efficient(self):
        # Son satırdaki verinin tarihini getirir bu sayede tarih karşılaştırması yapılabilir
        last_line = None
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                # Dosyayı satır satır döner, en son son satırı tutar
                for line in f:
                    last_line = line
            
            if last_line:
                log_data = json.loads(last_line)
                registration_date = log_data["tarih"]

                return registration_date
        except Exception as e:
            print(f"Hata: {e}")
        return None
    

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
```
