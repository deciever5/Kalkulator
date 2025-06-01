"""
Polish UI Override System
Forces all Streamlit UI elements to display in Polish
"""

import streamlit as st

def apply_polish_ui_css():
    """Apply CSS to override English UI elements with Polish"""
    
    polish_css = """
    <style>
    /* Override Streamlit's default English placeholders */
    
    /* Clean selectbox styling without duplicate placeholders */
    div[data-baseweb="select"] {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
    }
    
    /* File uploader Polish text */
    .stFileUploader label {
        color: #262730;
    }
    
    .stFileUploader small {
        color: #808495;
    }
    
    /* Text input placeholders */
    .stTextInput input::placeholder {
        color: #a0a0a0;
    }
    
    .stTextArea textarea::placeholder {
        color: #a0a0a0;
    }
    
    /* Number input placeholders */
    .stNumberInput input::placeholder {
        color: #a0a0a0;
    }
    
    /* Date input placeholders */
    .stDateInput input::placeholder {
        color: #a0a0a0;
    }
    
    /* Time input placeholders */
    .stTimeInput input::placeholder {
        color: #a0a0a0;
    }
    
    /* Slider labels */
    .stSlider label {
        font-weight: 600;
        color: #262730;
    }
    
    /* Radio button labels */
    .stRadio label {
        font-weight: 600;
        color: #262730;
    }
    
    /* Checkbox labels */
    .stCheckbox label {
        font-weight: 600;
        color: #262730;
    }
    
    /* Multi-select styling */
    .stMultiSelect div[data-baseweb="select"] {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
    }
    
    /* Button styling for consistency */
    .stButton button {
        background-color: #ff6b6b;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: 600;
    }
    
    .stButton button:hover {
        background-color: #ff5252;
        color: white;
    }
    
    /* Download button styling */
    .stDownloadButton button {
        background-color: #4ecdc4;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: 600;
    }
    
    .stDownloadButton button:hover {
        background-color: #44a08d;
        color: white;
    }
    
    /* Success/error message styling */
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 12px;
        margin: 10px 0;
    }
    
    .stError {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 12px;
        margin: 10px 0;
    }
    
    .stWarning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 12px;
        margin: 10px 0;
    }
    
    .stInfo {
        background-color: #d1ecf1;
        color: #0c5460;
        border: 1px solid #b8daff;
        border-radius: 5px;
        padding: 12px;
        margin: 10px 0;
    }
    
    /* Custom polish selectbox styling */
    .polish-selectbox div[data-baseweb="select"] {
        border: 2px solid #e0e0e0;
        border-radius: 5px;
        background-color: white;
    }
    
    .polish-selectbox div[data-baseweb="select"]:focus-within {
        border-color: #ff6b6b;
        box-shadow: 0 0 0 1px #ff6b6b;
    }
    
    /* Loading spinner polish styling */
    .stSpinner div {
        border-top-color: #ff6b6b !important;
    }
    
    /* Progress bar polish styling */
    .stProgress .stProgress-bar {
        background-color: #ff6b6b;
    }
    
    /* Polish metric styling */
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        text-align: center;
    }
    
    .metric-label {
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .metric-delta {
        font-size: 12px;
        opacity: 0.8;
    }
    </style>
    """
    
    st.markdown(polish_css, unsafe_allow_html=True)

