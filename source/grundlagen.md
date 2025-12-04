# Theoretische Grundlagen


.. raw:: latex

   {
   \Large 
   Dieses Kapitel beschreibt die theoretischen und technischen Grundlagen, auf
   denen die im Rahmen dieser Arbeit entwickelte GUI- und Simulationsumgebung
   basiert.  
   Dazu gehören die **RISC-V-Architektur**, das **Hardware-Framework SpinalHDL**,
   sowie der **VexRiscv Prozessor** mit seinem modularen Plugin-System.  
   Abschließend werden die genutzten Software-Tools für die Codegenerierung und
   Simulation erläutert.
   }
   
```{raw} latex
\clearpage
```
---

## RISC-V

**RISC-V** (Reduced Instruction Set Computer – Fifth Generation) ist eine offene, modulare und lizenzfreie **Befehlssatzarchitektur (ISA)**,  die 2010 an der University of California, Berkeley, entwickelt wurde.  

Im Gegensatz zu proprietären Architekturen wie **x86** oder **ARM** kann RISC-V frei genutzt, angepasst und erweitert werden.  

Diese Offenheit macht RISC-V besonders interessant für Forschung, Lehre und industrielle Anwendungen.

### RISC-V-Architektur

Die Architektur folgt dem klassischen **RISC-Prinzip**, welches auf Einfachheit, Effizienz und deterministische Ausführungswege abzielt.
Typische Eigenschaften sind:

- eine reduzierte Anzahl elementarer Instruktionen,  
- eine einheitliche Befehlslänge (typischerweise 32 Bit),
- ein einfacher, gleichmäßiger Befehlspfad.
   
Dadurch wird ein effizienter Pipeline-Aufbau und eine klare Trennung zwischen **Fetch**, **Decode**, **Execute**, **Memory** und **Write-Back** ermöglicht.

Durch die geringe Komplexität der Basisinstruktionen lassen sich RISC-V-Prozessoren in sehr unterschiedlichen Leistungs- und Energieklassen realisieren von kleinen Mikrocontrollern bis hin zu High-Performance-Kernen.

Die Grundmenge des RISC-V-Befehlssatzes, **RV32I**,  
enthält alle Basisoperationen für arithmetische, logische und Speicherbefehle.  
Darauf aufbauend existieren optionale Erweiterungen,z. B:

- Multiplikation und Division (M-Extension),  
- Atomare Operationen (A),
- Fließkomma (F/D),
- Vektorverarbeitung (V).  


Die Offenheit der Architektur erlaubt es, eigene Erweiterungen oder Spezialbefehle  
hinzuzufügen. Das ist ein Aspekt, ohne die Kompatibilität zum Standard zu verlieren.

```{raw} latex
\clearpage
```

### ISA-Überblick

Die RISC-V Instruction Set Architecture (ISA) ist hierarchisch und modular aufgebaut.
Sie besteht aus:

1. **Basis-ISA (RV32I, RV64I, RV128I)**
   - Definiert die Register (32 allgemeine Register, PC),
   - Instruktionsformate (R-, I-, S-, B-, U- und J-Format),
   - elementare Operationen wie ADD, SUB, AND, OR, LW, SW, BEQ, JAL usw.
   Die Basis-ISA ist bewusst klein gehalten, um Implementierungen möglichst einfach
   und energieeffizient zu gestalten.
2. **Standarderweiterungen (M, A, F, D, C, V usw.)**
   - Jede Erweiterung ist vollständig optional, wodurch sich RISC-V besser an
   Anwendungsfälle anpassen lässt als viele andere ISAs.
   -Kombinationen der Basis-ISA mit Erweiterungen werden als Variants bezeichnet,
   z. B. RV32IMC.
