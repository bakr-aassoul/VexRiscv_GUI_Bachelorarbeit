# Einleitung

## Motivation

In den letzten Jahren hat sich **RISC-V** als offene Prozessorarchitektur zu einem zentralen Bestandteil moderner Forschungs- und Entwicklungsprojekte etabliert.  
Ihre modulare und lizenzfreie Struktur ermöglicht es, maßgeschneiderte CPU-Designs zu entwickeln und an spezifische Anwendungen anzupassen von eingebetteten Systemen bis hin zu KI-Beschleunigern.

**SpinalHDL** stellt dabei eine moderne Hardwarebeschreibungssprache dar, die die Produktivität bei der Prozessorentwicklung erheblich steigert.  
Sie kombiniert die Vorteile von **Scala** (objektorientiert und funktional) mit der Möglichkeit, effizienten **Verilog-Code** zu generieren.

Das in SpinalHDL implementierte Projekt **VexRiscv** ist ein konfigurierbarer 32-Bit-RISC-V-Prozessor, dessen Architektur sich durch ein Plugin-System flexibel anpassen lässt.  
Jedes Plugin implementiert eine klar abgegrenzte Funktionalität wie beispielsweise den **Integer-ALU**, **Branch-Handling**, oder den **CSR-Zugriff**.  
Dadurch können Entwickler gezielt Leistungsmerkmale oder Pipeline-Stufen aktivieren und deaktivieren.

## Ziel der Arbeit

Ziel dieser Bachelorarbeit ist die Entwicklung einer **grafischen Benutzeroberfläche (GUI)**,  
mit der sich der **VexRiscv-Prozessor** komfortabel konfigurieren und automatisch bis hin zum lauffähigen Verilog-Design erzeugen lässt.  
Der Fokus liegt auf der **Automatisierung des Designprozesses** – von der Plugin-Auswahl über die Verilog-Generierung bis zur Simulation und Signalvisualisierung mit **GTKWave**.

Die GUI soll insbesondere Studierenden und Forschern den Einstieg in SpinalHDL erleichtern,  
da sich komplexe Konfigurationsschritte damit intuitiv über Checkboxen und Buttons ausführen lassen, ohne die Scala-Quelltexte manuell zu bearbeiten.

## Vorgehensweise

Im Verlauf der Arbeit wird zunächst die **VexRiscv-Architektur** analysiert und die Funktionsweise der wichtigsten Plugins beschrieben.  
Anschließend wird die grafische Designumgebung implementiert und um Funktionen wie  
*„Auto-add required plugins“*, *Simulation (Verilator)* und *Signalvisualisierung (GTKWave)* ergänzt.  
Zum Abschluss erfolgt eine Simulation des generierten Prozessors zur Verifikation der Funktionalität.
