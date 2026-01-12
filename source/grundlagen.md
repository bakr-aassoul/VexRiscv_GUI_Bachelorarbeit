# Theoretische Grundlagen


```{raw} latex
\large
```
   Dieses Kapitel beschreibt die theoretischen und technischen Grundlagen, auf
   denen die im Rahmen dieser Arbeit entwickelte GUI- und Simulationsumgebung
   basiert.  
   Dazu gehören die **RISC-V-Architektur**,das Konzept der **Domain-Specific           Architectures**, das **Hardware-Framework SpinalHDL**, sowie der **VexRiscv         Prozessor** mit seinem modularen Plugin-System.  
   Abschließend werden die genutzten Software-Tools für die Codegenerierung und
   Simulation erläutert.

```{raw} latex
\clearpage
```

```{raw} latex
\normalsize
```
## RISC-V

**RISC-V** (Reduced Instruction Set Computer – Fifth Generation) ist eine offene, modulare und lizenzfreie **Befehlssatzarchitektur (ISA)**,  die 2010 an der University of California, Berkeley, entwickelt wurde {cite}`RISCV19`.  

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
Die Grundmenge des RISC-V-Befehlssatzes, **RV32I**, enthält alle Basisoperationen für arithmetische, logische und Speicherbefehle {cite}`RISCV19`.  
Darauf aufbauend existieren optionale Erweiterungen {cite}`PH17a`, z.B:

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

```{figure} images/Abb1.png
:name: fig:riscv_formats
:width: 100%
:align: center

Übersicht der RISC-V Basis-Instruktionsformate (RV32I)
```
{cite}`RISCV19`

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

```{raw} latex
\clearpage
```
### Benutzerdefinierte Erweiterungen (Custom Extensions)

Eine Besonderheit der RISC-V-Spezifikation ist die explizite Reservierung von Opcodes für proprietäre oder experimentelle Erweiterungen. 
Im 32-Bit-Befehlssatz sind vier Hauptbereiche (Custom-0 bis Custom-3) definiert, die nicht durch Standardinstruktionen belegt werden. 
Dies ermöglicht es Chip-Designern, spezialisierte Hardware-Beschleuniger (Domain-Specific Accelerators) direkt in die Pipeline zu integrieren und über eigene Opcodes anzusprechen, ohne die Kompatibilität zum Basis-Standard zu verletzen.
Diese Offenheit ist die theoretische Grundlage für die in dieser Arbeit entwickelte Generierung von Custom ALUs.



## Domain-Specific Architectures (DSA)

Die Grenzen der Skalierung klassischer General-Purpose-Prozessoren (Moore’s Law) führen zunehmend zum Einsatz von Domain-Specific Architectures (DSA) {cite}`HP17b`
. Hierbei wird die Hardware-Architektur an die spezifischen Anforderungen einer Anwendungsdomäne (z. B. Signalverarbeitung, Kryptografie oder KI) angepasst.

Durch die Implementierung spezialisierter Rechenwerke (Custom Instructions), die häufig benötigte komplexe Operationen in Hardware abbilden, lassen sich signifikante Effizienzgewinne gegenüber einer reinen Softwarelösung erzielen. Der VexRiscv-Prozessor in Kombination mit einem FPGA bietet eine ideale Plattform für das Rapid Prototyping solcher heterogenen Architekturen.

```{raw} latex
\clearpage
```
## SpinalHDL

SpinalHDL ist eine moderne HDL (Hardwarebeschreibungssprache), die im Jahr 2014 eingeführt wurde und als Domain-Specific Language (DSL) in Scala implementiert ist {cite}`PP19`. Sie bietet die Möglichkeit, digitale Schaltungen zu entwerfen. 
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

Der **VexRiscv** ist ein in SpinalHDL geschriebener, **konfigurierbarer RISC-V-Prozessor**, der sich durch seine modulare Struktur und flexible Architektur auszeichnet {cite}`Pap24a`.  
Er wird in zahlreichen Forschungs- und Lehrprojekten eingesetzt und dient als Referenzdesign für anpassbare RISC-V-Kerne.
Das Besondere am VexRiscv ist sein **Plugin-System**. Jede Funktionseinheit (z. B. ALU, Branch-Unit, CSR-Verwaltung oder Speicherinterface) wird als separates Plugin implementiert.  
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

```{raw} latex
\clearpage
```
### Pipeline-Injection und Decoder-Service

Die Modularität des VexRiscv basiert technisch auf dem *Plugin-Interface* von SpinalHDL. Ein Plugin ist dabei nicht nur ein abgeschlossenes Modul, sondern Code, der sich während der Hardware-Generierung in verschiedene Stufen der CPU-Pipeline (Fetch, Decode, Execute, Memory, WriteBack) **einhängen** kann.

Besonders relevant für Erweiterungen ist der DecoderService. Plugins können diesem Service spezifische Bitmuster (Instruktions-Opcodes) übergeben. Erkennt der Decoder zur Laufzeit dieses Muster, aktiviert er automatisch die entsprechenden Steuersignale für das Plugin in der Execute-Stufe. 
Dieser Mechanismus erlaubt es, neue Recheneinheiten (ALUs) hinzuzufügen, ohne den Kern-Decoder manuell umschreiben zu müssen. Die entwickelte GUI nutzt genau diesen Mechanismus zur automatischen Code-Generierung.