3. **Privilegierte Architektur**
   - RISC-V definiert mehrere Ausführungsmodi (Machine, Supervisor, User) und eine
   Reihe von Control and Status Registers (CSRs).
   - Diese sind für Interrupt-Handling, Exceptions, Speicherverwaltung und
   Betriebssystemunterstützung zuständig.
   - Der modulare Aufbau ermöglicht Implementierungen mit oder ohne
   Betriebssystem, von Bare-Metal-Systemen bis hin zu Linux-fähigen SoCs.

---
```{raw} latex
\clearpage
```

## SpinalHDL

SpinalHDL ist eine moderne HDL (Hardwarebeschreibungssprache), die im Jahr 2014 eingeführt wurde und als Domain-Specific Language (DSL) in Scala implementiert ist. Sie bietet die Möglichkeit, digitale Schaltungen zu entwerfen. 
Danach können diese als Verilog oder VHDL-Code generiert werden, der einsatzbereit und mit FPGA sowie ASIC-Toolchains kompatibel ist.


**Vorteile von SpinalHDL:** 

- **Hohe Abstraktionsebene:** Durch die Integration in Scala können Parameter, Schleifen und logische Strukturen sehr flexibel formuliert werden.  
- **Weniger Code, gleiche Funktionalität:** SpinalHDL reduziert die Code-Menge im Vergleich zu VHDL/Verilog erheblich.  
- **Automatische Generierung:** SpinalHDL erzeugt synthetisierbaren Verilog- oder VHDL-Code,  
  der anschließend mit Standard-EDA-Tools (Vivado, Quartus, etc.) verarbeitet werden kann.  
- **Typensicherheit:** Fehler durch unpassende Signalbreiten oder Datentypen werden frühzeitig erkannt.



SpinalHDL eignet sich besonders für parametrische Designs, die oft in Forschungsprojekten oder SoC-Entwicklungen verwendet werden.  
Ein bekanntes Beispiel hierfür ist der **VexRiscv-Prozessor**, der vollständig in SpinalHDL realisiert wurde.

```{raw} latex
\clearpage
```

## Der VexRiscv-Prozessor

Der **VexRiscv** ist ein in SpinalHDL geschriebener, **konfigurierbarer RISC-V-Prozessor**, der sich durch seine modulare Struktur und flexible Architektur auszeichnet.  
Er wird in zahlreichen Forschungs- und Lehrprojekten eingesetzt und dient als Referenzdesign für anpassbare RISC-V-Kerne.

Das Besondere am VexRiscv ist sein **Plugin-System**.  
Jede Funktionseinheit (z. B. ALU, Branch-Unit, CSR-Verwaltung oder Speicherinterface) wird als separates Plugin implementiert.  
Diese Plugins können beim Aufbau des Prozessors dynamisch hinzugefügt, entfernt oder parametrisiert werden.  

### Plugins im VexRiscv

Durch das Plugin-System lässt sich der VexRiscv gezielt an unterschiedliche Anforderungen anpassen, von sehr kleinen, ressourcenschonenden Implementierungen bis hin zu leistungsfähigeren Varianten mit Cache, MMU oder Debug-Schnittstellen.
Jedes Plugin erweitert den Kern um klar abgegrenzte Funktionalität, ohne die Grundstruktur des Prozessors zu verändern. Somit entsteht eine hochgradig modulare Mikroarchitektur, deren Umfang und Fähigkeiten präzise steuerbar sind.

In dieser Arbeit wird eine Konfiguration verwendet, die sich auf die Kernelemente eines klassischen RV32I/M-Prozessors konzentriert. Die folgenden Plugins bilden dabei die funktionale Grundlage des eingesetzten Prozessors:


- IBusSimplePlugin / DBusSimplePlugin: einfache Instruktions- und Datenbus
	Schnittstellen für Speicherzugriffe ohne Cache.
- DecoderSimplePlugin: steuert das Instruktions-Decode und ordnet Instruktionen
	den jeweiligen Funktionseinheiten zu.
