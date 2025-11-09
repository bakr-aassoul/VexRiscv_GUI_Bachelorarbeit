# Simulation und Verifikation

Die Simulation bildet den zentralen Nachweis der Funktionsfähigkeit des mit der GUI erzeugten Prozessors.  
Sie überprüft, ob der automatisch generierte Verilog-Code die erwarteten Operationen des RISC-V-Befehlssatzes korrekt ausführt.

---

## Testaufbau

Für die Verifikation wurde der erzeugte Verilog-Code mit **Verilator** simuliert.  
Das Testsystem bestand aus:

- dem generierten Prozessor (`VexRiscv.v`),  
- einem **C++-Testbench** (`minimal_tb.cpp`),  
- und der grafischen Signalansicht in **GTKWave**.

Die Simulation wurde automatisiert über die GUI gestartet,  
welche im Hintergrund die folgenden Befehle ausführt:

```bash
verilator -cc output/gui_build/VexRiscv.v --exe sim/minimal_tb.cpp -Wno-WIDTH --trace
make -C obj_dir -f VVexRiscv.mk VVexRiscv
./obj_dir/VVexRiscv
```
Dabei wird der Prozessor in Software simuliert,
und alle internen Signale werden in der Datei trace.vcd gespeichert.
Die resultierende Datei `trace.vcd` (Value Change Dump) enthält sämtliche zeitlichen Signaländerungen des Prozessors.  
Sie dient als Grundlage für die grafische Analyse in **GTKWave** und ermöglicht eine detaillierte Verifikation der CPU-Architektur.  

Im Rahmen dieser Arbeit wurde die Simulation mit einer **Taktperiode von 1 ns** durchgeführt,  
was eine ausreichend feine Auflösung für die Untersuchung der Pipeline-Stufen bietet.  
Die Simulationsergebnisse lassen sich damit präzise im zeitlichen Verlauf darstellen.

---

## Aufbau des Testbenches

Der Testbench `minimal_tb.cpp` bildet die Verbindung zwischen dem generierten Verilog-Modul und der Verilator-Simulationsumgebung.  
Er steuert den Takt, setzt die Reset-Signale, liefert Instruktionen über den `iBus` und verarbeitet Datenzugriffe über den `dBus`.

Der Aufbau des Testbenches lässt sich in drei Hauptbereiche gliedern:

1. **Initialisierung**
   - Setzen der Eingangssignale (`clk = 0`, `reset = 1`)
   - Bereitstellung eines kleinen ROMs mit Testinstruktionen
   - Definition eines simulierten RAMs (z. B. `uint8_t ram[4096]`)

2. **Taktsteuerung**
   - Die Simulation läuft über eine Schleife von typischerweise 200–400 Zyklen
   - In jedem Zyklus werden steigende und fallende Flanken ausgewertet
   - Alle Änderungen werden mit Zeitstempel (`main_time++`) in die VCD-Datei geschrieben

3. **Buskommunikation**
   - Der `iBus` liefert die nächsten Instruktionen
   - Der `dBus` wird für Speichertransaktionen genutzt  
     (Lesen/Schreiben von Werten bei `lw` und `sw`)

Der Codeabschnitt für die Busbehandlung im Testbench sieht beispielsweise so aus:

```cpp
if (top->dBus_cmd_valid) {
    uint32_t addr = top->dBus_cmd_payload_address & (sizeof(ram)-1);
    if (top->dBus_cmd_payload_wr) {
        ram[addr]     = top->dBus_cmd_payload_data & 0xFF;
        ram[addr + 1] = (top->dBus_cmd_payload_data >> 8) & 0xFF;
        ram[addr + 2] = (top->dBus_cmd_payload_data >> 16) & 0xFF;
        ram[addr + 3] = (top->dBus_cmd_payload_data >> 24) & 0xFF;
    } else {
        uint32_t rdat = (ram[addr + 3] << 24) | (ram[addr + 2] << 16)
                      | (ram[addr + 1] << 8)  | (ram[addr + 0] << 0);
        top->dBus_rsp_data = rdat;
    }
}
```
Dieser Abschnitt zeigt den simulierten Zugriff auf den Arbeitsspeicher des Prozessors.
Sobald der Core ein sw (Store Word) ausführt, werden die Daten in das ram[]-Array geschrieben.
Ein anschließendes lw (Load Word) liest dieselben Werte wieder zurück und prüft somit die Speicherintegrität.
Durch diesen Mechanismus lässt sich im Verlauf der Simulation eindeutig nachweisen,  
dass die Speicherzugriffe des Prozessors korrekt funktionieren.  
Der Abgleich zwischen geschriebenen und gelesenen Werten bildet somit einen  
wichtigen Teil der funktionalen Verifikation des Designs.

---

## Erweiterte Signalüberwachung

Neben den Standard-Bus-Signalen werden während der Simulation auch interne Signale beobachtet,  
um ein umfassendes Verständnis des Prozessors zu erhalten.  
Dazu gehören insbesondere:

| Signalname | Beschreibung |
|-------------|--------------|
| **execute_IS_ALU_REG** | Kennzeichnet, ob die aktuelle Instruktion eine ALU-Operation ausführt |
| **execute_BRANCH_DO** | Zeigt an, ob ein Sprungbefehl (Branch) aktiv ist |
| **memory_STORE** | Gibt an, dass ein Speicher-Schreibvorgang (Store) aktiv ist |
| **writeBack_REGFILE_WRITE_VALID** | Bestätigt den erfolgreichen Schreibvorgang in das Registerfile |
| **csrplugin_inWfi** | Markiert den Low-Power-Wait-Zustand, falls aktiviert |

