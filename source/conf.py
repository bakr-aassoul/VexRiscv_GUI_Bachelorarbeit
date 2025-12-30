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

Ziel der Arbeit ist die Entwicklung einer grafischen Benutzeroberfläche (GUI), die über die reine Selektion vorhandener Komponenten hinausgeht: Sie ermöglicht es, den Prozessor durch einen integrierten Code-Generator um anwendungsspezifische Befehlssatzerweiterungen (Custom Instructions) zu ergänzen. 
Die GUI abstrahiert dabei die Komplexität der zugrunde liegenden Hardwarebeschreibungssprache und transformiert benutzerdefinierte Logik vollautomatisch in synthetisierbaren SpinalHDL-Code. 
Anwender werden so schrittweise durch den gesamten Entwicklungsprozess geführt, von der Definition eigener Recheneinheiten über die Generierung des Prozessordesigns bis zur Simulation.

Zur funktionalen Überprüfung der erzeugten Konfigurationen und Erweiterungen wird eine RTL-Simulation mit Verilator durchgeführt. Die Signalverläufe, einschließlich der internen Abläufe der generierten Custom ALUs, werden anschließend mit GTKWave analysiert und verifiziert.
Aufbauend darauf erfolgt die Integration des Prozessors in ein LiteX-System-on-Chip sowie die Implementierung auf einem Pynq-Z1-FPGA, wodurch eine Evaluierung der Leistungsfähigkeit unter realen Hardwarebedingungen möglich wird.

Die Ergebnisse zeigen, dass sich der VexRiscv durch die entwickelte GUI und den integrierten Code-Generator nicht nur effizient konfigurieren, sondern gezielt um anwendungsspezifische Instruktionen erweitern lässt. Das System weist dabei sowohl in der Simulation als auch auf der Hardware ein reproduzierbares Verhalten auf.

Die Arbeit leistet damit einen Beitrag zur benutzerfreundlichen Exploration von RISC-V-Architekturen und stellt eine durchgängige Entwicklungsumgebung für das Design spezialisierter Hardwarebeschleuniger in Lehre und Forschung bereit.
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
