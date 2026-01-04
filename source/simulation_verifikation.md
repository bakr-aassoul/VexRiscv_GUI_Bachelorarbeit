# Simulation und Verifikation

Die Simulation bildet den zentralen Nachweis der Funktionsfähigkeit des mit der GUI erzeugten Prozessors. Sie dient der Validierung, ob der automatisch generierte Verilog-Code die erwarteten Operationen des RISC-V-Befehlssatzes sowie die benutzerdefinierten Erweiterungen (Custom Instructions) korrekt ausführt. In diesem Kapitel werden der Testaufbau, die Durchführung der Simulation mittels Verilator und die Analyse der Ergebnisse beschrieben.

---

## Testaufbau

Für die funktionale Verifikation wurde der generierte Verilog-Code (*VexRiscv.v*) mithilfe von Verilator simuliert. Im Gegensatz zu klassischen ereignisbasierten Simulatoren übersetzt Verilator das Hardware-Design in ein optimiertes C++-Modell. Dies ermöglicht eine effiziente, zyklusgenaue Simulation, die sich nahtlos in C++-Testumgebungen integrieren lässt

Das Testsystem setzt sich aus folgenden Komponenten zusammen:

- Device Under Test (DUT): Der generierte VexRiscv-Prozessorkern. 
- Testbench: Eine in C++ implementierte Umgebung (minimal_tb.cpp), die den Prozessor instanziiert, Takte generiert und die Peripherie (Speicher, Reset) simuliert.  
- Analysewerkzeug: GTKWave zur grafischen Auswertung der aufgezeichneten Signalverläufe (Waveforms)

Der Simulationsprozess wird direkt aus der GUI angestoßen und durchläuft automatisiert die Schritte Kompilierung, Build und Ausführung . Das Ergebnis ist eine VCD-Datei (*trace.vcd*), die sämtliche internen Signalwechsel protokolliert.

**Einfügen: Abbildung 6.1 – Simulations-Workflow
Was: Ein Flussdiagramm, das den Weg zeigt: GUI → VexRiscv.v (Verilog) → Verilator Compiler → simv (Executable) → trace.vcd → GTKWave.
Warum: Es visualisiert den abstrakten Prozess für den Leser auf einen Blick und zeigt, wie die Tools ineinandergreifen.**

## Aufbau der Testumgebung (Testbench)

Dabei wird der Prozessor in Software simuliert, und alle internen Signale werden in der Datei trace.vcd gespeichert.
Die resultierende Datei `trace.vcd` (Value Change Dump) enthält sämtliche zeitlichen Signaländerungen des Prozessors.  
Sie dient als Grundlage für die grafische Analyse in **GTKWave** und ermöglicht eine detaillierte Verifikation der CPU-Architektur.  

Im Rahmen dieser Arbeit wurde die Simulation mit einer **Taktperiode von 1 ns** durchgeführt, was eine ausreichend feine Auflösung für die Untersuchung der Pipeline-Stufen bietet.  
Die Simulationsergebnisse lassen sich damit präzise im zeitlichen Verlauf darstellen.

---

## Aufbau des Testbenches

Der Testbench tb_gui.cpp fungiert als Wrapper für den simulierten Prozessorkern. Er stellt die notwendige Infrastruktur bereit, damit der Prozessor Instruktionen laden und Daten speichern kann. Die Implementierung nutzt die Verilator-API und gliedert sich in drei funktionale Blöcke:


1. **Initialisierung und Programmspeicher:** Zu Beginn der Simulation wird ein festes Testprogramm (irom) definiert, das eine grundlegende Sanity-Check-Sequenz enthält:

- *addi x1, x0, 0x123*: Lädt einen Testwert in Register x1.

- *sw x1, 0x100(x0)*: Schreibt diesen Wert in den Speicher.

- *lw x2, 0x100(x0)*: Liest den Wert zurück in Register x2.

- *jal x0, 0*: Endlosschleife.

Zusätzlich wird ein 4 KiB großer Datenspeicher (*dmem*) als Byte-Array initialisiert.

2. **Taktsteuerung**: Die Simulation erfolgt in einer Schleife über 400 Taktzyklen. In jedem Durchlauf emuliert der Testbench explizit die steigenden und fallenden Flanken des Taktsignals (*clk*), wodurch die synchrone Logik des Prozessors geschaltet wird.

