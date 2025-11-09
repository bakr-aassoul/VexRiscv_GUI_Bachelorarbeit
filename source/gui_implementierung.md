# GUI-Implementierung

Die Implementierung der grafischen Benutzeroberfläche basiert auf **Python 3**  
und verwendet das **Tkinter-Framework** zur Darstellung und Steuerung der Benutzerinteraktionen.  
Das Gesamtsystem besteht aus zwei klar getrennten Teilen:

1. dem **Backend-Skript** `gui_backend.py`, das die eigentliche Logik, Dateigenerierung und Simulation steuert,  
2. dem **Frontend (GUI)**, das die Bedienoberfläche darstellt und alle Funktionen über Buttons und Checkboxen zugänglich macht.

---

## Aufbau des Backends (`gui_backend.py`)

Das Backend ist das Herzstück der Anwendung.  
Es enthält alle Funktionen zur Kommunikation mit SpinalHDL, Verilator und GTKWave.  
Die Datei ist modular aufgebaut und gliedert sich in mehrere Hauptfunktionen.

### 1. `read_selected()`
Liest die vom Benutzer gewählten Plugins aus der JSON-Datei `gui_config.json`.  
Wenn keine Auswahl vorhanden ist, wird eine **Baseline-Konfiguration** genutzt,  
die alle für einen lauffähigen Prozessor notwendigen Plugins enthält.  
Wird die Option *Auto-add required plugins* aktiviert, ergänzt das Skript automatisch alle essenziellen Pipeline-Plugins,  
um eine vollständige CPU-Konfiguration sicherzustellen.

### 2. `write_top(selected)`
Erzeugt automatisch eine Scala-Datei (`VexRiscvTopFromGui.scala`),  
in der die ausgewählten Plugins als Liste in der VexRiscv-Konfiguration definiert werden.

```scala
val cpuConfig = VexRiscvConfig(plugins = List(
  new IBusSimplePlugin(...),
  new DBusSimplePlugin(),
  new IntAluPlugin(),
  new CsrPlugin(...)
))
```
### 3. `generate()`

Die Funktion `generate()` ruft die Build-Toolchain von **SpinalHDL** über das Scala-Build-Tool (**SBT**) auf:

```bash
sbt "runMain vexriscv.demo.VexRiscvTopFromGui"
```

Dabei wird die zuvor erzeugte Scala-Datei kompiliert und von SpinalHDL in **Verilog-Code übersetzt**.
Das resultierende Hardware-Design wird anschließend im Verzeichnis output/gui_build/ gespeichert.
Nach erfolgreichem Build wird der Pfad zur erzeugten Datei im Log-Fenster ausgegeben.

Die Funktion beinhaltet außerdem Sicherheitsprüfungen, um sicherzustellen,
dass das Verilog-File (VexRiscv.v) tatsächlich existiert.
Falls der Build fehlschlägt, wird der Prozess automatisch abgebrochen und eine Fehlermeldung ausgegeben.

### 4. `simulate()`

Die Funktion `simulate()` führt die automatische **Simulation** des zuvor generierten Prozessors mit **Verilator** durch.  
Dabei wird der in Verilog erzeugte VexRiscv-Core mit einem einfachen **Testbench** (z. B. `minimal_tb.cpp`) verknüpft.  
Dieser Testbench simuliert die grundlegenden Instruktionen und überprüft das Verhalten des Daten- und Instruktionsbusses.

Der Simulationsablauf besteht aus mehreren Schritten:

1. **Initialisierung**  
   Zu Beginn werden Takt (`clk`) und Reset (`reset`) gesetzt.  
   Der Prozessor wird einige Zyklen im Reset gehalten, bevor die Simulation startet.

2. **Instruktionsabruf**  
   Über den `iBus` fordert der Core fortlaufend Instruktionen an.  
   Das Testbench-Modul liefert diese direkt aus einem internen ROM-Array,  
   beispielsweise die Befehle `addi`, `sw`, `lw` oder `jal`.

