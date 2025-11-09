# Systemarchitektur

Die entworfene Umgebung besteht aus zwei Hauptkomponenten:  
einem **Backend-Skript (`gui_backend.py`)** und einer **grafischen Oberfläche (Tkinter-Frontend)**.  
Beide Komponenten arbeiten eng zusammen, um den vollständigen Hardware-Generierungsprozess von der Plugin-Auswahl bis zur Simulation zu automatisieren.

---

## Gesamtüberblick


**Ablauf des Workflows:**

1. **Plugin-Auswahl** –  
   Der Benutzer wählt im GUI aus, welche VexRiscv-Plugins aktiviert werden sollen  
   (z. B. `IntAluPlugin`, `BranchPlugin`, `CsrPlugin`, `DBusSimplePlugin`).

2. **Konfigurationsspeicherung** –  
   Die Auswahl wird als JSON-Datei (`gui_config.json`) gespeichert, die vom Backend verarbeitet wird.

3. **Scala-Generierung** –  
   Das Backend erzeugt automatisch die Scala-Datei `VexRiscvTopFromGui.scala`,  
   in der die ausgewählten Plugins als Konstruktorparameter an `VexRiscvConfig` übergeben werden.

4. **Verilog-Erzeugung** –  
   Über den Aufruf `sbt "runMain vexriscv.demo.VexRiscvTopFromGui"` wird das SpinalHDL-Buildsystem gestartet,  
   welches aus der Scala-Beschreibung den Verilog-Code (`VexRiscv.v`) generiert.

5. **Simulation und Signalanalyse** –  
   Die GUI bietet Schaltflächen zum Starten der Simulation (Verilator) sowie zum Öffnen der erzeugten Wellenformdatei (`trace.vcd`) in GTKWave.

---

## Architekturkomponenten

### Backend
Das Python-Skript `gui_backend.py` übernimmt alle systemnahen Aufgaben:
- Lesen und Schreiben der JSON-Konfiguration  
- Generierung der Scala-Topdatei  
- Aufruf von **SpinalHDL/SBT** zur Verilog-Erzeugung  
- Durchführung der **Simulation** über Verilator  
- Öffnen der **GTKWave-Oberfläche**

Es ist so aufgebaut, dass es auch ohne GUI auf der Kommandozeile genutzt werden kann.

### GUI-Frontend
Das **Tkinter-Frontend** dient als Benutzeroberfläche und kommuniziert direkt mit dem Backend.  
Es bietet:
- Checkboxen zur Plugin-Auswahl  
- Schaltflächen für „Generate Verilog“, „Run Simulation“, „Open GTKWave“  
- Einen Log-Bereich zur Laufzeit-Ausgabe  
- Eine Option *„Auto-add required plugins“* (fügt automatisch essenzielle Pipeline-Plugins hinzu)  
- Einen Button *„Clear Log“* zum Zurücksetzen der Konsolenausgabe

---

## Abbildung der GUI

In der folgenden Abbildung ist die entwickelte grafische Benutzeroberfläche dargestellt.  
Über diese kann der Benutzer die gewünschten VexRiscv-Plugins auswählen, 
den Verilog-Code erzeugen, eine Simulation starten oder die Ergebnisse in **GTKWave** anzeigen.

![GUI Architektur](images/gui_overview.png)

*Abbildung 1: Grafische Benutzeroberfläche des VexRiscv-Konfigurators mit Plugin-Auswahl, Build-Steuerung und Log-Ausgabe.*

Die Oberfläche wurde mit **Python** unter Verwendung des **Tkinter-Frameworks** implementiert.  
Sie stellt die zentrale Steuerungseinheit der Designumgebung dar und bietet alle wesentlichen Funktionen für:
- die Konfiguration der Prozessor-Plugins,  
- die automatische Verilog-Generierung,  
- das Ausführen der Simulation über **Verilator**,  
- sowie die Anzeige der Signale in **GTKWave**.

---

## Datenfluss der Designumgebung

Der Gesamtprozess von der grafischen Auswahl bis zur Hardwarebeschreibung kann durch den folgenden Ablauf beschrieben werden:

```text
[GUI] 
   ↓
(gui_config.json)
   ↓
[Backend-Skript]
   ↓
[SpinalHDL / SBT] → Verilog-Generierung
   ↓
[Verilator Simulation]
   ↓
[GTKWave Analyse]
