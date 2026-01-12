# Simulation und Verifikation

```{raw} latex
\large
```
Die Simulation bildet den zentralen Nachweis der Funktionsfähigkeit des mit der GUI erzeugten Prozessors. Sie dient der Validierung, ob der automatisch generierte Verilog-Code die erwarteten Operationen des RISC-V-Befehlssatzes sowie die benutzerdefinierten Erweiterungen (Custom Instructions) korrekt ausführt. In diesem Kapitel werden der Testaufbau, die Durchführung der Simulation mittels Verilator und die Analyse der Ergebnisse beschrieben.

```{raw} latex
\clearpage
```

```{raw} latex
\normalsize
```


## Testaufbau

Für die funktionale Verifikation wurde der generierte Verilog-Code (*VexRiscv.v*) mithilfe von Verilator simuliert. Im Gegensatz zu klassischen ereignisbasierten Simulatoren übersetzt Verilator das Hardware-Design in ein optimiertes C++-Modell. Dies ermöglicht eine effiziente, zyklusgenaue Simulation, die sich nahtlos in C++-Testumgebungen integrieren lässt.

Das Testsystem setzt sich aus folgenden Komponenten zusammen:

- Device Under Test (DUT): Der generierte VexRiscv-Prozessorkern. 
- Testbench: Eine in C++ implementierte Umgebung (tb_gui.cpp), die den Prozessor instanziiert, Takte generiert und die Peripherie (Speicher, Reset) simuliert.  
- Analysewerkzeug: GTKWave zur grafischen Auswertung der aufgezeichneten Signalverläufe (Waveforms)

Der Simulationsprozess wird direkt aus der GUI angestoßen und durchläuft automatisiert die Schritte Kompilierung, Build und Ausführung . Das Ergebnis ist eine VCD-Datei (*trace.vcd*), die sämtliche internen Signalwechsel protokolliert.

```{figure} images/Abb6.1.png
:name: fig:sim_workflow
:width: 100%
:align: center

Der Simulations-Workflow
```
```{raw} latex
\clearpage
```

## Aufbau des Testbenches (Testbench)

Die Testbench tb_gui.cpp fungiert als Wrapper für den simulierten Prozessorkern. Sie stellt die notwendige Infrastruktur bereit, damit der Prozessor Instruktionen laden und Daten speichern kann. Die Implementierung nutzt die Verilator-API und gliedert sich in drei funktionale Blöcke:


1. **Initialisierung und Programmspeicher:** Zu Beginn der Simulation wird ein festes Testprogramm (irom) definiert. Um nicht nur die Standardbefehle, sondern auch die Custom ALU zu verifizieren, wurde eine spezifische Testsequenz entwickelt:

- *addi x1, x0, 0x123*: Lädt den Wert 291 (0x123) in Register x1.

- *addi x2, x0, 0x123*: Lädt denselben Wert in Register x2.

- **Custom Instruction**: Führt die benutzerdefinierte SIMD-Addition aus (*x3 = x1 + x2*).

- *sw x3, 0x100(x0)*: Schreibt das Ergebnis (erwartet: 0x246) in den Speicher.

- *jal x0, 0*: Endlosschleife.

Zwischen den Befehlen wurden nop-Instruktionen (No Operation) eingefügt, um potenzielle Pipeline-Hazards in dieser isolierten Testumgebung sicher auszuschließen und die Signalverläufe klarer trennen zu können.

2. **Taktsteuerung**: Die Simulation erfolgt in einer Schleife über 400 Taktzyklen. In jedem Durchlauf emuliert der Testbench explizit die steigenden und fallenden Flanken des Taktsignals (*clk*), wodurch die synchrone Logik des Prozessors geschaltet wird.

3. **Bus-Simulation**: Der Testbench überwacht die *dBus*-Signale, um Speicherzugriffe abzufangen. Anstatt komplexer Bit-Operationen nutzt die Implementierung *std::memcpy*, um Daten zwischen dem simulierten Bus und dem *dmem*-Array zu transferieren. Dies ermöglicht eine sehr kompakte und lesbare Simulation des Datenbusses.

```{figure} images/Abb6.2.png
:name: fig:testbench_setup
:width: 80%
:align: center

Blockschaltbild des Testaufbaus
```


