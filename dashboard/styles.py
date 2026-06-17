import streamlit as st

def inject_custom_css():
    """Injeta estilos CSS customizados para elevar a estética visual da aplicação."""
    css = """
    <style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Título principal com gradiente moderno */
    .main-title {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.3rem;
        font-weight: 700;
        text-align: left;
        margin-bottom: 5px;
        padding-top: 10px;
    }
    
    /* Subtítulo institucional */
    .sub-title {
        font-size: 1.1rem;
        color: #555;
        font-weight: 400;
        margin-bottom: 25px;
        border-bottom: 2px solid #eaeaea;
        padding-bottom: 15px;
    }
    
    /* Preâmbulo e destaques em blocos */
    .preamble-box {
        background-color: #f8f9fa;
        border-left: 4px solid #1D9E75;
        border-radius: 4px;
        padding: 15px 20px;
        margin: 20px 0;
        font-size: 0.95rem;
        color: #444;
        line-height: 1.6;
    }
    
    /* Container de cartões de KPI */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 15px;
        margin-bottom: 25px;
    }
    
    /* Cartão de KPI individual */
    .kpi-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #eaeaea;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    /* Efeito de hover suave no cartão de KPI */
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        border-color: #3498db;
    }
    
    /* Estilos internos do cartão de KPI */
    .kpi-label {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #7f8c8d;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 4px;
    }
    
    .kpi-sub {
        font-size: 0.8rem;
        color: #95a5a6;
    }
    
    /* Cores personalizadas para os KPIs */
    .kpi-blue { border-top: 4px solid #3498db; }
    .kpi-purple { border-top: 4px solid #9b59b6; }
    .kpi-green { border-top: 4px solid #2ecc71; }
    .kpi-red { border-top: 4px solid #e74c3c; }
    
    /* Estilo de box de estatísticas descritivas */
    .stats-box {
        background-color: #fcfcfc;
        border: 1px solid #eaeaea;
        border-radius: 6px;
        padding: 12px 15px;
        margin-top: 10px;
        font-size: 0.85rem;
        color: #333;
        line-height: 1.5;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    .stats-header {
        font-weight: 600;
        font-size: 0.9rem;
        color: #2c3e50;
        margin-bottom: 6px;
        border-bottom: 1px dashed #ddd;
        padding-bottom: 4px;
    }
    
    /* Estilo de rodapé profissional */
    .footer-text {
        text-align: center;
        font-size: 0.8rem;
        color: #888;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #eaeaea;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
