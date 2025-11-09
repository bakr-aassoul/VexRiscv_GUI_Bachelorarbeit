# Einleitung

## Motivation

Ein Chip ist die Grundlage der gesamten Informations- und Elektronikindustrie, wobei die ISA (Instruction Set Architecture ) die zentrale technische Basis eines jeden Prozessors darstellt.

In den letzten Jahrzehnten haben sich zwei wichtige Befehlssatzarchitekturen (ISAs) auf dem Mikroprozessormarkt durchgesetzt: ARM und x86. Beide sind jedoch proprietär oder lizenzpflichtig. Dies stellt für bestimmte industrielle und akademische Andendungsbereiche einen Nachteil dar, etwa für individuelles Chipdesign oder für die Forschung, die volle Transparenz erfordern. Im Gegensatz dazu bietet RISC_V eine offene, lizenzgebührenfreie ISA, die jeder ohne solche Einschränkungen nutzen, modifizieren und für eigene Hardware Designs verwenden kann.
Diese Offenheit hat RISC-V in den letzten Jahren zu einem wichtigen Treiber für Innovation, Forschung und Lehre im Bereich der Prozessorentwicklung gemacht.

SpinalHDL stellt dabei eine moderne Hardwarebeschreibungssprache dar, die die Produktivität bei der Prozessorentwicklung erheblich steigert. Sie kombiniert die Vorteile von Scala (objektorientiert und funktional) mit der Möglichkeit, effizienten Verilog-Code zu generieren.
Das in SpinalHDL implementierte Projekt VexRiscv ist ein konfigurierbarer 32 Bit-RISC-V-Prozessor, dessen Architektur sich durch ein Plugin-System flexibel anpassen lässt.
Jedes Plugin implementiert eine klar abgegrenzte Funktionalität wie beispielsweise den Integer-ALU, Branch-Handling, oder den CSR-Zugriff. Dadurch können Entwickler gezielt Leistungsmerkmale oder Pipeline-Stufen aktivieren und deaktivieren.

## Ziel der Arbeit

Ziel dieser Bachelorarbeit ist die Entwicklung einer grafischen Benutzeroberfläche (GUI), mit der sich der VexRiscv-Prozessor komfortabel konfigurieren und automatisch bis hin zum lauffähigen Verilog-Design erzeugen lässt.  
Der Fokus liegt auf der Automatisierung des Designprozesses von der Plugin-Auswahl über die Verilog-Generierung bis zur Simulation und Signalvisualisierung mit GTKWave.

Die GUI soll insbesondere Studierenden und Forschern den Einstieg in SpinalHDL erleichtern, da sich komplexe Konfigurationsschritte damit intuitiv über Checkboxen und Buttons ausführen lassen, ohne die Scala-Quelltexte manuell zu bearbeiten.

## Vorgehensweise

Im Verlauf dieser Arbeit wird zunächst die VexRiscv-Architektur im Detail analysiert und die Funktionsweise ihrer zentralen Plugins beschrieben.  
Darauf aufbauend erfolgt die Implementierung einer grafischen Designumgebung, die den Entwurfsprozess automatisiert und benutzerfreundlich gestaltet.  

Die entwickelte GUI wird schrittweise um Funktionen erweitert, darunter:  
- *„Auto-add required plugins“* zur automatischen Ergänzung essenzieller Pipeline-Komponenten,  
- *Simulation (Verilator)* zur funktionalen Überprüfung des generierten Prozessors,  
- sowie *Signalvisualisierung (GTKWave)* zur Analyse der internen CPU-Aktivitäten.  

Zum Abschluss wird der mit der GUI erzeugte Prozessor simuliert,  
um seine Funktionsfähigkeit und Korrektheit anhand der Signalverläufe und Testprogramme zu verifizieren.