Diese erweiterten Signale bieten tiefe Einblicke in die Pipelineaktivitäten und  
unterstützen die Identifikation potenzieller Timing- oder Logikfehler.  
Sie werden ebenfalls in der Datei `trace.vcd` abgelegt und können in GTKWave eingeblendet werden.

---

## Verifikation des Befehlssatzes

Zur weiteren Überprüfung wurde der Grundbefehlssatz **RV32I** des RISC-V-Standards getestet.  
Dabei lag der Fokus auf den folgenden Instruktionsgruppen:

| Kategorie | Beispielbefehle | Zweck |
|------------|----------------|-------|
| **Arithmetisch-logisch** | `addi`, `sub`, `and`, `or`, `xor` | Test der ALU und Registerlogik |
| **Sprungbefehle** | `beq`, `jal`, `jalr` | Prüfung der Verzweigungs- und PC-Logik |
| **Speicherbefehle** | `lw`, `sw` | Kontrolle der Bus- und RAM-Operationen |
| **Systembefehle** | `ecall`, `ebreak` (optional) | Kontrolle des CSR-Plugins |

Alle getesteten Instruktionen zeigten das erwartete Verhalten.  
Besonders die Speicher- und Sprungbefehle ließen sich im GTKWave-Trace gut nachvollziehen,  
da sie markante Signaländerungen auf `dBus` und `iBus` verursachen.

---

## Validierung über Konsolenausgaben

Während der Simulation wurden zusätzlich Konsolenausgaben generiert,  
um wichtige Prozessschritte direkt zu protokollieren.  
Beispiel:

```text
Cycle 1  PC=0x00000000
Cycle 2  PC=0x00000004
Cycle 3  PC=0x00000008
Cycle 4  PC=0x0000000C
Cycle 5  PC=0x00000000  <-- Sprung zurück (Branch aktiv)
```

Diese Ausgabe verdeutlicht das korrekte Verhalten des Program Counters
und bestätigt die fehlerfreie Auswertung des beq-Befehls.
Somit wird die Übereinstimmung zwischen Simulation und GTKWave-Darstellung sichergestellt.

---

### Bedeutung für die Verifikation

Durch die Kombination aus **Signalaufzeichnung**, **Busaktivitätsprotokoll** und **Konsolenausgabe**  
konnte eine vollständige **funktionale Verifikation** des VexRiscv-Kerns erreicht werden.  
Die Simulation belegt, dass:

- alle getesteten Instruktionen korrekt dekodiert und ausgeführt wurden,  
- der Speicherzugriff synchron und stabil funktioniert,  
- keine unerwarteten Pipeline-Konflikte (Hazards) auftraten,  
- und der Program Counter stets deterministisch arbeitet.

Damit erfüllt die implementierte CPU-Architektur die Anforderungen  
an einen funktionsfähigen **RV32I-Prozessor** gemäß der RISC-V-Spezifikation.  
Das Ergebnis zeigt, dass sowohl der Instruktionsfluss als auch die Speicheroperationen  
vollständig im Einklang mit den Architekturprinzipien des RISC-V-Standards stehen.

---

### Visualisierung der Ergebnisse

Im Folgenden ist ein Ausschnitt der simulierten Signale dargestellt,  
wie sie in **GTKWave** beobachtet wurden:


*Abbildung 1: Ausschnitt aus dem GTKWave-Verlauf mit sichtbaren Fetch-, Decode- und Speicherzugriffen.*

In der dargestellten Signalsequenz sind die Taktflanken (`clk`),  
der Program Counter (`iBus_cmd_payload_pc`) sowie die Datenbus-Aktivitäten (`dBus_cmd_payload_address`, `dBus_rsp_data`)  
klar zu erkennen.  

Diese Darstellung bestätigt das korrekte Zusammenspiel der Pipeline-Stufen —  
vom **Instruktionsabruf (Fetch)** über **Dekodierung (Decode)** bis zur **Speicherphase (Memory)** und unterstreicht die Zuverlässigkeit des automatisch generierten Prozessordesigns.

---

## Zusammenfassung der Simulationsergebnisse

Die Simulation und anschließende Signalverifikation bestätigen die **funktionale Korrektheit**  
des mit der GUI generierten VexRiscv-Prozessors.  
Alle getesteten Instruktionen aus dem **RV32I-Befehlssatz** wurden fehlerfrei dekodiert, ausgeführt  
und in den aufgezeichneten Wellenformen nachvollzogen.  

Zusätzlich zeigte die Analyse:

- stabile Pipeline-Ausführung ohne Hazard-Konflikte,  
- korrekte Takt- und Reset-Sequenzen,  
- konsistente Busoperationen mit synchronem Zugriff auf den Speicher,  
- sowie deterministische Sprung- und Rücksprungverhalten der Branch-Logik.

Die Kombination aus **Verilator-Simulation** und **GTKWave-Signalanalyse**  
ermöglichte eine präzise Beobachtung des internen CPU-Verhaltens.  
Damit konnte nachgewiesen werden, dass die durch die GUI erzeugten Prozessorvarianten  
nicht nur syntaktisch korrekt generiert, sondern auch **funktional stabil und reproduzierbar** sind.

Dieses Ergebnis belegt die Wirksamkeit der entworfenen Designumgebung als  
**vollständige Verifikationsplattform** für den VexRiscv-Prozessor.  
Sie ermöglicht eine effiziente Überprüfung neuer Konfigurationen,  
ohne manuelle Anpassungen im Quellcode oder in der Build-Kette vornehmen zu müssen.

---