```{figure} images/Abb2.png
:name: fig:vex_pipeline
:width: 120%
:align: center

Die VexRiscv 5-Stufen-Pipeline und Plugin Injection
```

Die in dieser Arbeit entwickelte GUI automatisiert genau diesen Konfigurationsprozess.
Anstatt die einzelnen Plugins manuell im Scala/SpinalHDL-Code zusammenzustellen, ermöglicht die Oberfläche eine intuitive Auswahl der gewünschten Komponenten, beispielsweise ALU-Erweiterungen, Branch-Units, Speicher-Interfaces oder CSR-Optionen.
Die GUI generiert anschließend den vollständigen VexRiscvTopFromGui.scala bzw. die entsprechende Verilog-Datei, sodass ein reproduzierbarer und fehlerfreier Build-Prozess gewährleistet ist.
Damit wird die inhärente Modularität des VexRiscv nicht nur sichtbar, sondern auch praktisch nutzbar: Entwicklerinnen und Entwickler können unterschiedliche Mikroarchitekturen schnell vergleichen, testen und an spezifische Anforderungen anpassen.

```{raw} latex
\clearpage
```

## Entwicklungs- und Simulationswerkzeuge

Im Rahmen dieser Arbeit kamen mehrere Tools zum Einsatz, die für den Build, Simulation und Analyseprozess eines konfigurierbaren VexRiscv-Kerns notwendig sind. Diese Werkzeuge bilden die Grundlage für den Entwicklungsworkflow der GUI sowie für die Validierung des generierten Prozessordesigns.

```{figure} images/Abb3.png
:name: fig:toolchain_flow
:width: 100%
:align: center

Der SpinalHDL Toolchain-Workflow
```

### Scala Build Tool (SBT)

Das **Scala Build Tool (SBT)** ist das Standard-Buildsystem für Scala-Projekte. 
Es wird genutzt, um den SpinalHDL-Code zu kompilieren und den VexRiscv-Codegenerator auszuführen, der letztlich den Verilog-Code erzeugt.

### Verilator

**Verilator** ist ein freies, leistungsstarkes Simulationswerkzeug, das Verilog-Code in optimierten *C++*-Code übersetzt und als ausführbares Programm simuliert {cite}`Sny24`.
Im Gegensatz zu klassischen eventbasierten Simulatoren arbeitet Verilator mit einem statischen Zeitschritt-Modell, was deutlich höhere Simulationsgeschwindigkeit ermöglicht.
In dieser Arbeit wird Verilator genutzt, um den mit SpinalHDL erzeugten Verilog-Code zu simulieren und Korrektheitstests in Kombination mit LiteX oder eigenständigen Testbenches auszuführen.

### GTKWave

GTKWave ist ein Open-Source-Tool zur Visualisierung digitaler Signalverläufe.
Es ermöglicht das Anzeigen, Zoomen und Analysieren von VCD-Dateien (Value Change Dump), die von Simulationsprogrammen wie Verilator erzeugt werden.

Über GTKWave können alle internen Signale des Prozessors beobachtet werden, z. B. Takt, Reset, Program Counter, ALU-Eingänge und Bus-Daten.
Dieses Werkzeug ist ein zentraler Bestandteil des Verifikationsprozesses, da es die visuelle Kontrolle des CPU-Verhaltens ermöglicht und somit Fehler und Timing-Probleme direkt sichtbar macht
Die Kombination aus Verilator und GTKWave bildet somit ein vollständiges Werkzeugpaar für die funktionale Validierung der Hardware.

### LiteX
LiteX ist ein modulares Framework zur Erstellung von System-on-Chip-(SoC) Architekturen auf FPGAs {cite}`Ker24`. Es abstrahiert viele der typischen Aufgaben der SoC-Integration (Bus-Infrastruktur, Peripherieanbindung, Speichercontroller oder Simulation) und ermöglicht dadurch einen schnellen Aufbau komplexer Systeme.

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


**Tabelle 2.1: Übersicht der verwendeten Software-Versionen und Bibliotheken**
| Software / Komponente    | Version   | Verwendungszweck                     |
| :----------------------- | :-------- | :----------------------------------- |
| **SBT** | 1.6.0     | Build-System für Scala               |
| **Scala** | 2.12.18   | Programmiersprache für SpinalHDL     |
| **SpinalHDL (Core/Lib)** | 1.12.0    | Hardwarebeschreibungssprache         |
| **VexRiscv** | 2.0.0     | RISC-V Prozessorkern (Basis)         |
| **Verilator** | 4.038     | Simulation und C++ Transpilierung    |
| **LiteX** | 10c52e742 | SoC-Builder und BIOS (Git SHA1)      |
| **Xilinx Vivado** | 2023.1    | Synthese und Implementierung         |
| **Python** | 3.10.12   | Laufzeitumgebung für die GUI         |
| **GTKWave** | 3.3.104   | Visualisierung der Signalverläufe    |
| **sbt-bloop** | 2.0.10    | Build Server Integration             |
| **ScalaTest** | 3.2.17    | Unit-Testing Framework               |

