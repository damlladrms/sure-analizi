import cv2
import streamlit as st
import time
from datetime import datetime

def main():
    st.title("Canlı Video ile Çalışan Süresi Hesaplama")

    # Video Akışını Başlatma
    run_video = st.checkbox("Canlı Videoyu Başlat")
    calculate_time = st.checkbox("Süreyi Başlat ve Hesapla")
    stop_video = st.checkbox("Videoyu Durdur")

    cap = None
    start_time = None
    end_time = None

    if run_video:
        # Web kamerasını başlat
        cap = cv2.VideoCapture(0)
        st.warning("Canlı video başlatıldı. Çalışan görüldüğünde süre hesaplamayı başlatabilirsiniz.")

        # Streamlit üzerinden canlı video görüntüsü
        while run_video and not stop_video:
            ret, frame = cap.read()
            if not ret:
                st.error("Kamera akışı açılamıyor.")
                break

            # OpenCV ile çerçeveleme
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame, channels="RGB", caption="Canlı Video Akışı", use_column_width=True)

            if calculate_time:
                if start_time is None:
                    start_time = datetime.now()
                    st.success(f"Başlangıç zamanı: {start_time.strftime('%H:%M:%S')}")
                else:
                    elapsed_time = (datetime.now() - start_time).seconds
                    st.info(f"Süre: {elapsed_time} saniye")

    if stop_video and cap is not None:
        cap.release()
        st.warning("Video akışı durduruldu.")

        if start_time:
            end_time = datetime.now()
            duration = (end_time - start_time).seconds
            st.success(f"Çalışan süresi: {duration} saniye")
        st.warning("Kamera kapatıldı.")

if __name__ == "__main__":
    main()