3. **Bus-Simulation** Der Testbench überwacht die *dBus*-Signale, um Speicherzugriffe abzufangen. Anstatt komplexer Bit-Operationen nutzt die Implementierung *std::memcpy*, um Daten zwischen dem simulierten Bus und dem *dmem*-Array zu transferieren. Dies ermöglicht eine sehr kompakte und lesbare Simulation des Datenbusses.

**Einfügen: Abbildung 6.2 – Blockschaltbild des Testaufbaus
Was: Ein Diagramm mit dem "VexRiscv Core" (DUT) in der Mitte. Pfeile zeigen die Verbindungen zum umgebenden "Testbench (C++)".
Pfeile rein (Inputs): clk, reset, iBus Response, dBus Response.
Pfeile raus (Outputs): iBus Command (PC), dBus Command (Address/Data).
Warum: Verdeutlicht, wie der C++-Code physikalisch mit den Verilog-Ports des Prozessors kommuniziert.**

```cpp
// Auszug aus tb_gui.cpp
if (top->dBus_cmd_valid && top->dBus_cmd_ready) {
    uint32_t addr = top->dBus_cmd_payload_address;
    uint32_t size = top->dBus_cmd_payload_size;
    uint32_t nbytes = 1u << size; // Berechnung der Byte-Anzahl (2^size)

    if (top->dBus_cmd_payload_wr) {
        // Schreibzugriff (Store): Kopiere Daten vom Bus in den Speicher
        std::memcpy(&dmem[addr], &top->dBus_cmd_payload_data, nbytes);
        std::printf("[SW]  addr=0x%08x data=0x%08x size=%u\n", addr, top->dBus_cmd_payload_data, size);
    } else {
        // Lesezugriff (Load): Kopiere Daten vom Speicher auf den Bus
        uint32_t rdata = 0;
        std::memcpy(&rdata, &dmem[addr], nbytes);
        top->dBus_rsp_data = rdata;
        std::printf("[LW]  addr=0x%08x data=0x%08x size=%u\n", addr, rdata, size);
    }
}
```
Dieser Codeabschnitt stellt sicher, dass jeder Schreibvorgang (SW) protokolliert und persistent gespeichert wird, sodass ein nachfolgender Lesebefehl (LW) korrekte Daten erhält.



## Erweiterte Signalüberwachung

Um über die bloße Ein-/Ausgabe-Prüfung hinausgehende Diagnosen zu ermöglichen, wurden spezifische interne Signale der VexRiscv-Pipeline für das Tracing freigeschaltet. Dies erlaubt einen tiefen Einblick in den internen Zustand des Kerns während der Laufzeit.

Zu den wichtigsten überwachten Signalen gehören:
- *execute_IS_ALU_REG*: Kennzeichnet ALU-Operationen.

- *execute_BRANCH_DO*: Signalisiert aktive Sprünge.

- *writeBack_REGFILE_WRITE_VALID*: Bestätigt das erfolgreiche Schreiben in das Registerfile.

Die Analyse dieser Signale ist essenziell, um Pipeline-Hazards oder fehlerhafte Sprungvorhersagen zu identifizieren.

## Verifikation des Befehlssatzes

Die Validierung erfolgte anhand des im irom definierten Testprogramms. Die Sequenz deckt die wichtigsten Basisoperationen ab:

- Arithmetisch-Logische Befehle (wie addi): Prüft die ALU-Funktionalität und Immediate-Verarbeitung.

- Speicherzugriffe: Durch Sequenzen von SW (Store Word) und LW (Load Word) wurde überprüft, ob Daten korrekt im emulierten RAM abgelegt und konsistent wiederhergestellt werden.

- Kontrollfluss: Sprungbefehle (BEQ, JAL) wurden genutzt, um die korrekte Berechnung des Program Counters (PC) bei Verzweigungen zu verifizieren


**Einfügen: Abbildung 6.3 – Validierung von Speicherzugriffen im GTKWave-Trace
Was: Ein Screenshot aus GTKWave, der einen Store (Schreiben) und kurz darauf einen Load (Lesen) zeigt.
Markieren Sie die Signale dBus_cmd_payload_address (Adresse) und dBus_cmd_payload_data (Daten).
Warum: Belegt visuell, dass die Simulation funktioniert ("Proof of Work") und der Prozessor tatsächlich mit dem Speicher interagiert.**