```{raw} latex
\clearpage
```

# Verwendete Hardwareplattform
```{raw} latex
\large
```


Für die praktische Evaluierung des konfigurierbaren VexRiscv-Prozessors wurde eine FPGA-basierte Entwicklungsumgebung eingesetzt. 
Diese ermöglicht sowohl die Überprüfung der synthetisierten Hardware als auch die Interaktion mit externen Peripheriegeräten. 
Auf dieser Hardwarebasis können die durch die GUI erzeugten Konfigurationen in realen Betriebsbedingungen getestet, verglichen und hinsichtlich ihrer Funktionalität verifiziert werden.

```{raw} latex
\clearpage
```


```{raw} latex
\normalsize
```
## Pynq-Z1 FPGA-Board

Das Pynq-Z1 ist ein kostengünstiges, aber leistungsfähiges FPGA-Board, das auf dem Xilinx Zynq-7000 SoC (XC7Z020) basiert {cite}`Dig24`.

```{figure} images/Abb4.png
:name: fig:pynq_board
:width: 70%
:align: center

Das verwendete Entwicklungsboard Digilent PYNQ-Z1 [Digilent PYNQ-Z1](https://digilent.com/reference/programmable-logic/pynq-z1/start)
```

### Zynq-Architektur (PS und PL)
Der Zynq-Chip vereint zwei Welten auf einem Die {cite}`Xil21`:

- **Processing System (PS):** Ein Dual-Core ARM Cortex-A9 Prozessor, der typischerweise ein Betriebssystem (Linux) ausführt.
- **Programmable Logic (PL):** Ein Artix-7 basierter FPGA-Bereich, in dem benutzerdefinierte digitale Schaltungen realisiert werden können.

Für diese Arbeit ist primär die Programmable Logic (PL) von Bedeutung. Der generierte VexRiscv-Prozessor wird als *Soft-Core* vollständig in diesen FPGA-Bereich synthetisiert.
Das PS dient dabei lediglich zur Stromversorgung und Konfiguration oder wird ( je nach LiteX-Setup ) komplett umgangen.

```{figure} images/Abb5.png
:name: fig:zynq_arch
:width: 90%
:align: center

Architektur des Zynq-7000 SoC (PS und PL)
```

```{raw} latex
\clearpage
```
### Verfügbare Ressourcen

Der XC7Z020-Chip bietet ausreichende Ressourcen, um auch komplexe VexRiscv-Konfigurationen (z. B. mit Caches, Multipliern und Custom ALUs) zu implementieren. Die wichtigsten Kenndaten sind:

- Logic Cells: 85.000
- Look-Up Tables (LUTs): 53.200
- Flip-Flops: 106.400
- Block RAM: 4,9 Mbit (wichtig für den internen Speicher des VexRiscv)
- DSP Slices: 220 (wichtig für mathematische Custom Instructions)

Diese Ressourcen bieten genügend Spielraum, um neben dem Standard-Prozessor auch umfangreiche benutzerdefinierte Logik-Erweiterungen zu platzieren, ohne in Platzprobleme (Fitting Issues) zu geraten

## Peripherieanbindung (UART-PMOD)

Die Kommunikation zwischen dem VexRiscv-Softcore und dem Entwickler-PC erfolgt über eine serielle Schnittstelle. Da die internen UART-Pins des Pynq-Boards hardwareseitig fest mit dem ARM-Prozessor (PS) verbunden sind, wurde für den VexRiscv ein dediziertes UART-PMOD-Modul verwendet.

Dieses Modul wird an einen der PMOD-Ports (Peripheral Module Interface) des Boards angeschlossen und direkt mit den generierten IO-Pins des VexRiscv in der Programmable Logic (PL) verdrahtet.

**Funktion im System:**

- Terminal-Ausgabe (RX): Nach dem Laden des Bitstreams über Vivado dient das Modul als Standard-Ausgabekanal (stdout). Hier werden Systemmeldungen, Ergebnisse der Custom-ALU-Berechnungen oder *printf*-Ausgaben der C-Software angezeigt.
- Benutzer-Interaktion (TX): Über die Sende-Leitung können zur Laufzeit Eingaben an den Prozessor gesendet werden, um beispielsweise verschiedene Testmodi zu starten oder Parameter für die Custom Instructions dynamisch zu verändern.
- Debugging: Das Terminal ermöglicht eine direkte Überwachung des Programmablaufs in Echtzeit, was die Fehlersuche bei der Integration neuer Instruktionen erheblich erleichtert.

Die Verwendung des externen PMODs gewährleistet somit eine saubere physikalische Trennung: Die Konfiguration des FPGAs erfolgt über JTAG (Vivado), während die operative Kommunikation mit dem Soft-Core exklusiv über den UART-PMOD läuft.
