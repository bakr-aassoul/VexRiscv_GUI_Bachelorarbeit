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
latex_additional_files = ['fh-dortmund-logo.jpg']

latex_elements = {
    'pointsize': '14pt',
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
            \includegraphics[width=0.3\textwidth]{fh-dortmund-logo.jpg}
        \end{flushleft}
        \vspace*{2cm}
        \centering
        
        {\Huge \bfseries \textcolor{orange}{Bachelorarbeit} \par}  % <-- Added line
        \vspace{0.5cm}
        {\Huge \bfseries Konfiguration, Simulation und FPGA-basierte Evaluierung eines modularen Risc-V Prozessors mittels einer GUI-gestützten Entwicklungsumgebung \par}
        \vspace{1cm}
        

        \vfill
        
        {\Large \textbf{Bakr Aassoul} \par}
        {\large Matrikelnummer: 7215705 \par}
        \vspace{2cm}
        {\large \today \par}
        {\large an der Fachhochschule Dortmund \par}
        \vspace{3cm}
        \begin{flushleft}
            {\large \textbf{Erstprüfer:} Prof.\ Dr.\ Jens Rettkowski \par}
            {\large \textbf{Zweitprüfer:} Dipl.\ -Ing.\ Sebastian Kindler \par}
        \end{flushleft}
    \end{titlepage}

    \clearpage
    \null
    \thispagestyle{empty}
    \clearpage
    % %% --- START OF ABSTRACT SECTION --- %%
    
    \thispagestyle{plain} % Allows a page number here (optional)
    \begin{center}
        {\LARGE \bfseries Abstract \par}
    \end{center}
    \vspace{1cm}
    {\large
    % REPLACE THE TEXT BELOW WITH YOUR OWN ABSTRACT
    Diese Bachelorarbeit beschäftigt sich mit der Konfiguration, Simulation und FPGA-basierten Evaluierung eines modularen RISC-V-Prozessors auf Basis des in SpinalHDL entwickelten VexRiscv-Kerns. 
    Ziel der Arbeit ist die Entwicklung einer grafischen Benutzeroberfläche, die es ermöglicht, den Prozessor über ein flexibles Plugin-System zu konfigurieren und automatisch bis hin zu einem lauffähigen Verilog-Design zu generieren. 
    Die GUI abstrahiert die Komplexität der zugrunde liegenden Toolchain und führt Anwender schrittweise durch den gesamten Entwicklungsprozess, von der Auswahl der Architekturkomponenten über die Codegenerierung bis zur Simulation.

    Zur funktionalen Überprüfung der erzeugten Prozessorkonfigurationen wird eine RTL-Simulation mit Verilator durchgeführt, deren Signalverläufe anschließend mit GTKWave analysiert werden. 
    Aufbauend darauf erfolgt die Integration des Prozessors in ein LiteX-System-on-Chip sowie die Implementierung auf einem Pynq-Z1-FPGA, wodurch eine Evaluierung unter realen Hardwarebedingungen möglich wird. 
    Die Ergebnisse zeigen, dass sich der VexRiscv durch die modulare Architektur und die entwickelte GUI effizient an unterschiedliche Anforderungen anpassen lässt und sowohl in Simulation als auch auf Hardware ein reproduzierbares und nachvollziehbares Verhalten aufweist.

    Die Arbeit leistet damit einen Beitrag zur benutzerfreundlichen Exploration von RISC-V-Prozessorarchitekturen und stellt eine vollständige Entwicklungsumgebung für Lehre, Forschung und prototypische Hardwareentwicklung bereit.
    
    % %% --- END OF ABSTRACT SECTION --- %%
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
