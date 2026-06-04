import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

API_URL = 'http://localhost:8000'

st.set_page_config(
    page_title='Détection Alzheimer',
    page_icon='🧠',
    layout='wide'
)

st.title('Système de détection précoce — Alzheimer')
st.caption('Outil d aide au dépistage uniquement. Ne remplace pas un diagnostic clinique.')
st.markdown('---')

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header('Informations patient')
    age            = st.slider('Âge', 60, 90, 72)
    gender         = st.selectbox('Genre', [0, 1], format_func=lambda x: 'Femme' if x == 0 else 'Homme')
    ethnicity      = st.selectbox('Ethnicité', [0,1,2,3],
                        format_func=lambda x: ['Caucasien','Afro-Américain','Asiatique','Autre'][x])
    education      = st.selectbox('Niveau éducation', [0,1,2,3],
                        format_func=lambda x: ['Aucun','Lycée','Licence','Master+'][x])

    st.header('Antécédents médicaux')
    family_history = st.selectbox('Antécédents familiaux Alzheimer', [0,1], format_func=lambda x: 'Non' if x==0 else 'Oui')
    cardio         = st.selectbox('Maladie cardiovasculaire', [0,1], format_func=lambda x: 'Non' if x==0 else 'Oui')
    diabetes       = st.selectbox('Diabète', [0,1], format_func=lambda x: 'Non' if x==0 else 'Oui')
    depression     = st.selectbox('Dépression', [0,1], format_func=lambda x: 'Non' if x==0 else 'Oui')
    head_injury    = st.selectbox('Traumatisme crânien', [0,1], format_func=lambda x: 'Non' if x==0 else 'Oui')
    hypertension   = st.selectbox('Hypertension', [0,1], format_func=lambda x: 'Non' if x==0 else 'Oui')

    st.header('Scores cognitifs')
    mmse           = st.slider('MMSE (0-30)', 0.0, 30.0, 24.0)
    functional     = st.slider('Functional Assessment (0-10)', 0.0, 10.0, 7.0)
    adl            = st.slider('ADL (0-10)', 0.0, 10.0, 7.0)

    st.header('Symptômes')
    memory         = st.selectbox('Plaintes mémoire', [0,1], format_func=lambda x: 'Non' if x==0 else 'Oui')
    behavioral     = st.selectbox('Problèmes comportementaux', [0,1], format_func=lambda x: 'Non' if x==0 else 'Oui')
    confusion      = st.selectbox('Confusion', [0,1], format_func=lambda x: 'Non' if x==0 else 'Oui')
    disorientation = st.selectbox('Désorientation', [0,1], format_func=lambda x: 'Non' if x==0 else 'Oui')
    personality    = st.selectbox('Changements personnalité', [0,1], format_func=lambda x: 'Non' if x==0 else 'Oui')
    forgetfulness  = st.selectbox('Oublis fréquents', [0,1], format_func=lambda x: 'Non' if x==0 else 'Oui')

    st.header('Biologie & mode de vie')
    bmi            = st.slider('IMC', 15.0, 40.0, 25.0)
    systolic       = st.slider('Tension systolique', 90, 180, 120)
    diastolic      = st.slider('Tension diastolique', 60, 120, 80)
    chol_total     = st.slider('Cholestérol total', 150.0, 300.0, 200.0)
    chol_ldl       = st.slider('Cholestérol LDL', 50.0, 200.0, 100.0)
    chol_hdl       = st.slider('Cholestérol HDL', 20.0, 100.0, 50.0)
    chol_trig      = st.slider('Triglycérides', 50.0, 400.0, 150.0)
    smoking        = st.selectbox('Tabagisme', [0,1], format_func=lambda x: 'Non' if x==0 else 'Oui')
    alcohol        = st.slider('Consommation alcool', 0.0, 20.0, 5.0)
    physical       = st.slider('Activité physique', 0.0, 10.0, 5.0)
    diet           = st.slider('Qualité alimentation', 0.0, 10.0, 5.0)
    sleep          = st.slider('Qualité sommeil', 0.0, 10.0, 6.0)

    submitted = st.button('Analyser', type='primary', use_container_width=True)