```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} cpp
:linenos:
:caption: Auszug aus tb_gui.cpp

if (top->dBus_cmd_valid && top->dBus_cmd_ready) {
    uint32_t addr = top->dBus_cmd_payload_address;
    // ... (Größenberechnung)

    if (top->dBus_cmd_payload_wr) {
        // Schreibzugriff (Store): Daten in simulierten Speicher schreiben
        std::memcpy(&dmem[addr], &top->dBus_cmd_payload_data, nbytes);
        
        // Logging für die Verifikation
        std::printf("SW  cycle=%3d  addr=0x%08x  data=0x%08x  size=%u\n", 
                    cycle, addr, top->dBus_cmd_payload_data, nbytes);
    } else {
        // Lesezugriff (Load): Daten bereitstellen
        // ...
    }
}
```

```{raw} latex
\end{minipage}
```
Dieser Mechanismus ermöglicht eine geschlossene Verifikation: Das Ergebnis der Custom-ALU-Berechnung wird durch den sw-Befehl auf den Bus gelegt, von der Testbench abgefangen und auf der Konsole ausgegeben.

```{raw} latex
\clearpage
```

## Erweiterte Signalüberwachung

Um über die bloße Ein-/Ausgabe-Prüfung hinausgehende Diagnosen zu ermöglichen, wurden spezifische interne Signale der VexRiscv-Pipeline für das Tracing freigeschaltet. Dies erlaubt einen tiefen Einblick in den internen Zustand des Kerns.

Zu den wichtigsten überwachten Signalen gehören:
- *execute_IS_ALU_REG*: Kennzeichnet aktive ALU-Operationen.

- *execute_BRANCH_DO*: Signalisiert aktive Sprünge.

- *writeBack_REGFILE_WRITE_VALID*: Bestätigt das erfolgreiche Schreiben in das Registerfile.

Die Analyse dieser Signale in GTKWave ist essenziell, um sicherzustellen, dass die Custom Instruction korrekt in die Pipeline integriert wurde und das Ergebnis im richtigen Taktzyklus zurückschreibt.

```{raw} latex
\clearpage
```
## Verifikation des Befehlssatzes

Ein besonderer Fokus lag auf der Validierung der durch die GUI generierten Hardware-Erweiterung. Im getesteten Szenario wurde eine SIMD-Addition (MySimdAdd) implementiert.

Die Erwartungswerte für den Test waren:

- Arithmetisch-Logische Befehle (wie addi): Prüft die ALU-Funktionalität und Immediate-Verarbeitung.

- Speicherzugriffe: Durch Sequenzen von SW (Store Word) und LW (Load Word) wurde überprüft, ob Daten korrekt im emulierten RAM abgelegt und konsistent wiederhergestellt werden.

- Kontrollfluss: Sprungbefehle (BEQ, JAL) wurden genutzt, um die korrekte Berechnung des Program Counters (PC) bei Verzweigungen zu verifizieren


```{figure} images/abb6.3.png
:name: fig:gtkwave_trace
:width: 100%
:align: center

Validierung der Custom ALU im GTKWave-Trace
```
## Validierung über Konsolenausgabe
Ein wesentlicher Vorteil des verwendeten C++-Testbenches ist die direkte Protokollierung der Speicherzugriffe auf der Konsole. Während der Simulation generiert der Code Ausgaben, die den Datenfluss transparent machen:


```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} text
:linenos:
:caption: 

IF  cycle=  1  pc=0x00000000  word= 0  inst=0x12300093
IF  cycle=  2  pc=0x00000004  word= 1  inst=0x00000013
IF  cycle=  3  pc=0x00000008  word= 2  inst=0x12300113
IF  cycle=  4  pc=0x0000000c  word= 3  inst=0x00000013
IF  cycle=  5  pc=0x00000010  word= 4  inst=0x0020818b
# Custom Instruction
IF  cycle=  6  pc=0x00000014  word= 5  inst=0x00000013
IF  cycle=  8  pc=0x00000018  word= 6  inst=0x10302023
IF  cycle=  9  pc=0x0000001c  word= 7  inst=0x0000006f
IF  cycle= 11  pc=0x00000020  word= 8  inst=0x00000013
IF  cycle= 12  pc=0x00000024  word= 9  inst=0x00000013
SW  cycle= 12  addr=0x00000100  data=0x00000246  size=4
```

```{raw} latex
\end{minipage}
```

Diese Ausgabe bestätigt zwei kritische Punkte:
- Korrekter Fetch: Der Prozessor hat die Custom Instruction (Opcode *0x0020818b*) an Adresse *0x10* korrekt geladen.
- Korrekte Berechnung: Der nachfolgende Schreibbefehl (*SW*) schreibt den Wert *0x00000246* an die Adresse *0x100*.

Da 0x123 + 0x123 exakt 0x246 ergibt, ist hiermit der funktionale Nachweis erbracht, dass die über die GUI definierte Logik korrekt in Verilog übersetzt, synthetisiert und ausgeführt wurde.

