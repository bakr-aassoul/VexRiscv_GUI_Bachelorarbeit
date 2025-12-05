# Systemarchitektur
```{raw} latex
\large
```
In diesem Kapitel wird die Architektur des gesamten Entwicklungs- und           Evaluierungssystems beschrieben, das im Rahmen dieser Arbeit realisiert wurde. 
Dabei werden sowohl die GUI-basierte Konfigurationsumgebung, der Aufbau des VexRiscv-Prozessors, die Integration in ein LiteX-SoC als auch die Umsetzung auf einer FPGA-Plattform betrachtet. 
Ziel ist es, die Zusammenhänge zwischen den einzelnen Systemkomponenten darzustellen und zu erläutern, wie aus einer benutzerdefinierten Konfiguration ein lauffähiges Hardwaredesign entsteht, das auf dem FPGA getestet und analysiert werden kann.

Die Systemarchitektur dieser Arbeit basiert auf einem modularen Softcore-Design, das durch eine eigens entwickelte grafische Benutzeroberfläche zur Konfiguration des VexRiscv-Prozessors ergänzt wird. 
Ziel ist es, unterschiedliche Varianten des Prozessorkerns automatisiert zu erzeugen, in einer SoC-Umgebung einzubetten und schließlich auf einer FPGA-Plattform zu evaluieren. Die einzelnen Komponenten: GUI, Codegenerierung, SoC-Integration, Simulation und FPGA-Implementierung, greifen dabei eng ineinander und bilden einen durchgängigen Entwicklungs- und Evaluierungsworkflow.

```{raw} latex
\clearpage
```
---

```{raw} latex
\normalsize
```
## GUI-basierte Konfigurationsschicht


Den Ausgangspunkt der Systemarchitektur bildet die im Rahmen dieser Arbeit entwickelte GUI. 
Sie dient als abstrahierende Schicht, über die der VexRiscv-Prozessor konfiguriert werden kann, ohne direkt in den SpinalHDL-Quellcode eingreifen zu müssen. 
Der Benutzer wählt in der Oberfläche die gewünschten Architekturmerkmale und Plugins aus, etwa die Aktivierung von Multiplikations- und Divisionsmodulen, die Art des Shifters, die Ausgestaltung der Branch-Logik oder die Nutzung des CSR-Plugins.

Auf Basis dieser Auswahl generiert die GUI eine angepasste Top-Level-Definition des Prozessors (z. B. `VexRiscvTopFromGui.scala`) sowie optionale Konfigurationsdateien, die die aktuelle Architekturvariante beschreiben. 
Darüber hinaus ist die GUI mit der Build-Toolchain verknüpft: 

Sie kann den SBT-Buildprozess anstoßen, SpinalHDL ausführen und die Erzeugung von Verilog-Code automatisieren. 
Dadurch wird der Übergang von der architekturellen Beschreibung zu einer synthetisierbaren Hardwareimplementierung weitgehend entkoppelt und für den Benutzer stark vereinfacht.

```{raw} latex
\clearpage
```

## Prozessor- und SoC-Ebene

Die durch die GUI generierte Konfiguration beschreibt einen konkreten VexRiscv-Prozessorkern, der aus einer Kombination verschiedener Plugins besteht. 
Dazu gehören insbesondere Einheiten für Instruktions- und Datenzugriffe, die arithmetisch-logische Einheit, Shifter und Branch-Logik, das Registerfile, die Hazard-Behandlung sowie die Verwaltung der Control-and-Status-Register. 
Je nach gewählter Konfiguration können zusätzliche Funktionseinheiten wie Multiplikation und Division oder weitere Spezialfunktionen integriert werden. 
Auf diese Weise lässt sich der Umfang des Prozessors gezielt an den gewünschten Einsatzzweck anpassen von einer kompakten, ressourcenschonenden Ausführung bis hin zu einer leistungsfähigeren Variante mit erweitertem Befehlssatz.

Um den Prozessor in einem lauffähigen Gesamtsystem zu betreiben, wird er mithilfe von LiteX in eine System-on-Chip-Struktur eingebettet. 
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

Für die Interaktion mit dem System wird ein UART-PMOD an eine PMOD-Schnittstelle des Pynq-Z1 angeschlossen. 
Über diese serielle Schnittstelle können Bootmeldungen, Debug-Ausgaben und Testergebnisse an einen Host-PC übertragen werden. 
Gleichzeitig erlaubt sie das Einspielen kleiner Testprogramme oder Firmware, die auf dem VexRiscv-Prozessor ausgeführt werden. 
Die Kombination aus grafischer Konfiguration, automatisierter Hardwaregenerierung, LiteX-SoC, FPGA-Implementierung und UART-basierter Kommunikation bildet damit eine vollständige Umgebung zur systematischen Evaluierung unterschiedlicher Prozessorvarianten.

```{raw} latex
\clearpage
```

## Zusammenfassung des Workflows

Zusammenfassend lässt sich der Gesamtworkflow wie folgt beschreiben: 

Die GUI definiert die Architekturvarianten und erzeugt die zugehörigen Konfigurationsdateien. 
SpinalHDL und SBT übersetzen diese Konfigurationen in synthetisierbaren Verilog-Code. 

LiteX erweitert den Prozessorkern zu einem vollständigen SoC, das anschließend sowohl simuliert als auch auf der FPGA-Plattform ausgeführt werden kann. 

Vivado übernimmt die Synthese und Implementierung des Designs, während das Pynq-Z1-Board in Verbindung mit dem UART-PMOD als physische Testumgebung dient.

Auf dieser Basis können verschiedene Prozessorarchitekturen unter identischen Bedingungen verglichen und hinsichtlich ihrer Funktionalität und Effizienz bewertet werden.

---