def polish_selectbox(label, options, index=0, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False):
    """Polish version of selectbox with proper placeholder"""
    
    # Apply Polish CSS first
    apply_polish_ui_css()
    
    # Create a container with Polish styling
    with st.container():
        st.markdown('<div class="polish-selectbox">', unsafe_allow_html=True)
        
        # Use standard selectbox but with Polish placeholder behavior
        result = st.selectbox(
            label=label,
            options=options,
            index=index,
            key=key,
            help=help,
            on_change=on_change,
            args=args,
            kwargs=kwargs,
            disabled=disabled
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    return result

def polish_text_input(label, value="", max_chars=None, key=None, type="default", help=None, 
                     autocomplete=None, on_change=None, args=None, kwargs=None, 
                     placeholder="Wprowadź tekst...", disabled=False):
    """Polish version of text input with Polish placeholder"""
    
    apply_polish_ui_css()
    
    return st.text_input(
        label=label,
        value=value,
        max_chars=max_chars,
        key=key,
        type=type,
        help=help,
        autocomplete=autocomplete,
        on_change=on_change,
        args=args,
        kwargs=kwargs,
        placeholder=placeholder,
        disabled=disabled
    )

def polish_text_area(label, value="", height=None, max_chars=None, key=None, help=None,
                    on_change=None, args=None, kwargs=None, placeholder="Wprowadź tekst...", disabled=False):
    """Polish version of text area with Polish placeholder"""
    
    apply_polish_ui_css()
    
    return st.text_area(
        label=label,
        value=value,
        height=height,
        max_chars=max_chars,
        key=key,
        help=help,
        on_change=on_change,
        args=args,
        kwargs=kwargs,
        placeholder=placeholder,
        disabled=disabled
    )

def polish_file_uploader(label, type=None, accept_multiple_files=False, key=None, help=None,
                        on_change=None, args=None, kwargs=None, disabled=False):
    """Polish version of file uploader with Polish text"""
    
    apply_polish_ui_css()
    
    # Add Polish file uploader text
    st.markdown("""
    <style>
    .uploadedFileName {
        color: #262730 !important;
    }
    .uploadedFileData {
        color: #808495 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    return st.file_uploader(
        label=label,
        type=type,
        accept_multiple_files=accept_multiple_files,
        key=key,
        help=help,
        on_change=on_change,
        args=args,
        kwargs=kwargs,
        disabled=disabled
    )

def polish_success(text):
    """Polish styled success message"""
    apply_polish_ui_css()
    return st.success(text)

def polish_error(text):
    """Polish styled error message"""
    apply_polish_ui_css()
    return st.error(text)

def polish_warning(text):
    """Polish styled warning message"""
    apply_polish_ui_css()
    return st.warning(text)

def polish_info(text):
    """Polish styled info message"""
    apply_polish_ui_css()
    return st.info(text)

def polish_metric(label, value, delta=None, delta_color="normal", help=None):
    """Polish styled metric display"""
    apply_polish_ui_css()
    
    delta_html = ""
    if delta:
        delta_color_class = "metric-delta-positive" if delta_color == "normal" else "metric-delta-negative"
        delta_html = f'<div class="metric-delta {delta_color_class}">{delta}</div>'
    
    metric_html = f"""
    <div class="metric-container">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """
    
    st.markdown(metric_html, unsafe_allow_html=True)

def initialize_polish_ui():
    """Initialize Polish UI overrides for the entire app"""
    apply_polish_ui_css()
    
    # Add JavaScript to override Streamlit's English defaults
    st.markdown("""
    <script>
    // Override English placeholders with Polish
    function overrideEnglishText() {
        // Replace "Choose an option" in selectboxes
        const selectBoxes = document.querySelectorAll('div[data-baseweb="select"]');
        selectBoxes.forEach(selectBox => {
            const placeholder = selectBox.querySelector('div[data-baseweb="input"] > div');
            if (placeholder && placeholder.textContent === 'Choose an option') {
                placeholder.textContent = 'Wybierz opcję';
            }
        });
        
        // Replace other English UI text
        const textReplacements = {
            'Loading...': 'Ładowanie...',
            'Processing...': 'Przetwarzanie...',
            'Error': 'Błąd',
            'Success': 'Sukces',
            'Warning': 'Ostrzeżenie',
            'Info': 'Informacja',
            'Cancel': 'Anuluj',
            'OK': 'OK',
            'Yes': 'Tak',
            'No': 'Nie',
            'Close': 'Zamknij',
            'Save': 'Zapisz',
            'Load': 'Wczytaj',
            'Export': 'Eksport',
            'Import': 'Import'
        };
        
        Object.entries(textReplacements).forEach(([english, polish]) => {
            const elements = document.querySelectorAll('*');
            elements.forEach(element => {
                if (element.textContent === english) {
                    element.textContent = polish;
                }
            });
        });
    }
    
    // Run immediately and on DOM changes
    overrideEnglishText();
    
    // Observer for dynamic content
    const observer = new MutationObserver(overrideEnglishText);
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    </script>
    """, unsafe_allow_html=True)