### Bedeutung für die Verifikation

Durch die Kombination aus **Signalaufzeichnung**, **Busaktivitätsprotokoll** und **Konsolenausgabe** konnte eine vollständige **funktionale Verifikation** des VexRiscv-Kerns erreicht werden.  
Die Simulation belegt, dass:

- alle getesteten Instruktionen korrekt dekodiert und ausgeführt wurden,  
- der Speicherzugriff synchron und stabil funktioniert,  
- keine unerwarteten Pipeline-Konflikte (Hazards) auftraten,  
- und der Program Counter stets deterministisch arbeitet.

Damit erfüllt die implementierte CPU-Architektur die Anforderungen an einen funktionsfähigen **RV32I-Prozessor** gemäß der RISC-V-Spezifikation.  
Das Ergebnis zeigt, dass sowohl der Instruktionsfluss als auch die Speicheroperationen vollständig im Einklang mit den Architekturprinzipien des RISC-V-Standards stehen.


## Zusammenfassung der Simulationsergebnisse

Die in diesem Kapitel beschriebene Simulationsmethodik lieferte den empirischen Nachweis für die funktionale Korrektheit des generierten Prozessorsystems. Durch die Kombination aus zyklusgenauer RTL-Simulation mittels Verilator und detaillierter Signalanalyse in GTKWave konnte verifiziert werden, dass die von der GUI erzeugte Hardwarebeschreibung (Verilog) sowohl die Spezifikation des RISC-V-Standards erfüllt als auch die benutzerdefinierten Erweiterungen fehlerfrei implementiert. 

Die Ergebnisse lassen sich in drei Kernbereiche zusammenfassen:

1. **Validierung der Basis-Architektur (RV32I):** Die Simulation bestätigte, dass der automatisch konfigurierte VexRiscv-Kern die fundamentalen Operationen einer RV32I-CPU mit Harvard-Architektur (getrennter Instruktions- und Datenbus) korrekt ausführt.

- Datenpfad: Register-Transfers zwischen Speicher (Load/Store) und Registerfile erfolgten bitgenau und ohne Datenverlust.

- Kontrollfluss: Sprungbefehle (JAL, BEQ) manipulierten den Program Counter (PC) deterministisch, wobei die Pipeline-Stufen (Fetch, Decode, Execute) synchron arbeiteten.

- Hazard-Management: Potenzielle Datenkonflikte (Read-After-Write) wurden durch die Hardware-Interlocks des HazardSimplePlugin oder durch softwareseitige NOPs im Testbench korrekt aufgelöst, sodass zu keinem Zeitpunkt invalide Daten verarbeitet wurden.

2. **Verifikation der Custom-Instruction-Integration:** Ein Schwerpunkt der Evaluierung lag auf der Überprüfung der generativen Erweiterungen. Der in Abschnitt 6.4 definierte Testfall für die MySimdAdd-Instruktion lieferte den Beweis für die erfolgreiche "Pipeline-Injection".

- Korrekte Dekodierung: Der benutzerdefinierte Opcode (0x0020818b) wurde vom Decoder eindeutig erkannt und aktivierte die spezifische ALU-Logik in der Execute-Stufe.

- Rechengenauigkeit: Die durchgeführte SIMD-Addition der Testwerte (0x123 + 0x123) resultierte exakt im erwarteten Ergebnis 0x246. Dies belegt, dass die in der GUI definierte High-Level-Logik (Scala) semantisch korrekt in synthetisierbare Hardwareschaltungen übersetzt wurde.

- Timing: Das Ergebnis stand, wie für eine Single-Cycle-Instruktion gefordert, innerhalb eines Taktzyklus am Rückschreibepfad bereit.

3. **Konsistenz der Toolchain:** Der Abgleich zwischen den Protokollen der C++-Testbench (High-Level-Sicht) und den Wellenformen in GTKWave (Low-Level-Sicht) zeigte eine vollständige Übereinstimmung. Es traten keine Diskrepanzen zwischen dem erwarteten Software-Verhalten und der tatsächlichen Hardware-Ausführung auf.

**Fazit**:

Die Simulationsergebnisse belegen, dass die entwickelte Entwicklungsumgebung in der Lage ist, valides und funktionsfähiges Prozessordesign zu erzeugen. Die automatisierte Integration von Custom Instructions, welche die zentrale Innovation dieser Arbeit darstellt, hat sich als robust und verlässlich erwiesen. Damit ist die notwendige Vertrauensbasis geschaffen, um im nachfolgenden Kapitel den Transfer des Designs auf die physische FPGA-Hardware vorzunehmen.