- RegFilePlugin: implementiert das Registerfile mit Lese-/Schreibzugriffen.
- SrcPlugin: wählt und liefert die Operanden für ALU, Branch- und Shifter
	Einheiten.
- IntAluPlugin: realisiert arithmetische und logische Grundoperationen.
- LightShifterPlugin: implementiert rechte/links Shifts mit geringer
	Ressourcenkomplexität.
- HazardSimplePlugin: behandelt Pipeline-Hazards und stellt
	Forwarding/Bypassing sicher.
- BranchPlugin: führt Sprungberechnungen und einfache Branch-Vorhersage durch.
- CsrPlugin: stellt die Verwaltung der Control-and-Status-Register (CSRs)
	bereit und bildet den Kern der privilegierten Architektur.
- MulPlugin / DivPlugin: implementieren Multiplikation und Division und
	erweitern damit die Basis-ISA um die M-Extension.



Diese Plugin-Auswahl entspricht einem kompakten, aber voll funktionsfähigen Single-Issue-RISC-V-Kern, der sich besonders für eingebettete Systeme und FPGA-basierte Demonstratoren eignet.
Da keine Cache- oder MMU-Plugins integriert sind, erfolgt jeder Speicherzugriff direkt über die einfachen Bus-Interfaces. Dies vereinfacht sowohl die Hardwarestruktur als auch die spätere Integration in LiteX.

Neben dieser minimalistischen Variante existieren in der VexRiscv-Ökosystem zahlreiche optionale Plugins, wie sie etwa in LiteX-SoCs eingesetzt werden können. Beispiele hierfür sind:


- IBusCachedPlugin / DBusCachedPlugin: Instruktions- und Datencaches für höhere
  Leistung.
- MmuPlugin + StaticMemoryTranslatorPlugin: Unterstützung für virtuelle
  Speicherverwaltung und Betriebssysteme wie Linux.
- PmpPlugin: Physical Memory Protection gemäß der RISC-V-Spezifikation.
- FullBarrelShifterPlugin: hardwareseitig schneller Shifter.
- MulDivIterativePlugin: iterative Implementierung für ressourcenschonende
  Multiplikation/Division.
- ExternalInterruptArrayPlugin: Unterstützung externer Interruptquellen.
- DebugPlugin: JTAG-Debugging und Hardware-Breakpoints.
- CfuPlugin: Custom Function Units für benutzerdefinierte Instruktionen.
- YamlPlugin: generiert Metadaten zur Kernkonfiguration.



Diese Vielfalt verdeutlicht die Stärke des VexRiscv-Ansatzes:
Der Prozessorkern ist kein statisches Design, sondern ein baukastenartiges Framework, das Entwicklungs- und Forschungsprojekte ermöglicht, in denen gezielt einzelne Architekturmerkmale untersucht oder erweitert werden können.
Durch diese Architektur kann der VexRiscv je nach Anwendungsfall als **minimaler Kern** (nur Basis-Instruktionen, keine Pipeline-Optimierungen, kein Multiplikations-/Divisionsmodul) oder als **leistungsfähiger SoC-Prozessor** mit Cache-Hierarchie, MMU, Interrupt-Controller und Debug-Schnittstelle konfiguriert werden.  



Die in dieser Arbeit entwickelte GUI automatisiert genau diesen Konfigurationsprozess.
Anstatt die einzelnen Plugins manuell im Scala/SpinalHDL-Code zusammenzustellen, ermöglicht die Oberfläche eine intuitive Auswahl der gewünschten Komponenten, beispielsweise ALU-Erweiterungen, Branch-Units, Speicher-Interfaces oder CSR-Optionen.
Die GUI generiert anschließend den vollständigen VexRiscvTopFromGui.scala bzw. die entsprechende Verilog-Datei, sodass ein reproduzierbarer und fehlerfreier Build-Prozess gewährleistet ist.
Damit wird die inhärente Modularität des VexRiscv nicht nur sichtbar, sondern auch praktisch nutzbar: Entwicklerinnen und Entwickler können unterschiedliche Mikroarchitekturen schnell vergleichen, testen und an spezifische Anforderungen anpassen.

