# Configuration file for the Sphinx documentation builder.

# -- Project Information -----------------------------------------------------
project = 'Bachelorarbeit'
copyright = '2025, Bakr Aassoul'
author = 'Bakr Aassoul'

# -- General Configuration ---------------------------------------------------
extensions = ['myst_parser']
source_suffix = {'.rst': 'restructuredtext', '.md': 'markdown'}
exclude_patterns = []

# -- Options for HTML Output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']

# -- LaTeX Configurations ----------------------------------------------------
latex_engine = 'xelatex'
latex_additional_files = ['fh-dortmund-logo.jpg']

# 1. SWITCH TO KOMA-SCRIPT (Better for German Theses)
latex_docclass = {
   'manual': 'scrreprt',
}

latex_elements = {
    # 2. SET EXACTLY 13pt HERE
    # KOMA-Script allows 'fontsize=13pt'
    'pointsize': 'fontsize=13pt',
    
    # 3. KOMA-Script specific settings to make it look like a standard report
    # 'classoptions': ',twoside,openright', # Optional: for double-sided printing
    
    'sphinxsetup': 'verbatimwithframe=true, verbatimwrapslines=true',
    
    'preamble': r'''
        \usepackage{lmodern}
        \usepackage{fancyhdr}
        \usepackage{graphicx}
        \usepackage{xcolor}

        % Force serif font for headings (KOMA defaults to Sans Serif)
        \addtokomafont{disposition}{\rmfamily}

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
            \includegraphics[width=0.2\textwidth]{fh-dortmund-logo.jpg}
        \end{flushleft}
        \vspace*{2cm}
        \centering
        
        {\huge \bfseries \textcolor{orange}{Bachelorarbeit} \par}
        \vspace{0.5cm}
        {\huge \bfseries Konfiguration, Simulation und FPGA-basierte Evaluierung eines modularen Risc-V Prozessors mittels einer GUI-gestützten Entwicklungsumgebung \par}
        \vspace{1cm}
        
        \vfill
        
        {\large \textbf{Bakr Aassoul} \par}
        {\normalsize Matrikelnummer: 7215705 \par}
        \vspace{2cm}
        {\normalsize \today \par}
        {\normalsize an der Fachhochschule Dortmund \par}
        \vspace{3cm}
        \begin{flushleft}
            {\normalsize \textbf{Erstprüfer:} Prof.\ Dr.\ Jens Rettkowski \par}
            {\normalsize \textbf{Zweitprüfer:} Dipl.\ -Ing.\ Sebastian Kindler \par}
        \end{flushleft}
    \end{titlepage}

    \clearpage
    \null
    \thispagestyle{empty}
    \clearpage
    
    \thispagestyle{plain} 
    \begin{center}
        {\LARGE \bfseries Abstract \par}
    \end{center}
    \vspace{1cm}
    {\large
    Diese Bachelorarbeit beschäftigt sich mit der Konfiguration, Simulation und FPGA-basierten Evaluierung eines modularen RISC-V-Prozessors auf Basis des in SpinalHDL entwickelten VexRiscv-Kerns. 
    Ziel der Arbeit ist die Entwicklung einer grafischen Benutzeroberfläche, die es ermöglicht, den Prozessor über ein flexibles Plugin-System zu konfigurieren und automatisch bis hin zu einem lauffähigen Verilog-Design zu generieren. 
    Die GUI abstrahiert die Komplexität der zugrunde liegenden Toolchain und führt Anwender schrittweise durch den gesamten Entwicklungsprozess, von der Auswahl der Architekturkomponenten über die Codegenerierung bis zur Simulation.

    Zur funktionalen Überprüfung der erzeugten Prozessorkonfigurationen wird eine RTL-Simulation mit Verilator durchgeführt, deren Signalverläufe anschließend mit GTKWave analysiert werden. 
    Aufbauend darauf erfolgt die Integration des Prozessors in ein LiteX-System-on-Chip sowie die Implementierung auf einem Pynq-Z1-FPGA, wodurch eine Evaluierung unter realen Hardwarebedingungen möglich wird. 
    Die Ergebnisse zeigen, dass sich der VexRiscv durch die modulare Architektur und die entwickelte GUI effizient an unterschiedliche Anforderungen anpassen lässt und sowohl in Simulation als auch auf Hardware ein reproduzierbares und nachvollziehbares Verhalten aufweist.

    Die Arbeit leistet damit einen Beitrag zur benutzerfreundlichen Exploration von RISC-V-Prozessorarchitekturen und stellt eine vollständige Entwicklungsumgebung für Lehre, Forschung und prototypische Hardwareentwicklung bereit.
    }
    \clearpage
''',
}

language = 'de'

latex_documents = [
    ('index',
     'Bachelorarbeit.tex',
     'Bachelorarbeit',
     'Bakr Aassoul',
     'manual'),
]
