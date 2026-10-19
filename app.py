import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model.fitness_model import FitnessModel

# Sæt side-konfiguration
st.set_page_config(page_title="Styrketræning Tracker", page_icon="💪", layout="wide")

# Initialiser model (bruger vores eksisterende SQLite database)
@st.cache_resource
def get_model():
    model = FitnessModel("fitness.db")
    model.load_data()
    return model

model = get_model()
model.load_data() # Genindlæs data for at få seneste ændringer

# Sidebar navigation
st.sidebar.title("💪 Trænings-Tracker")
menu = st.sidebar.radio("Navigation", ["🏠 Forside", "📈 Styrkeudvikling (Graf)", "📋 Træningsoversigt", "⚖️ Kropsvægt", "📅 Træningsprogram"])

# --- FORSIDE ---
if menu == "🏠 Forside":
    st.title("Velkommen til din Styrketræning Tracker")
    st.write("Brug menuen til venstre til at navigere mellem dine grafer, træningspas, kropsvægt og program.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **Tip:** Du kan køre denne app lokalt på mobilen via dit lokale Wi-Fi, eller uploade den gratis til skyen!")
    with col2:
        st.success("🚀 **Database:** Forbundet til `fitness.db`.")

# --- GRAF ---
elif menu == "📈 Styrkeudvikling (Graf)":
    st.title("📈 Styrkeudvikling (Estimeret 1RM)")
    
    exercises = model.get_exercises()
    selected_ex = st.selectbox("Vælg øvelse", ["Alle øvelser"] + exercises)
    
    plot_df = model.get_aggregated_plot_data(selected_ex)
    
    if plot_df is not None and not plot_df.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        
        if selected_ex == "Alle øvelser":
            for ex, group in plot_df.groupby("Øvelse"):
                ax.plot(group["Dato"], group["Estimeret_1RM"], marker="o", label=ex)
            ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        else:
            ax.plot(plot_df["Dato"], plot_df["Estimeret_1RM"], marker="o", color="#4CAF50", linewidth=2)
            
        ax.set_xlabel("Dato")
        ax.set_ylabel("Estimeret 1RM (kg)")
        ax.grid(True, linestyle="--", alpha=0.6)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("Ingen data fundet til grafen endnu.")

# --- TRÆNINGSOVERSIGT ---
elif menu == "📋 Træningsoversigt":
    st.title("📋 Træningsoversigt & Sæt")
    
    sessions = model.get_workout_sessions()
    if not sessions.empty:
        st.dataframe(sessions, use_container_width=True)
        
        st.divider()
        st.subheader("Se detaljer for et pas")
        selected_date = st.selectbox("Vælg dato for pas", sessions["Dato"].tolist())
        
        if selected_date:
            details = model.get_session_details(selected_date)
            st.write(f"Enkelte løft den {selected_date}:")
            st.dataframe(details, use_container_width=True)
    else:
        st.info("Ingen træningspas registreret endnu.")

# --- KROPSVÆGT ---
elif menu == "⚖️ Kropsvægt":
    st.title("⚖️ Kropsvægt Log")
    
    if model.df_bodyweight is not None and not model.df_bodyweight.empty:
        st.dataframe(model.df_bodyweight[["Dato", "Kropsvægt (kg)"]], use_container_width=True)
        
        # Graf for kropsvægt
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(model.df_bodyweight["Dato"], model.df_bodyweight["Kropsvægt (kg)"], marker="s", color="#9C27B0")
        ax.set_ylabel("Kropsvægt (kg)")
        ax.grid(True, linestyle="--", alpha=0.6)
        st.pyplot(fig)
    else:
        st.info("Ingen kropsvægtmålinger fundet.")

# --- TRÆNINGSPROGRAM ---
elif menu == "📅 Træningsprogram":
    st.title("📅 Dit Træningsprogram")
    from workout_program import WORKOUT_PROGRAM
    
    for dag, info in WORKOUT_PROGRAM.items():
        with st.expander(f"{dag}: {info['title']} {info['extra']}" ):
            for ex, sets in info["exercises"]:
                st.write(f"- **{ex}**: {sets}")