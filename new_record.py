import streamlit as st
from datetime import datetime
from ai_service import AIService
from json_logger import JsonLogger
from config import API_KEY




class NewRegistration:
    def __init__(self):
        # .env dosyasından api aldıktan sonra alınan keyi getirir
        self.API_KEY = API_KEY
       

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