```{raw} latex
\clearpage
```

## Entwicklungs- und Simulationswerkzeuge

Im Rahmen dieser Arbeit kamen mehrere Tools zum Einsatz, die für den Build, Simulation und Analyseprozess eines konfigurierbaren VexRiscv-Kerns notwendig sind. Diese Werkzeuge bilden die Grundlage für den Entwicklungsworkflow der GUI sowie für die Validierung des generierten Prozessordesigns.

### Scala Build Tool (SBT)

Das **Scala Build Tool (SBT)** ist das Standard-Buildsystem für Scala-Projekte und wird von SpinalHDL genutzt, um:
- den SpinalHDL-Code zu kompilieren,
- Plugin-Konfigurationen zu laden,
- den VexRiscv-Codegenerator auszuführen,
- Verilog- oder VHDL-Dateien zu erzeugen.

### Verilator

Verilator ist ein freies, leistungsstarkes Simulationswerkzeug, das Verilog-Code in optimierten C++-Code übersetzt und als ausführbares Programm simuliert.
Im Gegensatz zu klassischen eventbasierten Simulatoren arbeitet Verilator mit einem statischen Zeitschritt-Modell, was deutlich höhere Simulationsgeschwindigkeit ermöglicht.
In dieser Arbeit wird Verilator genutzt, um den mit SpinalHDL erzeugten Verilog-Code zu simulieren und Korrektheitstests in Kombination mit LiteX oder eigenständigen Testbenches auszuführen.

### GTKWave

GTKWave ist ein Open-Source-Tool zur Visualisierung digitaler Signalverläufe.
Es ermöglicht das Anzeigen, Zoomen und Analysieren von VCD-Dateien (Value Change Dump), die von Simulationsprogrammen wie Verilator erzeugt werden.

Über GTKWave können alle internen Signale des Prozessors beobachtet werden, z. B. Takt, Reset, Program Counter, ALU-Eingänge und Bus-Daten.
Dieses Werkzeug ist ein zentraler Bestandteil des Verifikationsprozesses, da es die visuelle Kontrolle des CPU-Verhaltens ermöglicht und somit Fehler und Timing-Probleme direkt sichtbar macht
Die Kombination aus Verilator und GTKWave bildet somit ein vollständiges Werkzeugpaar für die funktionale Validierung der Hardware.

```{raw} latex
\clearpage
```
### LiteX
LiteX ist ein modulares Framework zur Erstellung von System-on-Chip-(SoC) Architekturen auf FPGAs. Es abstrahiert viele der typischen Aufgaben der SoC-Integration (Bus-Infrastruktur, Peripherieanbindung, Speichercontroller oder Simulation) und ermöglicht dadurch einen schnellen Aufbau komplexer Systeme.

Im Kontext dieser Arbeit erfüllt LiteX zwei zentrale Funktionen:
- **Integration des VexRiscv-Prozessors:**
  LiteX stellt fertige Infrastrukturmodule bereit (Wishbone/AXI-Bus,
  Speicherinterfaces, UART, Timer usw.), über die der erzeugte VexRiscv-Core
  nahtlos in ein vollständiges SoC eingebettet werden kann.
- **Simulation und Testing:**
  LiteX kann automatisch Simulationen mit Verilator erzeugen, wodurch ein
  vollständiges SoC (inklusive CPU, Speicher und Peripherie) getestet werden kann.
  Dies ist besonders wertvoll, um zu prüfen, ob der neu generierte Prozessor (mit
  der GUI-Konfiguration) korrekt mit dem restlichen System interagiert.
  
### Vivado

