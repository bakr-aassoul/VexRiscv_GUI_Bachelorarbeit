# Theoretische Grundlagen

Dieses Kapitel beschreibt die theoretischen und technischen Grundlagen,  
auf denen die im Rahmen dieser Arbeit entwickelte GUI- und Simulationsumgebung basiert.  
Dazu gehören die **RISC-V-Architektur**, das **Hardware-Framework SpinalHDL**,  
sowie der **VexRiscv Prozessor** mit seinem modularen Plugin-System.  
Abschließend werden die genutzten Software-Tools für die Codegenerierung und Simulation erläutert.

---

## RISC-V-Architektur

**RISC-V** (Reduced Instruction Set Computer – Fifth Generation) ist eine offene,  
modulare und lizenzfreie **Befehlssatzarchitektur (ISA)**,  
die 2010 an der University of California, Berkeley, entwickelt wurde.  
Im Gegensatz zu proprietären Architekturen wie **x86** oder **ARM**  
kann RISC-V frei genutzt, angepasst und erweitert werden.  
Diese Offenheit macht RISC-V besonders interessant für Forschung, Lehre und industrielle Anwendungen.

Die Architektur folgt dem klassischen **RISC-Prinzip**:  
eine reduzierte Anzahl elementarer Instruktionen,  
eine einheitliche Befehlslänge (typischerweise 32 Bit)  
und ein einfacher, gleichmäßiger Befehlspfad.  
Dadurch wird ein effizienter Pipeline-Aufbau und eine klare Trennung  
zwischen **Fetch**, **Decode**, **Execute**, **Memory** und **Write-Back** ermöglicht.

Die Grundmenge des RISC-V-Befehlssatzes, **RV32I**,  
enthält alle Basisoperationen für arithmetische, logische und Speicherbefehle.  
Darauf aufbauend existieren optionale Erweiterungen,  
z. B. für Multiplikation und Division (M-Extension),  
atomare Operationen (A), Fließkomma (F/D),  
oder Vektorverarbeitung (V).  

Die Offenheit der Architektur erlaubt es, eigene Erweiterungen oder Spezialbefehle  
hinzuzufügen. Das ist ein Aspekt, der auch für die spätere **ALU-Erweiterung** dieser Arbeit relevant ist.

---

## SpinalHDL

**SpinalHDL** ist eine in **Scala** implementierte Hardwarebeschreibungssprache (HDL),  die einen modernen Ansatz zur Schaltungsbeschreibung bietet.  
Im Gegensatz zu klassischen HDLs wie **VHDL** oder **Verilog** verwendet SpinalHDL objektorientierte und funktionale Konzepte, um Hardwarestrukturen kompakt, wiederverwendbar und typensicher zu beschreiben.

### Vorteile von SpinalHDL:
- **Hohe Abstraktionsebene:** Durch die Integration in Scala können Parameter, Schleifen und logische Strukturen sehr flexibel formuliert werden.  
- **Weniger Code, gleiche Funktionalität:** SpinalHDL reduziert die Code-Menge im Vergleich zu VHDL/Verilog erheblich.  
- **Automatische Generierung:** SpinalHDL erzeugt synthetisierbaren Verilog- oder VHDL-Code,  
  der anschließend mit Standard-EDA-Tools (Vivado, Quartus, etc.) verarbeitet werden kann.  
- **Typensicherheit:** Fehler durch unpassende Signalbreiten oder Datentypen werden frühzeitig erkannt.  

SpinalHDL eignet sich besonders für parametrische Designs, die oft in Forschungsprojekten oder SoC-Entwicklungen verwendet werden.  
Ein bekanntes Beispiel hierfür ist der **VexRiscv-Prozessor**, der vollständig in SpinalHDL realisiert wurde.

---

## Der VexRiscv-Prozessor

Der **VexRiscv** ist ein in SpinalHDL geschriebener,  
**konfigurierbarer RISC-V-Prozessor**,  
der sich durch seine modulare Struktur und flexible Architektur auszeichnet.  
Er wird in zahlreichen Forschungs- und Lehrprojekten eingesetzt  
und dient als Referenzdesign für anpassbare RISC-V-Kerne.