# ── Résultats ─────────────────────────────────────────────────────────────────
if submitted:
    payload = {
        'Age': age, 'Gender': gender, 'Ethnicity': ethnicity,
        'EducationLevel': education, 'BMI': bmi,
        'Smoking': smoking, 'AlcoholConsumption': alcohol,
        'PhysicalActivity': physical, 'DietQuality': diet,
        'SleepQuality': sleep, 'FamilyHistoryAlzheimers': family_history,
        'CardiovascularDisease': cardio, 'Diabetes': diabetes,
        'Depression': depression, 'HeadInjury': head_injury,
        'Hypertension': hypertension, 'SystolicBP': systolic,
        'DiastolicBP': diastolic, 'CholesterolTotal': chol_total,
        'CholesterolLDL': chol_ldl, 'CholesterolHDL': chol_hdl,
        'CholesterolTriglycerides': chol_trig, 'MMSE': mmse,
        'FunctionalAssessment': functional, 'ADL': adl,
        'MemoryComplaints': memory, 'BehavioralProblems': behavioral,
        'Confusion': confusion, 'Disorientation': disorientation,
        'PersonalityChanges': personality, 'Forgetfulness': forgetfulness,
    }

    with st.spinner('Analyse en cours...'):
        try:
            resp   = requests.post(f'{API_URL}/predict', json=payload, timeout=30)
            result = resp.json()
        except Exception as e:
            st.error(f'Erreur API : {e}')
            st.stop()

    # Alerte
    if result['alert']:
        st.error('ALERTE : Risque élevé détecté. Consultation spécialisée recommandée.')
    elif result['risk_score'] > 0.3:
        st.warning('Risque modéré détecté. Suivi recommandé.')
    else:
        st.success('Risque faible détecté.')

    # Métriques
    col1, col2, col3 = st.columns(3)
    col1.metric('Score de risque', f"{result['risk_score']:.0%}")
    col2.metric('Prédiction', result['prediction'])
    col3.metric('Sévérité', result['severity'])

    col_gauge, col_shap = st.columns([1, 1])

    # Jauge
    with col_gauge:
        st.subheader('Score de risque')
        color = 'red' if result['alert'] else ('orange' if result['risk_score'] > 0.3 else 'green')
        fig = go.Figure(go.Indicator(
            mode='gauge+number',
            value=result['risk_score'] * 100,
            number={'suffix': '%', 'font': {'size': 40}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 30],  'color': '#E1F5EE'},
                    {'range': [30, 60], 'color': '#FAEEDA'},
                    {'range': [60, 100],'color': '#FCEBEB'},
                ],
                'threshold': {'line': {'color': 'red', 'width': 3}, 'value': 70}
            }
        ))
        fig.update_layout(height=280, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    # Facteurs SHAP
    with col_shap:
        st.subheader('Facteurs déterminants')
        df_f = pd.DataFrame(result['top_factors'])
        df_f['couleur'] = df_f['impact'].apply(lambda x: 'red' if x > 0 else 'green')
        fig2 = go.Figure(go.Bar(
            x=df_f['impact'], y=df_f['feature'],
            orientation='h',
            marker_color=df_f['couleur']
        ))
        fig2.update_layout(height=280, margin=dict(t=20, b=20),
                           xaxis_title='Impact (SHAP)', yaxis_title='')
        st.plotly_chart(fig2, use_container_width=True)

    st.caption('Rouge = facteur augmentant le risque | Vert = facteur protecteur')



#  Historique

st.markdown('---')
st.subheader('Historique des consultations')

if 'history' not in st.session_state:
    st.session_state.history = []

if submitted and 'result' in dir():
    st.session_state.history.append({
        'Consultation': len(st.session_state.history) + 1,
        'Score (%)': round(result['risk_score'] * 100, 1),
        'Prédiction': result['prediction'],
        'Sévérité': result['severity']
    })

if st.session_state.history:
    df_hist = pd.DataFrame(st.session_state.history)

    # Graphique évolution
    colors = ['red' if s > 70 else 'orange' if s > 30 else 'green'
              for s in df_hist['Score (%)']]
    fig_hist = go.Figure(go.Scatter(
        x=df_hist['Consultation'],
        y=df_hist['Score (%)'],
        mode='lines+markers',
        marker=dict(color=colors, size=10),
        line=dict(color='gray', width=1)
    ))
    fig_hist.add_hline(y=70, line_dash='dash', line_color='red',
                       annotation_text='Seuil alerte (70%)')
    fig_hist.add_hline(y=30, line_dash='dash', line_color='orange',
                       annotation_text='Seuil modéré (30%)')
    fig_hist.update_layout(
        title="Évolution du score de risque",
        xaxis_title='Consultation',
        yaxis_title='Score de risque (%)',
        yaxis=dict(range=[0, 100]),
        height=350
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # Tableau historique
    st.dataframe(df_hist, use_container_width=True)

    if st.button('Réinitialiser historique'):
        st.session_state.history = []
        st.rerun()
else:
    st.info('Aucune consultation enregistrée. Lance une analyse pour commencer le suivi.')