3. **Datenbus-Operationen**  
   Wenn über den `dBus` eine Speichertransaktion angefordert wird,  
   simuliert das Testbench-Modul ein kleines Speicher-Array (`uint8_t ram[4096]`),  
   das die Daten entsprechend schreibt oder liest.  
   Dadurch können Instruktionen wie **Load** und **Store** realistisch ausgeführt werden.

4. **Zeiterfassung und Signalverlauf**  
   Während der Simulation werden alle Signale getaktet evaluiert  
   (`top->eval()` bei steigender und fallender Flanke).  
   Gleichzeitig werden die Signale in einer **VCD-Datei** (`trace.vcd`) gespeichert,  
   die später in GTKWave analysiert werden kann.

Beispielausgabe während der Simulation:
```text
[SW]  addr=0x100 data=0xDEADBEEF size=2
[LW]  addr=0x100 data=0xDEADBEEF size=2
```
Die Simulation endet, sobald alle Instruktionen im Test-ROM abgearbeitet sind.
Der erzeugte Datei-Output trace.vcd enthält sämtliche Signalverläufe des Prozessors.

### 5. `wave()`

Die Funktion `wave()` öffnet nach der Simulation automatisch das Programm **GTKWave**,  
mit dem die zuvor erzeugte Datei `trace.vcd` visualisiert werden kann.  
GTKWave stellt eine leistungsfähige Möglichkeit dar,  
die internen Signalverläufe der CPU und Busaktivitäten grafisch zu analysieren.

Beim Start der Funktion wird im Hintergrund folgender Befehl ausgeführt:

```bash
gtkwave trace.vcd &
```
Dadurch wird das Wellenform-Fenster im Hintergrund geöffnet,
während die Python-Anwendung weiterhin aktiv bleibt.
Diese asynchrone Ausführung ermöglicht es, die Simulation mehrfach zu starten,
ohne GTKWave bei jedem Durchlauf manuell schließen zu müssen.

In der GTKWave-Ansicht lassen sich alle wichtigen Signale des VexRiscv-Cores beobachten, darunter:

| Signalname | Beschreibung |
|-------------|--------------|
| **clk** | Taktsignal des Prozessors, treibt alle Pipeline-Stufen |
| **reset** | Rücksetzsignal zur Initialisierung aller Register |
| **iBus_cmd_payload_pc** | Aktueller Program Counter (PC), zeigt die Adresse der nächsten Instruktion |
| **iBus_rsp_payload_inst** | Die aktuell vom Instruktionsbus geladene Instruktion |
| **dBus_cmd_payload_address** | Adresse, auf die der Prozessor beim Datenzugriff zugreift |
| **dBus_cmd_payload_data** | Die Daten, die bei einem Store-Befehl in den Speicher geschrieben werden |
| **dBus_rsp_data** | Daten, die bei einem Load-Befehl aus dem Speicher gelesen werden |

Diese Signale bilden die zentralen Schnittstellen der CPU-Pipeline ab und ermöglichen es,  
den kompletten Instruktionsfluss in **GTKWave** visuell zu verfolgen.  

---

### Ablauf der Signalbeobachtung

1. **Startphase:**  
   Nach dem Reset (`reset = 1`) werden alle Register auf definierte Startwerte gesetzt.  
   Sobald der Reset deaktiviert wird (`reset = 0`), beginnt der Prozessor mit dem Instruktionsabruf.

2. **Fetch & Decode:**  
   Der Wert des `iBus_cmd_payload_pc` erhöht sich in 4-Byte-Schritten,  
   während über `iBus_rsp_payload_inst` die entsprechenden Instruktionen geladen werden.  
   Hier kann beobachtet werden, welche Befehle nacheinander ausgeführt werden.

3. **Execute & Memory:**  
   Während der Ausführung der Befehle werden im GTKWave-Verlauf  
   Speicherzugriffe über den Datenbus sichtbar (`dBus_cmd_payload_address`, `dBus_cmd_payload_data`).  
   Bei `sw`-Instruktionen erscheinen Schreibzugriffe, bei `lw`-Instruktionen die entsprechenden Lesevorgänge.