Das Besondere am VexRiscv ist sein **Plugin-System**.  
Jede Funktionseinheit (z. B. ALU, Branch-Unit, CSR-Verwaltung oder Speicherinterface) wird als separates Plugin implementiert.  
Diese Plugins können beim Aufbau des Prozessors dynamisch hinzugefügt, entfernt oder parametrisiert werden.  

Beispiele für häufig verwendete Plugins sind:

| Plugin | Funktion |
|--------|-----------|
| **IBusSimplePlugin** | Steuert den Instruktionsbus (Fetch) |
| **DBusSimplePlugin** | Verantwortlich für Datenzugriffe (Load/Store) |
| **IntAluPlugin** | Führt arithmetische und logische Operationen aus |
| **CsrPlugin** | Verwaltung der Control- und Status-Register |
| **BranchPlugin** | Realisiert Sprungbefehle und Verzweigungen |
| **HazardSimplePlugin** | Erkennt Pipeline-Hazards und steuert Stalls |
| **MulPlugin / DivPlugin** | Erweiterungen für Multiplikation und Division |

Durch diese Architektur kann der VexRiscv je nach Anwendungsfall  
als **minimaler Kern** (nur Basis-Instruktionen)  
oder als **leistungsfähiger SoC-Prozessor** konfiguriert werden.  
Die in dieser Arbeit entwickelte GUI automatisiert genau diesen Konfigurationsprozess.

---

## Scala Build Tool (SBT)

Das **Scala Build Tool (SBT)** ist das Standard-Build-System für Scala-Projekte  
und wird in SpinalHDL verwendet, um Hardwaredesigns zu kompilieren und in Verilog umzuwandeln.  

Der typische Ablauf einer Codegenerierung lautet:

```bash
sbt "runMain vexriscv.demo.VexRiscvTopFromGui"
```
Dabei wird die Hauptklasse (VexRiscvTopFromGui.scala) ausgeführt, welche den VexRiscv mit den ausgewählten Plugins instanziiert.
Anschließend erzeugt SpinalHDL automatisch eine Verilog-Datei (VexRiscv.v), die später für Simulation oder FPGA-Synthese verwendet werden kann.

## Verilator

Verilator ist ein freies, leistungsstarkes Simulationswerkzeug, das Verilog-Code in optimierten C++-Code übersetzt und als ausführbares Programm simuliert.
Im Gegensatz zu klassischen eventbasierten Simulatoren arbeitet Verilator mit einem statischen Zeitschritt-Modell, was deutlich höhere Simulationsgeschwindigkeit ermöglicht.
In dieser Arbeit wird Verilator genutzt, um den mit SpinalHDL erzeugten Verilog-Code zu simulieren und die Signalverläufe des Prozessors aufzuzeichnen.
Die resultierenden Signale werden im Format trace.vcd gespeichert und anschließend mit GTKWave visualisiert.

## GTKWave

GTKWave ist ein Open-Source-Tool zur Visualisierung digitaler Signalverläufe.
Es ermöglicht das Anzeigen, Zoomen und Analysieren von VCD-Dateien (Value Change Dump), die von Simulationsprogrammen wie Verilator erzeugt werden.

Über GTKWave können alle internen Signale des Prozessors beobachtet werden, z. B. Takt, Reset, Program Counter, ALU-Eingänge und Bus-Daten.
Dieses Werkzeug ist ein zentraler Bestandteil des Verifikationsprozesses, da es die visuelle Kontrolle des CPU-Verhaltens ermöglicht und somit Fehler und Timing-Probleme direkt sichtbar macht.

## Zusammenfassung

Die in diesem Kapitel vorgestellten Grundlagen bilden die theoretische Basis für die in dieser Arbeit entwickelte Umgebung. 
Die Kombination aus RISC-V, SpinalHDL und VexRiscv ermöglicht einen flexiblen, modularen und offenen Ansatz zur Prozessorentwicklung.
Die Tools SBT, Verilator und GTKWave bilden die technische Infrastruktur für die Automatisierung, Simulation und Verifikation des Designs, wie sie in den folgenden Kapiteln beschrieben wird.
