import datetime
import pandas as pd
import streamlit as st
import os
import pickle
import matplotlib.pyplot as plt

def calculate_duration(start_time, end_time):
    """Calculate the duration between two datetime objects."""
    return (end_time - start_time).total_seconds() / 60  # Duration in minutes

def load_data():
    """Load data from a file if it exists."""
    if os.path.exists("data.pkl"):
        with open("data.pkl", "rb") as file:
            return pickle.load(file)
    return []

def save_data(data):
    """Save data to a file."""
    with open("data.pkl", "wb") as file:
        pickle.dump(data, file)

def main():
    """Main function to run the Streamlit app."""
    st.title("Çalışan Ürün Süre Analizi")

    # Load or initialize data
    if "data" not in st.session_state:
        st.session_state.data = load_data()

    # Sidebar menu
    menu = ["Yeni Kayıt Ekle", "Verileri Analiz Et", "Kayıtlı Verileri Görüntüle"]
    choice = st.sidebar.selectbox("Menü", menu)

    if choice == "Yeni Kayıt Ekle":
        st.header("Yeni Kayıt Ekle")

        with st.form("entry_form"):
            employee_name = st.text_input("Çalışan Adı")
            product_name = st.text_input("Ürün Adı")
            start_time = st.text_input("Başlangıç Zamanı (YYYY-MM-DD HH:MM)")
            end_time = st.text_input("Bitiş Zamanı (YYYY-MM-DD HH:MM)")
            submit_button = st.form_submit_button("Kaydı Ekle")

            if submit_button:
                try:
                    start_time_dt = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
                    end_time_dt = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M")
                    if end_time_dt <= start_time_dt:
                        st.error("Bitiş zamanı, başlangıç zamanından sonra olmalıdır.")
                    else:
                        duration = calculate_duration(start_time_dt, end_time_dt)
                        new_entry = {
                            "Çalışan": employee_name,
                            "Ürün": product_name,
                            "Başlangıç": start_time_dt,
                            "Bitiş": end_time_dt,
                            "Süre (dk)": duration
                        }
                        st.session_state.data.append(new_entry)
                        save_data(st.session_state.data)
                        st.success("Kayıt başarıyla eklendi!")
                except ValueError as e:
                    st.error(f"Hatalı giriş: {e}")

    elif choice == "Verileri Analiz Et":
        st.header("Verileri Analiz Et")

        if not st.session_state.data:
            st.warning("Henüz veri yok.")
        else:
            df = pd.DataFrame(st.session_state.data)

            # Filtreleme Seçenekleri
            st.subheader("Filtreleme Seçenekleri")
            unique_employees = df["Çalışan"].unique()
            unique_products = df["Ürün"].unique()

            selected_employee = st.selectbox("Çalışan Seç", ["Tümü"] + list(unique_employees))
            selected_product = st.selectbox("Ürün Seç", ["Tümü"] + list(unique_products))

            # Filtre Uygulama
            if selected_employee != "Tümü":
                df = df[df["Çalışan"] == selected_employee]

            if selected_product != "Tümü":
                df = df[df["Ürün"] == selected_product]

            st.subheader("Filtrelenmiş Kayıtlar")
            st.dataframe(df)

            if not df.empty:
                avg_duration = df.groupby("Çalışan")["Süre (dk)"].mean()
                std_dev_duration = df.groupby("Çalışan")["Süre (dk)"].std()

                st.subheader("Çalışan Bazlı Ortalama Süreler")
                st.dataframe(avg_duration)

                st.subheader("Çalışan Bazlı Standart Sapmalar")
                st.dataframe(std_dev_duration)

                # Standart Sapma Grafiği
                st.subheader("Çalışanların Standart Sapma Grafiği")
                fig, ax = plt.subplots()
                std_dev_duration.plot(kind='bar', ax=ax, legend=False)
                ax.set_ylabel("Standart Sapma (dk)")
                ax.set_title("Çalışan Bazlı Süre Standart Sapmaları")
                st.pyplot(fig)

                fastest = avg_duration.idxmin()
                slowest = avg_duration.idxmax()

                st.success(f"En hızlı çalışan: {fastest}")
                st.error(f"En yavaş çalışan: {slowest}")

    elif choice == "Kayıtlı Verileri Görüntüle":
        st.header("Kayıtlı Veriler")

        if not st.session_state.data:
            st.warning("Henüz kayıtlı veri yok.")
        else:
            df = pd.DataFrame(st.session_state.data)

            # Filtreleme Seçenekleri
            st.subheader("Filtreleme Seçenekleri")
            unique_employees = df["Çalışan"].unique()
            unique_products = df["Ürün"].unique()

            selected_employee = st.selectbox("Çalışan Seç", ["Tümü"] + list(unique_employees))
            selected_product = st.selectbox("Ürün Seç", ["Tümü"] + list(unique_products))

            # Filtre Uygulama
            if selected_employee != "Tümü":
                df = df[df["Çalışan"] == selected_employee]

            if selected_product != "Tümü":
                df = df[df["Ürün"] == selected_product]

            st.subheader("Filtrelenmiş Kayıtlar")
            st.dataframe(df)

if __name__ == "__main__":
    main()
