"""
Breast Cancer Global Statistics Dashboard (2003-2023) / Tableau de Bord (2003-2023)
Bilingual Interactive Dashboard - English & French / Tableau de Bord Bilingue - Anglais & Français
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Breast Cancer Statistics / Statistiques Cancer du Sein",
    page_icon="🎗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Translation dictionary / Dictionnaire de traductions
TRANSLATIONS = {
    'en': {
        # Header
        'main_title': 'Pink Board : 🎗️ Breast Cancer Global Statistics Dashboard',
        'subtitle': 'Raising Awareness Through Data | October Breast Cancer Awareness Month',
        
        # Sidebar
        'filters_title': '🔍 Filters & Settings',
        'language': 'Language',
        'select_country': 'Select Country',
        'select_year': 'Select Year',
        'show_comparison': 'Show Global Comparison',
        'show_trends': 'Show Historical Trends',
        'show_recommendations': 'Show Recommendations',
        
        # Main metrics
        'statistics_title': 'Breast Cancer Statistics',
        'incidence_rate': 'Incidence Rate (ASR)',
        'mortality_rate': 'Mortality Rate (ASR)',
        'new_cases': 'New Cases',
        'deaths': 'Deaths',
        'incidence_help': 'Age-Standardized Rate per 100,000 population',
        'mortality_help': 'Age-Standardized Mortality Rate per 100,000',
        'cases_help': 'Total new breast cancer cases diagnosed',
        'deaths_help': 'Total deaths from breast cancer',
        
        # Key indicators
        'key_indicators': '🔑 Key Health Indicators',
        'screening_coverage': 'Screening Coverage',
        'early_detection': 'Early Detection Rate',
        'treatment_coverage': 'Treatment Coverage',
        'survival_rate': '5-Year Survival Rate',
        'vs_target': 'vs target',
        
        # MI Ratio
        'mi_ratio': 'Mortality-to-Incidence (MI) Ratio',
        'mi_help': 'Lower is better. Indicates healthcare system effectiveness',
        'status': 'Status',
        'target': 'Target',
        'good': '🟢 Good',
        'moderate': '🟡 Moderate',
        'high': '🔴 High',
        
        # Descriptive stats
        'desc_stats': '📈 Descriptive Statistics',
        'country_profile': '👥 Country Profile',
        'region': 'Region',
        'hdi_category': 'HDI Category',
        'population': 'Population',
        'millions': 'millions',
        'calculated_metrics': '🔢 Calculated Metrics',
        'case_fatality': 'Case Fatality Rate',
        'cases_per_million': 'Cases per Million',
        'deaths_per_million': 'Deaths per Million',
        
        # Visual indicators
        'visual_indicators': '📊 Visual Indicators',
        'screening': 'Screening',
        'detection': 'Detection',
        'treatment': 'Treatment',
        'survival': 'Survival',
        
        # Trends
        'historical_trends': '📈 Historical Trends',
        'incidence_mortality': 'Incidence & Mortality',
        'year': 'Year',
        'rate_per_100k': 'Rate per 100,000',
        'coverage_pct': 'Coverage (%)',
        'survival_pct': 'Survival Rate (%)',
        'mi_ratio_pct': 'MI Ratio (%)',
        'trend_title': 'Indicator Evolution',
        'objective': 'Target',
        'critical_threshold': 'Critical Threshold',
        
        # Changes
        'survival_change': 'Survival Change',
        'screening_change': 'Screening Change',
        'incidence_change': 'Incidence Change',
        'mi_change': 'MI Ratio Change',
        'change_from': 'Change from',
        'to': 'to',
        
        # Comparison
        'global_comparison': '🌍 Global Comparison',
        'key_metrics_vs_global': 'Key Metrics vs Global Average',
        'global_average': 'Global Average',
        'percentage': 'Percentage (%)',
        'hdi_comparison': '📊 Comparison by HDI Category',
        'health_metrics_hdi': 'Healthcare Metrics by HDI Category',
        'country_ranking': 'Where does',
        'rank': 'rank?',
        'survival_rank': 'Survival Rate Rank',
        'screening_rank': 'Screening Coverage Rank',
        'survival_percentile': 'Survival Percentile',
        
        # Recommendations
        'insights_recommendations': '💡 Key Insights & Recommendations',
        'positive_aspects': '✅ Positive Aspects',
        'areas_attention': '⚠️ Areas Requiring Attention',
        'actionable_recommendations': '🎯 Actionable Recommendations',
        'general_recommendations': 'General Recommendations for Improvement:',
        
        # Concerns
        'low_screening': 'Low Screening Coverage',
        'below_target': 'Significantly below the recommended 70% target',
        'low_detection': 'Low Early Detection',
        'advanced_stages': 'Majority of cases detected at advanced stages',
        'low_survival': 'Low Survival Rate',
        'below_average': 'Below global average, indicating treatment gaps',
        'high_mi': 'High MI Ratio',
        'late_detection': 'Indicates late detection and/or inadequate treatment',
        'inadequate_treatment': 'Inadequate Treatment Coverage',
        'not_receiving': 'Many diagnosed patients not receiving treatment',
        
        # Successes
        'good_screening': 'Good Screening Coverage',
        'meets_targets': 'Meets or exceeds recommended targets',
        'strong_detection': 'Strong Early Detection',
        'effective_programs': 'Effective early detection programs in place',
        'high_survival': 'High Survival Rate',
        'excellent_outcomes': 'Excellent treatment outcomes',
        'low_mi': 'Low MI Ratio',
        'effective_response': 'Effective healthcare system response',
        
        # Actions
        'increase_screening': '📍 Increase Screening Programs',
        'mobile_units': 'Implement mobile screening units in rural areas and provide free mammography services',
        'enhance_detection': '📍 Enhance Early Detection',
        'awareness_campaigns': 'Launch awareness campaigns about breast self-examination and clinical breast exams',
        'improve_treatment': '📍 Improve Treatment Access',
        'strengthen_infrastructure': 'Strengthen healthcare infrastructure and ensure availability of cancer drugs',
        'reduce_mi': '📍 Reduce MI Ratio',
        'focus_quality': 'Focus on both early detection and treatment quality improvements',
        'expand_treatment': '📍 Expand Treatment Access',
        'increase_centers': 'Increase oncology centers and train more healthcare professionals',
        
        # General recommendations
        'rec_1': '1. Public Awareness: Conduct regular breast cancer awareness campaigns, especially during October',
        'rec_2': '2. Education: Educate women about breast self-examination and early warning signs',
        'rec_3': '3. Healthcare Infrastructure: Invest in diagnostic equipment and treatment facilities',
        'rec_4': '4. Training: Train healthcare workers in breast cancer detection and treatment',
        'rec_5': '5. Policy: Implement national breast cancer screening guidelines and programs',
        'rec_6': '6. Support Groups: Establish patient support networks for emotional and practical assistance',
        'rec_7': '7. Research: Support local research on breast cancer patterns and effective interventions',
        'rec_8': '8. Affordability: Make screening and treatment financially accessible to all women',
        
        # Understanding data
        'understanding_data': '📖 Understanding the Data',
        'what_metrics_mean': '📊 What do these metrics mean?',
        'how_interpret': '🔍 How to interpret these findings?',
        
        # Metric definitions
        'def_incidence': 'Incidence Rate (ASR): Number of new breast cancer cases per 100,000 women, adjusted for age differences',
        'def_mortality': 'Mortality Rate (ASR): Number of deaths from breast cancer per 100,000 women, adjusted for age differences',
        'def_mi_ratio': 'MI Ratio: Mortality-to-Incidence ratio. Lower is better. High ratio suggests late detection or treatment gaps.',
        'mi_excellent': '< 30%: Excellent healthcare response',
        'mi_moderate': '30-50%: Moderate, room for improvement',
        'mi_concerning': '> 50%: Concerning, indicates significant healthcare challenges',
        'def_screening': 'Screening Coverage: Percentage of target population receiving regular breast cancer screening',
        'def_detection': 'Early Detection Rate: Percentage of cases detected at early stages (Stage I-II)',
        'def_treatment': 'Treatment Coverage: Percentage of diagnosed patients receiving appropriate treatment',
        'def_survival': '5-Year Survival Rate: Percentage of patients alive 5 years after diagnosis',
        
        # Interpretation
        'low_resource': 'For Low-Resource Settings:',
        'low_resource_1': '- Focus on improving screening coverage as a priority',
        'low_resource_2': '- Invest in early detection programs (most cost-effective)',
        'low_resource_3': '- Ensure basic treatment availability before advanced therapies',
        'medium_resource': 'For Medium-Resource Settings:',
        'medium_resource_1': '- Maintain and expand screening programs',
        'medium_resource_2': '- Focus on treatment quality and consistency',
        'medium_resource_3': '- Reduce disparities between urban and rural areas',
        'high_resource': 'For High-Resource Settings:',
        'high_resource_1': '- Optimize screening protocols (avoid over-screening)',
        'high_resource_2': '- Focus on personalized medicine and advanced treatments',
        'high_resource_3': '- Address health equity gaps',
        'red_flags': 'Red Flags:',
        'red_flag_1': '- MI Ratio > 50%: Urgent need for healthcare system improvements',
        'red_flag_2': '- Screening < 30%: Critical shortage of screening services',
        'red_flag_3': '- Survival < 40%: Systemic healthcare challenges',
        
        # Footer
        'footer_awareness': '🎗️ Breast Cancer Awareness Month - October 2025',
        'footer_detection': 'Early detection saves lives. Regular screening is crucial.',
        'footer_source': 'Data Source: Global Breast Cancer Statistics (2003-2023)',
        'footer_source1': '[NB: Some of the data were generated for analysis purposes.]',
        'footer_purpose': 'Created for awareness and education purposes | GitHub Repository',
        'footer_author': 'Author : Consolas HODONOU | Data Scientist| E-mail : nevinashodonou@gmail.com',
        
        # Sidebar info
        'about_dashboard': 'About This Dashboard',
        'about_text': 'This interactive dashboard provides comprehensive breast cancer statistics from 2003-2023 for 90 countries worldwide.',
        'how_use': 'How to Use:',
        'how_use_1': '1. Select a country from the dropdown',
        'how_use_2': '2. Choose a year to analyze',
        'how_use_3': '3. Toggle comparison and trend views',
        'how_use_4': '4. Review recommendations',
        'purpose': 'Purpose:',
        'purpose_text': 'Raise awareness about breast cancer and help inform evidence-based interventions.',
        'october_awareness': 'October is Breast Cancer Awareness Month 🎗️',
        'early_detection': '💪 Early detection saves lives!',
        
        # Error
        'no_data': 'No data available for',
        'in': 'in',
    },
    
    'fr': {
        # Header
        'main_title': 'Pink Board : 🎗️ Tableau de Bord des Statistiques Mondiales sur le Cancer du Sein',
        'subtitle': 'Sensibilisation par les Données | Octobre - Mois de Sensibilisation au Cancer du Sein',
        
        # Sidebar
        'filters_title': '🔍 Filtres & Paramètres',
        'language': 'Langue',
        'select_country': 'Sélectionner un Pays',
        'select_year': 'Sélectionner une Année',
        'show_comparison': 'Afficher la Comparaison Mondiale',
        'show_trends': 'Afficher les Tendances Historiques',
        'show_recommendations': 'Afficher les Recommandations',
        
        # Main metrics
        'statistics_title': 'Statistiques du Cancer du Sein',
        'incidence_rate': 'Taux d\'Incidence (TSA)',
        'mortality_rate': 'Taux de Mortalité (TSA)',
        'new_cases': 'Nouveaux Cas',
        'deaths': 'Décès',
        'incidence_help': 'Taux Standardisé par Âge pour 100 000 habitants',
        'mortality_help': 'Taux de Mortalité Standardisé par Âge pour 100 000 habitants',
        'cases_help': 'Total des nouveaux cas de cancer du sein diagnostiqués',
        'deaths_help': 'Total des décès dus au cancer du sein',
        
        # Key indicators
        'key_indicators': '🔑 Indicateurs Clés de Santé',
        'screening_coverage': 'Couverture du Dépistage',
        'early_detection': 'Taux de Détection Précoce',
        'treatment_coverage': 'Couverture du Traitement',
        'survival_rate': 'Taux de Survie à 5 Ans',
        'vs_target': 'vs objectif',
        
        # MI Ratio
        'mi_ratio': 'Ratio Mortalité-Incidence (MI)',
        'mi_help': 'Plus bas est meilleur. Indique l\'efficacité du système de santé',
        'status': 'Statut',
        'target': 'Objectif',
        'good': '🟢 Bon',
        'moderate': '🟡 Modéré',
        'high': '🔴 Élevé',
        
        # Descriptive stats
        'desc_stats': '📈 Statistiques Descriptives',
        'country_profile': '👥 Profil du Pays',
        'region': 'Région',
        'hdi_category': 'Catégorie IDH',
        'population': 'Population',
        'millions': 'millions',
        'calculated_metrics': '🔢 Métriques Calculées',
        'case_fatality': 'Taux de Létalité',
        'cases_per_million': 'Cas par Million',
        'deaths_per_million': 'Décès par Million',
        
        # Visual indicators
        'visual_indicators': '📊 Indicateurs Visuels',
        'screening': 'Dépistage',
        'detection': 'Détection',
        'treatment': 'Traitement',
        'survival': 'Survie',
        
        # Trends
        'historical_trends': '📈 Tendances Historiques',
        'incidence_mortality': 'Incidence & Mortalité',
        'year': 'Année',
        'rate_per_100k': 'Taux pour 100 000',
        'coverage_pct': 'Couverture (%)',
        'survival_pct': 'Taux de Survie (%)',
        'mi_ratio_pct': 'Ratio MI (%)',
        'trend_title': 'Évolution des Indicateurs',
        'objective': 'Objectif',
        'critical_threshold': 'Seuil Critique',
        
        # Changes
        'survival_change': 'Changement de Survie',
        'screening_change': 'Changement de Dépistage',
        'incidence_change': 'Changement d\'Incidence',
        'mi_change': 'Changement du Ratio MI',
        'change_from': 'Changement de',
        'to': 'à',
        
        # Comparison
        'global_comparison': '🌍 Comparaison Mondiale',
        'key_metrics_vs_global': 'Indicateurs Clés vs Moyenne Mondiale',
        'global_average': 'Moyenne Mondiale',
        'percentage': 'Pourcentage (%)',
        'hdi_comparison': '📊 Comparaison par Catégorie de l\'IDH',
        'health_metrics_hdi': 'Indicateurs de Santé par Catégorie IDH',
        'country_ranking': 'Où se classe',
        'rank': '?',
        'survival_rank': 'Classement Taux de Survie',
        'screening_rank': 'Classement Couverture Dépistage',
        'survival_percentile': 'Percentile de Survie',
        
        # Recommendations
        'insights_recommendations': '💡 Principales Observations & Recommandations',
        'positive_aspects': '✅ Aspects Positifs',
        'areas_attention': '⚠️ Domaines Nécessitant une Attention',
        'actionable_recommendations': '🎯 Recommandations Concrètes',
        'general_recommendations': 'Recommandations Générales pour l\'Amélioration :',
        
        # Concerns
        'low_screening': 'Faible Couverture du Dépistage',
        'below_target': 'Significativement en dessous de l\'objectif recommandé de 70%',
        'low_detection': 'Faible Détection Précoce',
        'advanced_stages': 'La majorité des cas détectés à des stades avancés',
        'low_survival': 'Faible Taux de Survie',
        'below_average': 'En dessous de la moyenne mondiale, indiquant des lacunes dans le traitement',
        'high_mi': 'Ratio MI Élevé',
        'late_detection': 'Indique une détection tardive et/ou un traitement inadéquat',
        'inadequate_treatment': 'Couverture de Traitement Inadéquate',
        'not_receiving': 'De nombreux patients diagnostiqués ne reçoivent pas de traitement',
        
        # Successes
        'good_screening': 'Bonne Couverture du Dépistage',
        'meets_targets': 'Atteint ou dépasse les objectifs recommandés',
        'strong_detection': 'Détection Précoce Efficace',
        'effective_programs': 'Programmes de détection précoce performants en place',
        'high_survival': 'Taux de Survie Élevé',
        'excellent_outcomes': 'Excellents résultats de traitement',
        'low_mi': 'Ratio MI Faible',
        'effective_response': 'Réponse efficace du système de santé',
        
        # Actions
        'increase_screening': '📍 Augmenter les Programmes de Dépistage',
        'mobile_units': 'Mettre en place des unités mobiles de dépistage dans les zones rurales et offrir des mammographies gratuites',
        'enhance_detection': '📍 Améliorer la Détection Précoce',
        'awareness_campaigns': 'Lancer des campagnes de sensibilisation sur l\'autopalpation mammaire et les examens cliniques',
        'improve_treatment': '📍 Améliorer l\'Accès aux Traitements',
        'strengthen_infrastructure': 'Renforcer les infrastructures de santé et assurer la disponibilité des médicaments anticancéreux',
        'reduce_mi': '📍 Réduire le Ratio MI',
        'focus_quality': 'Se concentrer sur l\'amélioration de la détection précoce et de la qualité des traitements',
        'expand_treatment': '📍 Élargir l\'Accès aux Traitements',
        'increase_centers': 'Augmenter les centres d\'oncologie et former davantage de professionnels de santé',
        
        # General recommendations
        'rec_1': '1. Sensibilisation Publique : Mener régulièrement des campagnes de sensibilisation au cancer du sein, en particulier en octobre',
        'rec_2': '2. Éducation : Éduquer les femmes sur l\'autopalpation mammaire et les signes d\'alerte précoces',
        'rec_3': '3. Infrastructure de Santé : Investir dans les équipements de diagnostic et les installations de traitement',
        'rec_4': '4. Formation : Former les professionnels de santé à la détection et au traitement du cancer du sein',
        'rec_5': '5. Politique : Mettre en œuvre des directives et programmes nationaux de dépistage du cancer du sein',
        'rec_6': '6. Groupes de Soutien : Établir des réseaux de soutien aux patients pour l\'assistance émotionnelle et pratique',
        'rec_7': '7. Recherche : Soutenir la recherche locale sur les tendances du cancer du sein et les interventions efficaces',
        'rec_8': '8. Accessibilité Financière : Rendre le dépistage et le traitement financièrement accessibles à toutes les femmes',
        
        # Understanding data
        'understanding_data': '📖 Comprendre les Données',
        'what_metrics_mean': '📊 Que signifient ces indicateurs ?',
        'how_interpret': '🔍 Comment interpréter ces résultats ?',
        
        # Metric definitions
        'def_incidence': 'Taux d\'Incidence (TSA) : Nombre de nouveaux cas de cancer du sein pour 100 000 femmes, ajusté pour les différences d\'âge',
        'def_mortality': 'Taux de Mortalité (TSA) : Nombre de décès dus au cancer du sein pour 100 000 femmes, ajusté pour les différences d\'âge',
        'def_mi_ratio': 'Ratio MI : Ratio Mortalité-Incidence. Plus bas est meilleur. Un ratio élevé suggère une détection tardive ou des lacunes dans le traitement.',
        'mi_excellent': '< 30% : Excellente réponse du système de santé',
        'mi_moderate': '30-50% : Modéré, possibilité d\'amélioration',
        'mi_concerning': '> 50% : Préoccupant, indique des défis importants dans le système de santé',
        'def_screening': 'Couverture du Dépistage : Pourcentage de la population cible recevant un dépistage régulier du cancer du sein',
        'def_detection': 'Taux de Détection Précoce : Pourcentage de cas détectés aux stades précoces (Stade I-II)',
        'def_treatment': 'Couverture du Traitement : Pourcentage de patients diagnostiqués recevant un traitement approprié',
        'def_survival': 'Taux de Survie à 5 Ans : Pourcentage de patients vivants 5 ans après le diagnostic',
        
        # Interpretation
        'low_resource': 'Pour les Contextes à Faibles Ressources :',
        'low_resource_1': '- Se concentrer sur l\'amélioration de la couverture du dépistage comme priorité',
        'low_resource_2': '- Investir dans les programmes de détection précoce (le plus rentable)',
        'low_resource_3': '- Assurer la disponibilité des traitements de base avant les thérapies avancées',
        'medium_resource': 'Pour les Contextes à Ressources Moyennes :',
        'medium_resource_1': '- Maintenir et élargir les programmes de dépistage',
        'medium_resource_2': '- Se concentrer sur la qualité et la cohérence des traitements',
        'medium_resource_3': '- Réduire les disparités entre zones urbaines et rurales',
        'high_resource': 'Pour les Contextes à Ressources Élevées :',
        'high_resource_1': '- Optimiser les protocoles de dépistage (éviter le sur-dépistage)',
        'high_resource_2': '- Se concentrer sur la médecine personnalisée et les traitements avancés',
        'high_resource_3': '- Aborder les écarts d\'équité en santé',
        'red_flags': 'Signaux d\'Alarme :',
        'red_flag_1': '- Ratio MI > 50% : Besoin urgent d\'amélioration du système de santé',
        'red_flag_2': '- Dépistage < 30% : Pénurie critique des services de dépistage',
        'red_flag_3': '- Survie < 40% : Défis systémiques dans le système de santé',
        
        # Footer
        'footer_awareness': '🎗️ Mois de Sensibilisation au Cancer du Sein - Octobre 2025',
        'footer_detection': 'La détection précoce sauve des vies. Le dépistage régulier est crucial.',
        'footer_source': 'Source des Données : Statistiques Mondiales du Cancer du Sein (2003-2023)', 
        'footer_source1': '[NB: Une partie des données a été générée dans un but analytique.]',
        'footer_purpose': 'Créé à des fins de sensibilisation et d\'éducation | Dépôt GitHub',
        'footer_author': 'Auteure : Consolas HODONOU | Data Scientist| E-mail : nevinashodonou@gmail.com',
        
        # Sidebar info
        'about_dashboard': 'À Propos de ce Tableau de Bord',
        'about_text': 'Ce tableau de bord interactif fournit des statistiques complètes sur le cancer du sein de 2003 à 2023 pour 90 pays dans le monde.',
        'how_use': 'Comment Utiliser :',
        'how_use_1': '1. Sélectionnez un pays dans la liste déroulante',
        'how_use_2': '2. Choisissez une année à analyser',
        'how_use_3': '3. Activez/désactivez les vues de comparaison et de tendances',
        'how_use_4': '4. Consultez les recommandations',
        'purpose': 'Objectif :',
        'purpose_text': 'Sensibiliser au cancer du sein et contribuer à éclairer les interventions fondées sur des preuves.',
        'october_awareness': 'Octobre est le Mois de Sensibilisation au Cancer du Sein 🎗️',
        'early_detection': '💪 La détection précoce sauve des vies !',
        
        # Error
        'no_data': 'Aucune donnée disponible pour',
        'in': 'en',
    }
}

# Helper function to get translated text
def t(key, lang='en'):
    """Get translated text for given key and language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

