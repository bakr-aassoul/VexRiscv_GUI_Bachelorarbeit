# Einleitung

## Motivation

Ein Chip ist die Grundlage der gesamten Informations- und Elektronikindustrie, wobei die ISA (Instruction Set Architecture ) die zentrale technische Basis eines jeden Prozessors darstellt.

In den letzten Jahrzehnten haben sich zwei wichtige Befehlssatzarchitekturen (ISAs) auf dem Mikroprozessormarkt durchgesetzt: ARM und x86. Beide sind jedoch proprietär oder lizenzpflichtig. Dies stellt für bestimmte industrielle und akademische Andendungsbereiche einen Nachteil dar, etwa für individuelles Chipdesign oder für die Forschung, die volle Transparenz erfordern. Im Gegensatz dazu bietet RISC_V eine offene, lizenzgebührenfreie ISA, die jeder ohne solche Einschränkungen nutzen, modifizieren und für eigene Hardware Designs verwenden kann {cite}`RISCV19` .
Diese Offenheit hat RISC-V in den letzten Jahren zu einem wichtigen Treiber für Innovation, Forschung und Lehre im Bereich der Prozessorentwicklung gemacht.

SpinalHDL stellt dabei eine moderne Hardwarebeschreibungssprache dar, die die Produktivität bei der Prozessorentwicklung erheblich steigert. Sie kombiniert die Vorteile von Scala (objektorientiert und funktional) mit der Möglichkeit, effizienten Verilog-Code zu generieren.
Das in SpinalHDL implementierte Projekt VexRiscv ist ein konfigurierbarer 32 Bit-RISC-V-Prozessor, dessen Architektur sich durch ein Plugin-System flexibel anpassen lässt.
Jedes Plugin implementiert eine klar abgegrenzte Funktionalität wie beispielsweise den Integer-ALU, Branch-Handling, oder den CSR-Zugriff. Dadurch können Entwickler gezielt Leistungsmerkmale oder Pipeline-Stufen aktivieren und deaktivieren.
Ein entscheidender Vorteil der offenen RISC-V-Architektur ist die Möglichkeit, den Befehlssatz um anwendungsspezifische Instruktionen (Custom Instructions) zu erweitern.
In Bereichen wie Kryptografie oder Signalverarbeitung können solche spezialisierten Rechenwerke die Effizienz drastisch steigern. Die Hürde für die Implementierung solcher Erweiterungen ist jedoch oft hoch, da sie tiefe Kenntnisse in Hardwarebeschreibungssprachen erfordern.
Hier setzt die Motivation dieser Arbeit an: Den Zugang zu Hardware-Modifikationen durch Automatisierung zu vereinfachen.

## Ziel der Arbeit

Ziel dieser Bachelorarbeit ist die Entwicklung einer grafischen Benutzeroberfläche (GUI), mit der sich der VexRiscv-Prozessor nicht nur komfortabel konfigurieren, sondern auch durch benutzerdefinierte Instruktionen gezielt erweitern lässt. 
Der Fokus liegt auf der Automatisierung des Designprozesses und Entwurfsprozesses, von der Plugin-Auswahl über die Generierung anwendungsspezifischer Hardware-Logik bis zur Simulation und Verifikation.

Ein besonderer Schwerpunkt liegt auf der Integration eines durchgängigen Workflows, der folgende Kernaspekte umfasst:

- **Plugin-Konfiguration:** Die intuitive Auswahl und Parametrierung vorhandener Architekturkomponenten sowie die automatische Ergänzung notwendiger Pipeline-Module.
- **Custom Instruction Generation:** Die Implementierung eines Code-Generators, der es ermöglicht, anwendungsspezifische Recheneinheiten (Custom ALUs) über eine High-Level-Eingabe zu definieren und vollautomatisch in die CPU-Pipeline zu integrieren.
- **Code-Erzeugung:** Die automatisierte Generierung der vollständigen Scala- und Verilog-Quelltexte mittels SpinalHDL.
- **Simulation** des resultierenden Prozessors mit Verilator,
- **Verifikation:** Die direkte Simulation des resultierenden Prozessors mit Verilator sowie die Signalvisualisierung in GTKWave, um interne Abläufe wie Pipeline-Stufen, Speicherzugriffe und die Ausführung der benutzerdefinierten Befehle detailliert analysieren zu können.

Die entwickelte GUI soll insbesondere Studierenden und Forschern den Einstieg in SpinalHDL und das Design domänenspezifischer Architekturen (Domain-Specific Architectures) erleichtern. Sowohl komplexe Konfigurationsschritte als auch die Erweiterung des Befehlssatzes lassen sich damit intuitiv ausführen, ohne die Scala-Quelltexte manuell bearbeiten zu müssen.

Darüber hinaus umfasst die Arbeit eine FPGA-basierte Evaluierung der generierten Prozessorkonfigurationen, um deren Funktionsfähigkeit und Effizienz unter realen Hardwarebedingungen zu überprüfen.


## Vorgehensweise

Im Verlauf dieser Arbeit wird zunächst die Architektur des VexRiscv-Prozessors analysiert und die Funktionsweise seines modularen Plugin-Systems erläutert. 
Darauf aufbauend erfolgt die Implementierung einer grafischen Entwicklungsumgebung, die den Entwurfsprozess nicht nur vereinfacht, sondern durch generative Ansätze funktional erweitert.

 Die technische Umsetzung gliedert sich dabei in folgende Kernbereiche, die sukzessive realisiert werden:
 
- **Architekturanalyse:** Untersuchung der Schnittstellen (DecoderService, Execute-Stage), die für die Integration eigener Hardware-Erweiterungen notwendig sind,
- **Frontend-Entwicklung:** Gestaltung einer intuitiven Benutzeroberfläche zur Konfiguration der Standard-Plugins sowie zur Definition benutzerdefinierter ALUs.
- **Backend-Implementierung:** Entwicklung eines Python-basierten Code-Generators, der Benutzereingaben dynamisch in synthetisierbaren SpinalHDL-Code übersetzt und die notwendigen Scala-Klassen in den Build-Prozess injiziert.
- **Automatisierung:** Integration der *„Auto-add required plugins“*-Logik zur Sicherstellung valider Konfigurationen sowie die Anbindung der Simulationswerkzeuge.

Abschließend wird der mit der GUI erzeugte Prozessor umfassend evaluiert. 
Dies beinhaltet die funktionale Verifikation der generierten Custom Instructions mittels Verilator-Simulation und Wellenformanalyse in GTKWave sowie die Integration in ein LiteX-SoC zur Validierung auf der FPGA-Hardware. 
Damit stellt die Arbeit einen vollständigen Workflow von der Definition einer Instruktion bis zur physikalischen Ausführung bereit.