4. **Verifikation des Speicherverhaltens:**  
   Das Signal `dBus_rsp_data` zeigt, dass der gelesene Wert mit dem zuvor gespeicherten übereinstimmt.  
   Im Beispiel der Instruktionen `sw` und `lw` (Store/Load) ist klar zu erkennen,  
   dass der Wert `0xDEADBEEF` korrekt geschrieben und anschließend fehlerfrei wieder gelesen wurde.

---

### Beispielhafter Signalverlauf

![GTKWave Signalverlauf](images/gtkwave_trace.png)

*Abbildung 1: GTKWave-Darstellung der CPU-Signale während der Simulation.*

In der obigen Abbildung ist der vollständige Ablauf des kleinen Testprogramms zu sehen.
Im dargestellten Programm werden einfache Instruktionen des RISC-V-Befehlssatzes ausgeführt.  
Das Programm dient zur Überprüfung der grundlegenden CPU-Funktionalität wie **ALU-Operationen**,  
**Program-Counter-Inkrementierung**, **Verzweigungen** und **Speicherzugriffe**.

```assembly
0x0000: addi x1, x0, 1      # Schreibe den Wert 1 in Register x1
0x0004: addi x2, x2, 1      # Erhöhe x2 um 1
0x0008: beq  x2, x0, -8     # Springe zurück, falls x2 == 0
0x000C: jal  x0, -12        # Endlosschleife zum Test der Sprunglogik
```
Diese kleine Schleife demonstriert die korrekte Inkrementierung und Sprunglogik des Prozessors.  
In der GTKWave-Ansicht ist zu erkennen, dass der Program Counter (`iBus_cmd_payload_pc`)  
nach jedem Befehl um vier Byte steigt, was der Befehlsbreite des RISC-V-Formats entspricht.  
Sobald der `beq`-Befehl aktiv wird, erfolgt ein Rücksprung zur Zieladresse,  
wodurch im Signalverlauf ein charakteristisches „Sägezahn“-Muster entsteht.

---

### Analyseergebnisse

Die Simulation bestätigt, dass:

- die Instruktionspipeline korrekt arbeitet,  
- der Program Counter erwartungsgemäß fortschreitet,  
- die Bus-Transaktionen synchron zu den Taktflanken erfolgen,  
- und die Speicheroperationen (`sw`, `lw`) funktional richtig sind.

Damit ist nachgewiesen, dass der mit der GUI generierte Prozessor  
vollständig lauffähig und korrekt implementiert ist.

---

### Bedeutung der Signalbeobachtung

Die Wellenformanalyse mit GTKWave ermöglicht ein tiefes Verständnis  
für das Verhalten des Prozessors auf Signalebene.  
Sie dient nicht nur der **Fehlererkennung**, sondern auch der **Leistungsoptimierung** –  
beispielsweise durch die Untersuchung von Pipeline-Hazards, Taktlatenzen oder Speicherzugriffen.

Durch die Integration in die GUI ist dieser Verifikationsprozess vollständig automatisiert:  
Nach jeder Verilog-Generierung lässt sich per Knopfdruck eine Simulation und Signalanalyse durchführen,  
ohne manuelles Eingreifen oder zusätzliche Konfigurationen.

---

### Zusammenfassung

Mit der Funktion `wave()` und der anschließenden Signalbeobachtung in **GTKWave**  
wird der letzte Schritt der Design- und Verifikationskette abgeschlossen.  
Die Möglichkeit, die interne Aktivität des Prozessors zu beobachten,  
liefert einen eindeutigen Nachweis über die Korrektheit der generierten Architektur.

Damit stellt die GUI nicht nur ein Werkzeug zur automatischen Generierung dar,  
sondern auch ein integrales System zur **funktionalen Verifikation** der CPU-Implementierung.
