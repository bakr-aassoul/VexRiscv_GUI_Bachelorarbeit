# Systemarchitektur
```{raw} latex
\large
```
In diesem Kapitel wird die Architektur des gesamten Entwicklungs- und Evaluierungssystems beschrieben, das im Rahmen dieser Arbeit realisiert wurde. 
Der Fokus liegt dabei auf dem Zusammenspiel der einzelnen Module: von der GUI-basierten Konfigurationsumgebung über den internen Aufbau des VexRiscv-Prozessors und die Integration in ein LiteX-SoC bis hin zur physischen Umsetzung auf der FPGA-Plattform.

Das zentrale Ziel der entworfenen Architektur ist die Schaffung eines durchgängigen Workflows, der über die reine Parametrierung bestehender Komponenten hinausgeht. 
Ein wesentliches Merkmal ist die Fähigkeit zur generativen Erweiterung der Hardware: Es wird erläutert, wie aus abstrakten benutzerdefinierten Konfigurationen und logischen Definitionen (Custom Instructions) vollautomatisch ein lauffähiges Hardwaredesign entsteht, das anschließend nahtlos auf dem FPGA getestet und analysiert werden kann.

Die Systemarchitektur basiert dabei auf einem modularen Softcore-Design, das durch eine eigens entwickelte grafische Benutzeroberfläche ergänzt wird. 
Diese GUI fungiert als zentrale Steuerzentrale, um unterschiedliche Varianten des VexRiscv-Prozessorkerns nicht nur zu konfigurieren, sondern automatisiert zu erzeugen, in eine System-on-Chip-Umgebung (SoC) einzubetten und schließlich auf einer FPGA-Plattform zu evaluieren. Die einzelnen Systemkomponenten, von der GUI über die Codegenerierung und SoC-Integration bis zur Simulation und physischen FPGA-Implementierung, greifen dabei eng ineinander und bilden einen geschlossenen, iterativen Entwicklungs- und Evaluierungsworkflow.

**ABBILDUNG 4.1: Systemarchitektur-Überblick**
```{raw} latex
\clearpage
```
---

```{raw} latex
\normalsize
```
## GUI-basierte Konfigurationsschicht


Den Ausgangspunkt der Systemarchitektur bildet die im Rahmen dieser Arbeit entwickelte GUI. Sie dient als abstrahierende Schicht, über die der VexRiscv-Prozessor konfiguriert werden kann, ohne direkt in den SpinalHDL-Quellcode eingreifen zu müssen.

Das System unterscheidet architektonisch zwischen zwei Arten der Benutzerinteraktion:

- **Statische Konfiguration:** Der Benutzer wählt in der Oberfläche gewünschte Architekturmerkmale aus, etwa die Aktivierung von Multiplikations- und Divisionsmodulen, die Art des Shifters oder die Nutzung des CSR-Plugins. Hierbei werden lediglich Parameter in der bestehenden VexRiscv-Klasse gesetzt.
- **Dynamische Generierung:** Für benutzerdefinierte Recheneinheiten (Custom ALUs) erweitert die GUI den Entwurfsprozess um eine generative Komponente. Anstatt nur vorhandene Module zu aktivieren, nimmt die GUI Logik-Definitionen (z. B. rs1 + rs2) entgegen. Das Backend generiert daraus vollautomatisch neuen Quellcode und injiziert diesen in die Dateistruktur des Prozessors.

Auf Basis dieser Eingaben erstellt die GUI eine angepasste Top-Level-Definition (z. B. *VexRiscvTopFromGui.scala*) und stößt den SBT-Buildprozess an. 
Dadurch wird der Übergang von der architekturellen Beschreibung zu einer synthetisierbaren Hardwareimplementierung weitgehend entkoppelt und für den Benutzer stark vereinfacht.

```{raw} latex
\clearpage
```

## Prozessor- und SoC-Ebene

Die durch die GUI generierte Konfiguration beschreibt einen konkreten VexRiscv-Prozessorkern, der aus einer Kombination verschiedener Plugins besteht. 
Dazu gehören insbesondere Einheiten für Instruktions- und Datenzugriffe, die arithmetisch-logische Einheit, Shifter und Branch-Logik, das Registerfile, die Hazard-Behandlung sowie die Verwaltung der Control-and-Status-Register. 
Je nach gewählter Konfiguration können zusätzliche Funktionseinheiten wie Multiplikation und Division oder weitere Spezialfunktionen integriert werden.