Xilinx Vivado ist die proprietäre Toolchain zur Synthese, Analyse und Implementierung digitaler Schaltungen auf Xilinx-FPGAs.
Während SpinalHDL und Verilator primär für die funktionale Simulation genutzt werden, übernimmt Vivado die hardwareseitige Umsetzung der erzeugten Verilog-Dateien.

Die wichtigsten Aufgaben von Vivado in dieser Arbeit sind:
- **Synthese:**
  Der generierte VexRiscv-Core wird in eine FPGA-Netzliste übersetzt. Dabei werden
  Timing, Logikressourcen und Pipeline-Strukturen optimiert.
- **Implementierung:**
  Platzierung (Placement) und Verdrahtung (Routing) der Schaltung auf dem FPGA
  Gewebe. Vivado stellt sicher, dass die Designvorgaben (z. B. maximale
  Taktfrequenz) eingehalten werden.
- **Bitstream-Erzeugung:**
  Aus der finalen Implementierung wird die Bitstream-Datei erstellt, die
  anschließend auf ein Board wie das Pynq-Z1 oder Artix-7-Boards geladen werden
  kann.
- **Debugging:**
  Tools wie Vivado Logic Analyzer (ILA) können genutzt werden, um interne Signale
  auf dem FPGA in Echtzeit zu beobachten – hilfreich für tiefergehende Tests des
  Prozessorkerns.

Vivado bildet damit den letzten Schritt im Hardware-Workflow:
Nach Konfiguration (GUI), Code-Generierung (SpinalHDL/SBT) und Simulation (Verilator/GTKWave) erfolgt über Vivado die physische Implementierung auf dem FPGA.

# Verwendete Hardwareplattform

Für die praktische Evaluierung des konfigurierbaren VexRiscv-Prozessors wurde eine FPGA-basierte Entwicklungsumgebung eingesetzt. Diese ermöglicht sowohl die Überprüfung der synthetisierten Hardware als auch die Interaktion mit externen Peripheriegeräten.

## Pynq-Z1 FPGA-Board

Das Pynq-Z1 ist ein kostengünstiges, aber leistungsfähiges FPGA-Board, das auf dem Xilinx Zynq-7000 SoC (XC7Z020) basiert.
Der Chip kombiniert:

- einen Dual-Core ARM Cortex-A9 (Processing System, PS)
- ein Artix-7 FPGA-Fabric (Programmable Logic, PL)

Damit eignet sich das Board sowohl für klassische FPGA-Designs als auch für heterogene Systeme, in denen Software und Hardware eng miteinander interagieren.

Für diese Arbeit wurde das Pynq-Z1 genutzt, um den durch die GUI generierten VexRiscv-Core in der programmierbaren Logik (PL) zu implementieren.
Das Board bietet dafür:

- ausreichend logische Ressourcen für RISC-V-Kerne,
- mehrere PMOD-Schnittstellen für Peripherie,
- integrierte Taktquellen,
- UART, LEDs, Schalter und Speicher.

Die Implementierung auf einem realen FPGA ermöglicht es, den generierten Kern nicht nur zu simulieren, sondern auch unter realen Betriebsbedingungen zu testen.

## UART-PMOD Modul

Für die serielle Kommunikation mit dem Prozessor wurde ein UART-PMOD verwendet.
Dieses Modul wird typischerweise über eine der PMOD-Schnittstellen des Pynq-Z1 angeschlossen und stellt einen einfach nutzbaren UART-Transceiver bereit.

**Hauptfunktionen:**

- serielle Übertragung über RX/TX-Leitungen,
- Kommunikation mit dem Host-PC (z. B. über USB-Seriell-Adapter),
- Debugging und Konsolenausgabe des RISC-V-Kerns,
- Übertragung kleiner Testprogramme oder Statusmeldungen.

In Kombination mit LiteX oder einer eigenen SoC-Top-Level-Beschreibung dient der UART-PMOD als Standard-Interface, um den generierten Kern in Betrieb zu nehmen und sein Verhalten zu beobachten.