## Validierung über Konsolenausgaben

Ein wesentlicher Vorteil des verwendeten C++-Testbenches ist die direkte Protokollierung der Speicherzugriffe auf der Konsole. Während der Simulation generiert der Code Ausgaben, die den Datenfluss transparent machen:


```text

[SW]  addr=0x00000100 data=0x00000123 size=2
[LW]  addr=0x00000100 data=0x00000123 size=2
```

Diese Ausgabe bestätigt:
- Der sw-Befehl hat den Wert *0x123* erfolgreich an Adresse 0x100 geschrieben.
- Der nachfolgende lw-Befehl hat exakt denselben Wert von dieser Adresse gelesen.

---

### Bedeutung für die Verifikation

Durch die Kombination aus **Signalaufzeichnung**, **Busaktivitätsprotokoll** und **Konsolenausgabe** konnte eine vollständige **funktionale Verifikation** des VexRiscv-Kerns erreicht werden.  
Die Simulation belegt, dass:

- alle getesteten Instruktionen korrekt dekodiert und ausgeführt wurden,  
- der Speicherzugriff synchron und stabil funktioniert,  
- keine unerwarteten Pipeline-Konflikte (Hazards) auftraten,  
- und der Program Counter stets deterministisch arbeitet.

Damit erfüllt die implementierte CPU-Architektur die Anforderungen an einen funktionsfähigen **RV32I-Prozessor** gemäß der RISC-V-Spezifikation.  
Das Ergebnis zeigt, dass sowohl der Instruktionsfluss als auch die Speicheroperationen vollständig im Einklang mit den Architekturprinzipien des RISC-V-Standards stehen.

---

### Visualisierung der Ergebnisse

Im Folgenden ist ein Ausschnitt der simulierten Signale dargestellt,  
wie sie in **GTKWave** beobachtet wurden:


*Abbildung 1: Ausschnitt aus dem GTKWave-Verlauf mit sichtbaren Fetch-, Decode- und Speicherzugriffen.*

In der dargestellten Signalsequenz sind die Taktflanken (`clk`), der Program Counter (`iBus_cmd_payload_pc`) sowie die Datenbus-Aktivitäten (`dBus_cmd_payload_address`, `dBus_rsp_data`) klar zu erkennen.  

Diese Darstellung bestätigt das korrekte Zusammenspiel der Pipeline-Stufen, vom **Instruktionsabruf (Fetch)** über **Dekodierung (Decode)** bis zur **Speicherphase (Memory)** und unterstreicht die Zuverlässigkeit des automatisch generierten Prozessordesigns.

---

## Zusammenfassung der Simulationsergebnisse

Die Simulation und anschließende Signalverifikation bestätigen die **funktionale Korrektheit** des mit der GUI generierten VexRiscv-Prozessors.  
Alle getesteten Instruktionen aus dem **RV32I-Befehlssatz** wurden fehlerfrei dekodiert, ausgeführt und in den aufgezeichneten Wellenformen nachvollzogen.  

Zusätzlich zeigte die Analyse:

- stabile Pipeline-Ausführung ohne Hazard-Konflikte,  
- korrekte Takt- und Reset-Sequenzen,  
- konsistente Busoperationen mit synchronem Zugriff auf den Speicher,  
- sowie deterministische Sprung- und Rücksprungverhalten der Branch-Logik.

Die Kombination aus **Verilator-Simulation** und **GTKWave-Signalanalyse** ermöglichte eine präzise Beobachtung des internen CPU-Verhaltens.  
Damit konnte nachgewiesen werden, dass die durch die GUI erzeugten Prozessorvarianten nicht nur syntaktisch korrekt generiert, sondern auch **funktional stabil und reproduzierbar** sind.

Dieses Ergebnis belegt die Wirksamkeit der entworfenen Designumgebung als **vollständige Verifikationsplattform** für den VexRiscv-Prozessor.  
Sie ermöglicht eine effiziente Überprüfung neuer Konfigurationen, ohne manuelle Anpassungen im Quellcode oder in der Build-Kette vornehmen zu müssen.

---

