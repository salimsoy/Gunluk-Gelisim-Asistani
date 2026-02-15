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





