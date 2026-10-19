import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from model.fitness_model import FitnessModel

# Sæt side-konfiguration
st.set_page_config(page_title="Styrketræning Tracker", page_icon="💪", layout="wide")

# Initialiser model (bruger din SQLite database)
@st.cache_resource
def get_model():
    model = FitnessModel("fitness.db")
    model.load_data()
    return model

model = get_model()
model.load_data() # Opdater data

# Sidebar navigation
st.sidebar.title("💪 Trænings-Tracker")
menu = st.sidebar.radio("Navigation", ["🏠 Forside", "➕ Tilføj nyt løft", "📈 Styrkeudvikling (Graf)", "📋 Træningsoversigt", "⚖️ Kropsvægt", "📅 Træningsprogram"])

# --- FORSIDE ---
if menu == "🏠 Forside":
    st.title("Velkommen til din Styrketræning Tracker")
    st.write("Brug menuen til venstre til at navigere mellem dine grafer, træningspas, tilføjelse af nye sæt og kropsvægt.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **Tip:** Denne web-app har nu de samme funktioner som din desktop-app!")
    with col2:
        st.success("🚀 **Database:** Forbundet til `fitness.db`.")

# --- TILFØJ NYT LØFT ---
elif menu == "➕ Tilføj nyt løft":
    st.title("➕ Tilføj et nyt træningssæt")
    
    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            val_dato = st.date_input("Dato", value=date.today())
            exercises_list = model.get_exercises()
            if not exercises_list:
                exercises_list = ["Bænkpres", "Squat", "Dødløft"]
            val_ovelse = st.selectbox("Øvelse", exercises_list)
        
        with col2:
            val_vaegt = st.number_input("Vægt (kg)", min_value=0.0, step=2.5, value=70.0)
            val_reps = st.number_input("Reps", min_value=1, step=1, value=5)
            
        submitted = st.form_submit_button("Gem træningssæt")
        if submitted:
            try:
                model.add_entry(val_dato.strftime("%Y-%m-%d"), val_ovelse, val_vaegt, val_reps)
                model.load_data()
                st.success(f"Tilføjet: {val_ovelse} ({val_vaegt} kg x {val_reps} reps) den {val_dato}!")
            except Exception as e:
                st.error(f"Kunne ikke gemme: {e}")

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
        st.subheader("Oversigt over træningspas")
        st.dataframe(sessions, use_container_width=True)
        
        st.divider()
        st.subheader("Detaljer for et valgt pas")
        selected_date = st.selectbox("Vælg dato for pas", sessions["Dato"].tolist())
        
        if selected_date:
            details = model.get_session_details(selected_date)
            st.write(f"Enkelte løft den {selected_date}:")
            st.dataframe(details, use_container_width=True)
            
            # Mulighed for at slette pas
            if st.button(f"Slet træningspas fra {selected_date}", type="primary"):
                model.delete_workout_session(selected_date)
                model.load_data()
                st.success(f"Træningspasset fra {selected_date} blev slettet!")
                st.rerun()
    else:
        st.info("Ingen træningspas registreret endnu.")

# --- KROPSVÆGT ---
elif menu == "⚖️ Kropsvægt":
    st.title("⚖️ Kropsvægt Log")
    
    with st.form("bw_form"):
        col1, col2 = st.columns(2)
        with col1:
            bw_date = st.date_input("Dato for måling", value=date.today())
        with col2:
            bw_weight = st.number_input("Kropsvægt (kg)", min_value=30.0, step=0.1, value=80.0)
        
        if st.form_submit_button("Gem kropsvægt"):
            try:
                model.add_bodyweight_entry(bw_date.strftime("%Y-%m-%d"), bw_weight)
                model.load_data()
                st.success("Kropsvægt gemt!")
            except Exception as e:
                st.error(f"Fejl: {e}")
                
    st.divider()
    if model.df_bodyweight is not None and not model.df_bodyweight.empty:
        st.dataframe(model.df_bodyweight[["Dato", "Kropsvægt (kg)"]], use_container_width=True)
        
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
    try:
        from workout_program import WORKOUT_PROGRAM
    except ImportError:
        WORKOUT_PROGRAM = {}
    
    if WORKOUT_PROGRAM:
        for dag, info in WORKOUT_PROGRAM.items():
            with st.expander(f"{dag}: {info['title']} {info['extra']}"):
                for ex, sets in info["exercises"]:
                    st.write(f"- **{ex}**: {sets}")
    else:
        st.info("Ingen træningsprogram fundet.")