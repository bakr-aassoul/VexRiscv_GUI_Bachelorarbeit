# Configuration file for the Sphinx documentation builder.

# -- Project Information -----------------------------------------------------
project = 'Bachelorarbeit'
copyright = '2025, Bakr Aassoul'
author = 'Bakr Aassoul'

# -- General Configuration ---------------------------------------------------
extensions = ['myst_parser']  # Markdown via MyST

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

exclude_patterns = []  # Nothing excluded

# -- Options for HTML Output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']

# -- LaTeX Configurations ----------------------------------------------------
latex_engine = 'xelatex'

# Tell Sphinx to copy the logo into the LaTeX build dir
latex_additional_files = ['fh-dortmund-logo.png']

latex_elements = {
    'sphinxsetup': 'verbatimwithframe=true, verbatimwrapslines=true',
    'preamble': r'''
        % XeLaTeX handles UTF-8 natively, so inputenc/fontenc not needed
        \usepackage{lmodern}
        \usepackage{fancyhdr}
        \usepackage{graphicx}
    
        \makeatletter
        \fancypagestyle{normal}{
            \fancyhf{}
            \fancyfoot[LE,RO]{\py@HeaderFamily\thepage}
            \fancyfoot[LO,RE]{\py@HeaderFamily\nouppercase{\leftmark}}
            \renewcommand{\headrulewidth}{0.4pt}
            \renewcommand{\footrulewidth}{0.4pt}
        }
        \makeatother
    ''',
    'maketitle': r'''
    \begin{titlepage}
        \begin{flushleft}
            % Replace 'fh-dortmund-logo.png' with the actual filename of your image.
            % Adjust 'width=0.2\textwidth' to change the logo's size.
            \includegraphics[width=0.2\textwidth]{fh-dortmund-logo.png}
        \end{flushleft}
        \vspace*{2cm}
        \centering
        
        
        {\Huge \bfseries Konfiguration, Simulation und FPGA-basierte Evaluierung eines modularen Risc-V Prozessors mittels einer GUI-gestützten Entwicklungsumgebung \par}
        \vspace{1cm}
        {\Huge \textcolor{orange}{Bachelorarbeit} \par}  % <-- Added line
        \vspace{0.5cm}

        \vfill
        {\large Erstprüfer: Prof.\ Dr.\ Jens Rettkowski \par}
        {\large Zweitprüfer: Dipl.\ -Ing.\ Sebastian Kindler \par}
        \vspace{1cm}
        {\Large Bakr Aassoul \par}
        \vspace{0.5cm}
        {\large Matrikelnummer: 7215705 \par}
        \vspace{1cm}
        {\large \today \par}
        \vspace{0.5cm}
        {\large an der Fachhochschule Dortmund \par}
    \end{titlepage}

    \clearpage
    \null
    \thispagestyle{empty}
    \clearpage
''',
}

language = 'de'

latex_documents = [
    ('index',
     'SpinalHDL.tex',
     'Bachelorarbeit',
     'Bakr Aassoul',
     'manual'),
]