**Integration der Custom ALU (Tight Coupling)** 
Ein wesentliches Architekturmerkmal dieser Arbeit ist die Art der Integration benutzerdefinierter Befehle. Im Gegensatz zu klassischen Co-Prozessoren, die oft über einen externen Bus angebunden sind, wird die generierte Custom ALU tief in die Pipeline integriert. Sie sitzt architektonisch parallel zur Standard-ALU in der *Execute-Stufe*. Dies ermöglicht einen direkten Zugriff auf die Registerwerte ohne Latenz und erlaubt die Rückführung des Ergebnisses im selben Taktzyklus ("Single Cycle Execution").
**ABBILDUNG 4.2: Diagramm, das zeigt, wie die Custom ALU parallel zur Standard ALU sitzt**

Auf diese Weise lässt sich der Umfang des Prozessors gezielt an den gewünschten Einsatzzweck anpassen, von einer kompakten, ressourcenschonenden Ausführung bis hin zu einer leistungsfähigeren Variante mit erweitertem Befehlssatz.

**SoC-Integration mit LiteX**
Um den Prozessor in einem lauffähigen Gesamtsystem zu betreiben, wird er mithilfe von **LiteX** in eine **System-on-Chip-Struktur** eingebettet. 
LiteX stellt dabei die notwendige Systeminfrastruktur bereit. 
Es generiert eine einheitliche Busarchitektur, verbindet den Prozessor mit Speicherressourcen wie internem SRAM oder externem DRAM und bindet grundlegende Peripheriefunktionen wie UART, Timer oder GPIO an. 
Gleichzeitig übernimmt LiteX die Adressierung und die Systeminitialisierung, sodass aus der Kombination von VexRiscv-Core und LiteX-Modulen ein voll funktionsfähiges SoC entsteht, das sowohl simuliert als auch auf einem FPGA ausgeführt werden kann.

```{raw} latex
\clearpage
```

## FPGA-Implementierung und Peripherieanbindung

Die physische Ausführung des Systems erfolgt auf dem in Abschnitt „Verwendete Hardwareplattform“ beschriebenen Pynq-Z1-Board. 
Der durch SpinalHDL und LiteX erzeugte Verilog-Code wird anschließend in Vivado synthetisiert, platziert und geroutet, sodass ein Bitstream entsteht, der auf die programmierbare Logik des Zynq-SoCs geladen werden kann. 
In der FPGA-Fabric laufen der konfigurierte VexRiscv-Prozessor und die LiteX-SoC-Struktur unter realen Timing-Bedingungen, was eine praxisnahe Bewertung der erzeugten Konfigurationen ermöglicht.

Für die Interaktion mit dem System wird ein UART-PMOD an eine PMOD-Schnittstelle des Pynq-Z1 angeschlossen. Über diese serielle Schnittstelle können Bootmeldungen, Debug-Ausgaben und Testergebnisse an einen Host-PC übertragen werden (RX). Gleichzeitig erlaubt der Sendekanal (TX) die Laufzeit-Interaktion mit dem Prozessor, etwa um Parameter zu ändern oder Testroutinen zu starten, während die Hardware läuft. Die Kombination aus grafischer Konfiguration, automatisierter Hardwaregenerierung, LiteX-SoC und UART-basierter Kommunikation bildet damit eine vollständige Umgebung zur systematischen Evaluierung unterschiedlicher Prozessorvarianten.

```{raw} latex
\clearpage
```

## Zusammenfassung des Workflows

Zusammenfassend lässt sich der Gesamtworkflow wie folgt beschreiben: 

- Die GUI definiert die Architekturvarianten und erzeugt die zugehörigen Konfigurationsdateien. 
- SpinalHDL und SBT übersetzen diese Konfigurationen in synthetisierbaren Verilog-Code. 
- LiteX erweitert den Prozessorkern zu einem vollständigen SoC, das anschließend sowohl simuliert als auch auf der FPGA-Plattform ausgeführt werden kann. 
- Vivado übernimmt die Synthese und Implementierung des Designs, während das Pynq-Z1-Board in Verbindung mit dem UART-PMOD als physische Testumgebung dient.

Auf dieser Basis können verschiedene Prozessorarchitekturen unter identischen Bedingungen verglichen und hinsichtlich ihrer Funktionalität und Effizienz bewertet werden.

---