# Custom CSS
st.markdown("""
<style> 
    html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
    }   
    .main-header {
        font-size: 3rem;
        color: #FF1493;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #FF69B4 0%, #FF1493 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #ffc107;
        margin: 1rem 0;
    }
    .insight-box {
        background-color: #fff3f8;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #FF69B4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("breast_cancer_global_data_2003_2023.csv")
    return df

df = load_data()

# Sidebar - Language Selection (at the top)
st.sidebar.image("rose1.jpeg", width=175)

# Language selector
lang = st.sidebar.selectbox(
    "🌐 Language / Langue",
    options=['en', 'fr'],
    format_func=lambda x: "🇬🇧 English" if x == 'en' else "🇫🇷 Français",
    index=0
)

st.sidebar.title(t('filters_title', lang))

# Country and year selection
countries = sorted(df['Country'].unique())
default_country = 'Benin' if 'Benin' in countries else countries[0]
selected_country = st.sidebar.selectbox(t('select_country', lang), countries, index=countries.index(default_country))

years = sorted(df['Year'].unique())
selected_year = st.sidebar.selectbox(t('select_year', lang), years, index=len(years)-1)

# Filter data
country_data = df[df['Country'] == selected_country].sort_values('Year')
year_data = df[df['Year'] == selected_year]
selected_data = df[(df['Country'] == selected_country) & (df['Year'] == selected_year)]

# Additional filters
st.sidebar.markdown("---")
show_comparison = st.sidebar.checkbox(t('show_comparison', lang), value=True)
show_trends = st.sidebar.checkbox(t('show_trends', lang), value=True)
show_recommendations = st.sidebar.checkbox(t('show_recommendations', lang), value=True)

# Header
st.markdown(f'<h1 class="main-header">{t("main_title", lang)}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">{t("subtitle", lang)}</p>', unsafe_allow_html=True)

# Main content
if len(selected_data) > 0:
    data = selected_data.iloc[0]
    
    # Overview Section
    st.header(f"📊 {selected_country} - {t('statistics_title', lang)} ({selected_year})")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            t('incidence_rate', lang),
            f"{data['Incidence_Rate_ASR']:.1f}",
            help=t('incidence_help', lang)
        )
    
    with col2:
        st.metric(
            t('mortality_rate', lang),
            f"{data['Mortality_Rate_ASR']:.1f}",
            help=t('mortality_help', lang)
        )
    
    with col3:
        st.metric(
            t('new_cases', lang),
            f"{int(data['New_Cases']):,}",
            help=t('cases_help', lang)
        )
    
    with col4:
        st.metric(
            t('deaths', lang),
            f"{int(data['Deaths']):,}",
            help=t('deaths_help', lang)
        )
    
    st.markdown("---")
    
    # Key Indicators
    st.subheader(t('key_indicators', lang))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        screening_color = "normal" if data['Screening_Coverage_%'] >= 70 else "inverse"
        st.metric(
            t('screening_coverage', lang),
            f"{data['Screening_Coverage_%']:.1f}%",
            delta=f"{data['Screening_Coverage_%'] - 70:.1f}% {t('vs_target', lang)} (70%)",
            delta_color=screening_color
        )
    
    with col2:
        detection_color = "normal" if data['Early_Detection_Rate_%'] >= 60 else "inverse"
        st.metric(
            t('early_detection', lang),
            f"{data['Early_Detection_Rate_%']:.1f}%",
            delta=f"{data['Early_Detection_Rate_%'] - 60:.1f}% {t('vs_target', lang)} (60%)",
            delta_color=detection_color
        )
    
    with col3:
        treatment_color = "normal" if data['Treatment_Coverage_%'] >= 90 else "inverse"
        st.metric(
            t('treatment_coverage', lang),
            f"{data['Treatment_Coverage_%']:.1f}%",
            delta=f"{data['Treatment_Coverage_%'] - 90:.1f}% {t('vs_target', lang)} (90%)",
            delta_color=treatment_color
        )
    
    with col4:
        survival_color = "normal" if data['Five_Year_Survival_%'] >= 70 else "inverse"
        st.metric(
            t('survival_rate', lang),
            f"{data['Five_Year_Survival_%']:.1f}%",
            delta=f"{data['Five_Year_Survival_%'] - 70:.1f}% {t('vs_target', lang)} (70%)",
            delta_color=survival_color
        )
    
    # MI Ratio
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        mi_status = t('good', lang) if data['MI_Ratio'] < 30 else t('moderate', lang) if data['MI_Ratio'] < 50 else t('high', lang)
        st.metric(
            t('mi_ratio', lang),
            f"{data['MI_Ratio']:.1f}%",
            help=t('mi_help', lang)
        )
        st.caption(f"{t('status', lang)}: {mi_status} | {t('target', lang)}: < 30%")
    
    # Descriptive Statistics
    st.markdown("---")
    st.subheader(t('desc_stats', lang))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{t('country_profile', lang)}**")
        st.write(f"**{t('region', lang)}:** {data['Region']}")
        st.write(f"**{t('hdi_category', lang)}:** {data['HDI_Category']}")
        st.write(f"**{t('population', lang)}:** {data['Population_Millions']:.2f} {t('millions', lang)}")
    
    with col2:
        st.markdown(f"**{t('calculated_metrics', lang)}**")
        case_fatality = (data['Deaths'] / data['New_Cases'] * 100) if data['New_Cases'] > 0 else 0
        cases_per_million = (data['New_Cases'] / data['Population_Millions'])
        deaths_per_million = (data['Deaths'] / data['Population_Millions'])
        
        st.write(f"**{t('case_fatality', lang)}:** {case_fatality:.1f}%")
        st.write(f"**{t('cases_per_million', lang)}:** {cases_per_million:.1f}")
        st.write(f"**{t('deaths_per_million', lang)}:** {deaths_per_million:.1f}")
    
    # Visual Indicators (Gauges)
    st.markdown("---")
    st.subheader(t('visual_indicators', lang))
    
    fig = make_subplots(
        rows=1, cols=4,
        subplot_titles=(t('screening', lang), t('detection', lang), t('treatment', lang), t('survival', lang)),
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}, 
               {'type': 'indicator'}, {'type': 'indicator'}]]
    )
    
    # Screening
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=data['Screening_Coverage_%'],
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#4169E1"},
            'steps': [
                {'range': [0, 70], 'color': "lightgray"},
                {'range': [70, 100], 'color': "lightgreen"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 70}
        }
    ), row=1, col=1)
    
    # Detection
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=data['Early_Detection_Rate_%'],
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#32CD32"},
            'steps': [
                {'range': [0, 60], 'color': "lightgray"},
                {'range': [60, 100], 'color': "lightgreen"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 60}
        }
    ), row=1, col=2)
    
    # Treatment
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=data['Treatment_Coverage_%'],
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#FF8C00"},
            'steps': [
                {'range': [0, 90], 'color': "lightgray"},
                {'range': [90, 100], 'color': "lightgreen"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}
        }
    ), row=1, col=3)
    
    # Survival
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=data['Five_Year_Survival_%'],
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#FF1493"},
            'steps': [
                {'range': [0, 70], 'color': "lightgray"},
                {'range': [70, 100], 'color': "lightgreen"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 70}
        }
    ), row=1, col=4)
    
    fig.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Historical Trends
    if show_trends and len(country_data) > 1:
        st.markdown("---")
        st.subheader(f"{t('historical_trends', lang)} - {selected_country} (2003-2023)")
        
        fig_trends = make_subplots(
            rows=2, cols=2,
            subplot_titles=(t('incidence_mortality', lang), t('screening_coverage', lang), 
                          t('survival_rate', lang), t('mi_ratio', lang)),
            vertical_spacing=0.2,
            horizontal_spacing=0.1
        )
        
        # Incidence & Mortality
        fig_trends.add_trace(go.Scatter(
            x=country_data['Year'], y=country_data['Incidence_Rate_ASR'],
            name=t('incidence_rate', lang), line=dict(color='#FF1493', width=2),
            mode='lines+markers'
        ), row=1, col=1)
        
        fig_trends.add_trace(go.Scatter(
            x=country_data['Year'], y=country_data['Mortality_Rate_ASR'],
            name=t('mortality_rate', lang), line=dict(color='#DC143C', width=2),
            mode='lines+markers'
        ), row=1, col=1)
        
        # Screening
        fig_trends.add_trace(go.Scatter(
            x=country_data['Year'], y=country_data['Screening_Coverage_%'],
            name=t('screening', lang), line=dict(color='#4169E1', width=3),
            fill='tozeroy', mode='lines+markers'
        ), row=1, col=2)
        fig_trends.add_hline(y=70, line_dash="dash", line_color="green", 
                            annotation_text=t('objective', lang), row=1, col=2)
        
        # Survival
        fig_trends.add_trace(go.Scatter(
            x=country_data['Year'], y=country_data['Five_Year_Survival_%'],
            name=t('survival', lang), line=dict(color='#FF69B4', width=3),
            fill='tozeroy', mode='lines+markers'
        ), row=2, col=1)
        fig_trends.add_hline(y=70, line_dash="dash", line_color="green", 
                            annotation_text=t('objective', lang), row=2, col=1)
        
        # MI Ratio
        fig_trends.add_trace(go.Scatter(
            x=country_data['Year'], y=country_data['MI_Ratio'],
            name=t('mi_ratio', lang), line=dict(color='#FFB6C1', width=3),
            fill='tozeroy', mode='lines+markers'
        ), row=2, col=2)
        fig_trends.add_hline(y=30, line_dash="dash", line_color="green", 
                            annotation_text=t('objective', lang), row=2, col=2)
        fig_trends.add_hline(y=50, line_dash="dash", line_color="orange", 
                            annotation_text=t('critical_threshold', lang), row=2, col=2)
        
        fig_trends.update_xaxes(title_text=t('year', lang))
        fig_trends.update_yaxes(title_text=t('rate_per_100k', lang), row=1, col=1)
        fig_trends.update_yaxes(title_text=t('coverage_pct', lang), row=1, col=2)
        fig_trends.update_yaxes(title_text=t('survival_pct', lang), row=2, col=1)
        fig_trends.update_yaxes(title_text=t('mi_ratio_pct', lang), row=2, col=2)
        
        fig_trends.update_layout(height=600, showlegend=True, title_text=f"{t('trend_title', lang)} - {selected_country}")
        st.plotly_chart(fig_trends, use_container_width=True)
        
        # Changes
        if len(country_data) >= 2:
            first_year = country_data.iloc[0]
            last_year = country_data.iloc[-1]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                survival_change = last_year['Five_Year_Survival_%'] - first_year['Five_Year_Survival_%']
                st.metric(t('survival_change', lang), f"{survival_change:+.1f}%",
                         help=f"{t('change_from', lang)} {int(first_year['Year'])} {t('to', lang)} {int(last_year['Year'])}")
            
            with col2:
                screening_change = last_year['Screening_Coverage_%'] - first_year['Screening_Coverage_%']
                st.metric(t('screening_change', lang), f"{screening_change:+.1f}%",
                         help=f"{t('change_from', lang)} {int(first_year['Year'])} {t('to', lang)} {int(last_year['Year'])}")
            
            with col3:
                incidence_change = last_year['Incidence_Rate_ASR'] - first_year['Incidence_Rate_ASR']
                st.metric(t('incidence_change', lang), f"{incidence_change:+.1f}",
                         help=f"{t('change_from', lang)} {int(first_year['Year'])} {t('to', lang)} {int(last_year['Year'])}")
            
            with col4:
                mi_change = last_year['MI_Ratio'] - first_year['MI_Ratio']
                st.metric(t('mi_change', lang), f"{mi_change:+.1f}%",
                         help=f"{t('change_from', lang)} {int(first_year['Year'])} {t('to', lang)} {int(last_year['Year'])}")
    
    # Global Comparison
    if show_comparison:
        st.markdown("---")
        st.subheader(f"{t('global_comparison', lang)} - {selected_year}")
        
        global_avg_survival = year_data['Five_Year_Survival_%'].mean()
        global_avg_screening = year_data['Screening_Coverage_%'].mean()
        
        fig_comp = go.Figure(data=[
            go.Bar(name=selected_country, x=[t('survival_rate', lang), t('screening_coverage', lang), 
                                            t('early_detection', lang), t('treatment_coverage', lang)],
                  y=[data['Five_Year_Survival_%'], data['Screening_Coverage_%'],
                     data['Early_Detection_Rate_%'], data['Treatment_Coverage_%']],
                  marker_color='#FF1493'),
            go.Bar(name=t('global_average', lang), x=[t('survival_rate', lang), t('screening_coverage', lang),
                                               t('early_detection', lang), t('treatment_coverage', lang)],
                  y=[global_avg_survival, global_avg_screening,
                     year_data['Early_Detection_Rate_%'].mean(),
                     year_data['Treatment_Coverage_%'].mean()],
                  marker_color='#4169E1')
        ])
        
        fig_comp.update_layout(
            title=t('key_metrics_vs_global', lang),
            yaxis_title=t('percentage', lang),
            barmode='group',
            height=400
        )
        st.plotly_chart(fig_comp, use_container_width=True)
        
        # HDI Comparison
        st.subheader(t('hdi_comparison', lang))
        
        hdi_stats = year_data.groupby('HDI_Category').agg({
            'Five_Year_Survival_%': 'mean',
            'Screening_Coverage_%': 'mean'
        }).round(1)
        
        fig_hdi = go.Figure(data=[
            go.Bar(name=t('survival_rate', lang), x=hdi_stats.index, y=hdi_stats['Five_Year_Survival_%'],
                  marker_color='#FF1493'),
            go.Bar(name=t('screening_coverage', lang), x=hdi_stats.index, y=hdi_stats['Screening_Coverage_%'],
                  marker_color='#4169E1')
        ])
        
        fig_hdi.update_layout(
            title=t('health_metrics_hdi', lang),
            yaxis_title=t('percentage', lang),
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig_hdi, use_container_width=True)
        
        # Country Ranking
        st.subheader(f"{t('country_ranking', lang)} {selected_country} {t('rank', lang)}")
        
        survival_rank = (year_data['Five_Year_Survival_%'] > data['Five_Year_Survival_%']).sum() + 1
        screening_rank = (year_data['Screening_Coverage_%'] > data['Screening_Coverage_%']).sum() + 1
        total_countries = len(year_data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(t('survival_rank', lang), f"{survival_rank} / {total_countries}")
        
        with col2:
            st.metric(t('screening_rank', lang), f"{screening_rank} / {total_countries}")
        
        with col3:
            percentile = ((total_countries - survival_rank) / total_countries * 100)
            st.metric(t('survival_percentile', lang), f"{percentile:.0f}e")
    
    # Recommendations
    if show_recommendations:
        st.markdown("---")
        st.header(t('insights_recommendations', lang))
        
        concerns = []
        successes = []
        recommendations = []
        
        # Evaluate metrics
        if data['Screening_Coverage_%'] < 50:
            concerns.append(f"**{t('low_screening', lang)} ({data['Screening_Coverage_%']:.1f}%)**: {t('below_target', lang)}")
            recommendations.append(f"{t('increase_screening', lang)}: {t('mobile_units', lang)}")
        elif data['Screening_Coverage_%'] >= 70:
            successes.append(f"**{t('good_screening', lang)} ({data['Screening_Coverage_%']:.1f}%)**: {t('meets_targets', lang)}")
        
        if data['Early_Detection_Rate_%'] < 50:
            concerns.append(f"**{t('low_detection', lang)} ({data['Early_Detection_Rate_%']:.1f}%)**: {t('advanced_stages', lang)}")
            recommendations.append(f"{t('enhance_detection', lang)}: {t('awareness_campaigns', lang)}")
        elif data['Early_Detection_Rate_%'] >= 60:
            successes.append(f"**{t('strong_detection', lang)} ({data['Early_Detection_Rate_%']:.1f}%)**: {t('effective_programs', lang)}")
        
        if data['Five_Year_Survival_%'] < 50:
            concerns.append(f"**{t('low_survival', lang)} ({data['Five_Year_Survival_%']:.1f}%)**: {t('below_average', lang)}")
            recommendations.append(f"{t('improve_treatment', lang)}: {t('strengthen_infrastructure', lang)}")
        elif data['Five_Year_Survival_%'] >= 70:
            successes.append(f"**{t('high_survival', lang)} ({data['Five_Year_Survival_%']:.1f}%)**: {t('excellent_outcomes', lang)}")
        
        if data['MI_Ratio'] > 50:
            concerns.append(f"**{t('high_mi', lang)} ({data['MI_Ratio']:.1f}%)**: {t('late_detection', lang)}")
            recommendations.append(f"{t('reduce_mi', lang)}: {t('focus_quality', lang)}")
        elif data['MI_Ratio'] < 30:
            successes.append(f"**{t('low_mi', lang)} ({data['MI_Ratio']:.1f}%)**: {t('effective_response', lang)}")
        
        if data['Treatment_Coverage_%'] < 70:
            concerns.append(f"**{t('inadequate_treatment', lang)} ({data['Treatment_Coverage_%']:.1f}%)**: {t('not_receiving', lang)}")
            recommendations.append(f"{t('expand_treatment', lang)}: {t('increase_centers', lang)}")
        
        # Display
        if successes:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown(f"### {t('positive_aspects', lang)}")
            for success in successes:
                st.markdown(f"- {success}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if concerns:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown(f"### {t('areas_attention', lang)}")
            for concern in concerns:
                st.markdown(f"- {concern}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if recommendations:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown(f"### {t('actionable_recommendations', lang)}")
            for rec in recommendations:
                st.markdown(f"{rec}")
            
            st.markdown(f"\n**{t('general_recommendations', lang)}**")
            for i in range(1, 9):
                st.markdown(t(f'rec_{i}', lang))
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Understanding data
        st.markdown("---")
        st.subheader(t('understanding_data', lang))
        
        with st.expander(t('what_metrics_mean', lang)):
            st.markdown(f"""
            **{t('def_incidence', lang)}**
            
            **{t('def_mortality', lang)}**
            
            **{t('def_mi_ratio', lang)}**
            - **{t('mi_excellent', lang)}**
            - **{t('mi_moderate', lang)}**
            - **{t('mi_concerning', lang)}**
            
            **{t('def_screening', lang)}**
            - **{t('target', lang)}**: ≥ 70%
            
            **{t('def_detection', lang)}**
            - **{t('target', lang)}**: ≥ 60%
            
            **{t('def_treatment', lang)}**
            - **{t('target', lang)}**: ≥ 90%
            
            **{t('def_survival', lang)}**
            - **{t('target', lang)}**: ≥ 70%
            """)
        
        with st.expander(t('how_interpret', lang)):
            st.markdown(f"""
            **{t('low_resource', lang)}**
            {t('low_resource_1', lang)}
            {t('low_resource_2', lang)}
            {t('low_resource_3', lang)}
            
            **{t('medium_resource', lang)}**
            {t('medium_resource_1', lang)}
            {t('medium_resource_2', lang)}
            {t('medium_resource_3', lang)}
            
            **{t('high_resource', lang)}**
            {t('high_resource_1', lang)}
            {t('high_resource_2', lang)}
            {t('high_resource_3', lang)}
            
            **{t('red_flags', lang)}**
            {t('red_flag_1', lang)}
            {t('red_flag_2', lang)}
            {t('red_flag_3', lang)}
            """)

else:
    st.error(f"{t('no_data', lang)} {selected_country} {t('in', lang)} {selected_year}")

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>{t('footer_awareness', lang)}</strong></p>
    <p>{t('footer_detection', lang)}</p>
    <p><em>{t('footer_source', lang)}</em></p>
    <p><em>{t('footer_source1', lang)}</em></p>
    <p>{t('footer_purpose', lang)}</p>
    <p>{t('footer_author', lang)}</p>
</div>
""", unsafe_allow_html=True)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.info(f"""
**{t('about_dashboard', lang)}**

{t('about_text', lang)}

**{t('how_use', lang)}**
{t('how_use_1', lang)}
{t('how_use_2', lang)}
{t('how_use_3', lang)}
{t('how_use_4', lang)}

**{t('purpose', lang)}**
{t('purpose_text', lang)}

**{t('october_awareness', lang)}**
""")

st.sidebar.markdown("---")
st.sidebar.success(t('early_detection', lang))
