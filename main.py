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