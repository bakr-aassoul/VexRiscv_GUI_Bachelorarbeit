# GUI-Implementierung


```{raw} latex
\large
```
In diesem Abschnitt wird die Implementierung der im Rahmen dieser Arbeit entwickelten grafischen Benutzeroberfläche beschrieben. 
Ziel der GUI ist es, die Konfiguration und Generierung des VexRiscv-Prozessors deutlich zu vereinfachen und Anwenderinnen und Anwendern eine intuitive Möglichkeit zu bieten, unterschiedliche Architekturvarianten zu erstellen und zu evaluieren. Die GUI bildet damit die zentrale Interaktionsschicht des gesamten Systems und vereint sowohl Eingabe- als auch Automatisierungslogik in einer einzigen Anwendung.

```{raw} latex
\clearpage
```
---

```{raw} latex
\normalsize
```

## Konzeption und Aufbau der Benutzeroberfläche

Die Implementierung der grafischen Benutzeroberfläche basiert auf **Python 3**  
und verwendet das **Tkinter-Framework**. 
Diese Wahl ermöglicht eine plattformunabhängige Ausführung und eine vergleichsweise einfache Gestaltung von Eingabeelementen, Menüstrukturen und Dialogen. 
Der Aufbau der Oberfläche folgt einem klaren, modularen Design: 
Die einzelnen Prozessorkomponenten und Plugins werden in logisch getrennten Bereichen dargestellt, sodass die Benutzerführung übersichtlich bleibt und die Konfigurationsschritte intuitiv nachvollzogen werden können. 
Jede auswählbare Komponente entspricht einem Plugin des VexRiscv-Prozessors, wodurch die Struktur der GUI direkt die modulare Architektur des Prozessorkerns widerspiegelt.

Das Gesamtsystem besteht aus zwei klar getrennten Teilen:

- dem **Backend-Skript** `gui_backend.py`, das die eigentliche Logik, Dateigenerierung und Simulation steuert,  
- dem **Frontend (GUI)**, das die Bedienoberfläche darstellt und alle Funktionen über Buttons und Checkboxen zugänglich macht.

```{raw} latex
\clearpage
```

## Frontend-Struktur (main.py)

Der Einstiegspunkt der Anwendung lädt zunächst die Konfiguration und baut anschließend dynamisch die Oberfläche auf. 
Der folgende Auszug zeigt, wie die GUI zu Beginn die gespeicherten Einstellungen aus dem Backend lädt:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: 

import gui_backend as be
cfg = be.load_config()     # lädt Plugins, Pfade, LiteX-Mode, Auto-Complete
```

```{raw} latex
\end{minipage}
```


Die Plugin-Auswahl wird dynamisch aus einer Liste erzeugt. Jede Option wird an eine BooleanVar gebunden, sodass die GUI später den Zustand aller Checkboxen auslesen kann:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: 

plugin_vars = {}
for name in plugin_names:
    var = BooleanVar(value=(name in cfg["plugins"]))
    ttk.Checkbutton(frm_plugins, text=name, variable=var).pack(anchor="w")
    plugin_vars[name] = var
```

```{raw} latex
\end{minipage}
```

Dieser Code zeigt, wie die GUI den Nutzerentscheid direkt in Python-Variablen abbildet und damit eine Basis für die spätere Codegenerierung schafft.

Der Log-Bereich wird als Textfeld implementiert. Die Methode append_log() fügt neue Nachrichten hinzu und hält den Scrollbereich immer am Ende:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: 

def append_log(msg: str):
    log.insert("end", msg + "\n")
    log.see("end")
```

```{raw} latex
\end{minipage}
```

Dadurch verhält sich der Log ähnlich wie eine klassische Build-Konsole.

```{raw} latex
\clearpage
```

## Ereignissteuerung und Threading

Rechenintensive Aufgaben wie SBT-Builds oder Verilator-Simulationen blockieren eine Tkinter-GUI normalerweise vollständig. In dieser Anwendung wird das durch Threading gelöst:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: 

def run_in_thread(fn):
    def worker():
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                fn()               # führt Backend-Funktion aus
            append_log(buf.getvalue())
        finally:
            set_buttons_state(True)
    
    set_buttons_state(False)
    threading.Thread(target=worker).start()
```

```{raw} latex
\end{minipage}
```
Wichtige Mechanismen:
- **redirect_stdout** fängt alle print()-Ausgaben aus dem Backend ab
- **StringIO** Buffer speichert diese Ausgabe
- **append_log** leitet alles in das GUI-Log weiter
- Buttons werden während der Ausführung deaktiviert, danach wieder aktiviert

Dieser Mechanismus sorgt dafür, dass die GUI nie einfriert.

```{raw} latex
\clearpage
```
## Backend-Logik & Plugins (gui_backend.py)

Alle Plugins des VexRiscv werden im Backend als Mapping von Namen zu Scala-Konstruktoren hinterlegt:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: 

PLUGIN_CTORS = {
    "IBusSimplePlugin": "new IBusSimplePlugin(resetVector=0x00000000l)",
    "RegFilePlugin": "new RegFilePlugin(regFileReadyKind=SYNC)",
    "MulPlugin": "new MulPlugin",
    "DivPlugin": "new DivPlugin",
    ...
}
```

```{raw} latex
\end{minipage}
```

Dadurch kann das Backend später automatisch gültige Scala-Deklarationen erzeugen.
Wenn ein Benutzer z. B. „DivPlugin“ aktiviert, erzeugt das Backend eine Zeile wie:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: 

plugins = List(
    new IBusSimplePlugin(...),
    new RegFilePlugin(...),
    new DivPlugin()
)
```

```{raw} latex
\end{minipage}
```

Ein weiteres zentrales Snippet ist die Konfigurationsverwaltung:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: 

def load_config():
    if CFG.exists():
        return json.loads(CFG.read_text())
    return {"plugins": [], "path": str(DEFAULT_OUT), "complete": False, "litex_mode": False}
```

```{raw} latex
\end{minipage}
```
Damit bleibt die gesamte GUI zwischen Sitzungen konsistent.

```{raw} latex
\clearpage
```

## Generierung der Scala-Topdatei

Die wichtigste Funktion im Backend ist **write_top()**, welche den kompletten VexRiscv-Code erzeugt:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: 

def write_top(selected, litex_mode):
    ctor_list = [PLUGIN_CTORS[name] for name in selected]
    ctor_str  = ",\n      ".join(ctor_list)

    scala_code = f"""
import spinal.core._
import vexriscv._

object VexRiscvTopFromGui {{
  def main(args: Array[String]) {{
    SpinalConfig(targetDirectory="{DEFAULT_OUT}").generateVerilog(new VexRiscv(
      plugins = List(
        {ctor_str}
      )
    ))
}}
}}
"""
    LAUNCHER.write_text(scala_code)
    return LAUNCHER

```

```{raw} latex
\end{minipage}
```
Hier passiert Folgendes:

- Die ausgewählten Plugins werden in echte Scala-Klassen umgewandelt
- Eine komplette Datei **VexRiscvTopFromGui.scala** wird generiert
- Diese Datei enthält eine sofort lauffähige **generateVerilog()**-Instruktion
- SpinalHDL übersetzt später genau diese Datei in Verilog

```{raw} latex
\clearpage
```
## Build- und Simulationsablauf

Die Funktion generate() steuert den gesamten Buildprozess:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: 

def generate(selected_plugins, litex_mode):
    write_top(selected_plugins, litex_mode)
    run('sbt "runMain VexRiscvTopFromGui"', cwd=ROOT)
```

```{raw} latex
\end{minipage}
```

Die Simulation wird über Verilator umgesetzt:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: 

def simulate():
    generate_if_needed()
    run(f"verilator --cc {verilog} --exe sim_main.cpp -o simv")
    run("make -C obj_dir -f VexRiscv.mk")
    run("./obj_dir/simv")
```

```{raw} latex
\end{minipage}
```

Die Wellenform wird anschließend geöffnet:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: 

def wave():
    run(f'gtkwave "{paths["vcd"]}" &')
```

```{raw} latex
\end{minipage}
```

Damit bildet das Backend die gesamte technische Toolchain ab:

- Scala-Generierung
- SBT-Kompilierung
- Verilog-Übersetzung
- Simulation
- Wellenform-Analyse

```{raw} latex
\clearpage
```

## Zusammenfassung

Die GUI vereint zwei komplementäre Komponenten zu einer vollständigen, benutzerfreundlichen Entwicklungsumgebung. 
Das Frontend in main.py übernimmt die Benutzerinteraktion, das Threading und die Live-Protokollierung aller Systemausgaben, während das Backend in gui_backend.py die technische Umsetzung der Prozessorerzeugung, einschließlich Codegenerierung, Plugin-Mapping und der Integration in die Build- und Simulationswerkzeuge, realisiert. 
Durch dieses Zusammenspiel wird eine Plattform geschaffen, die es ermöglicht, den VexRiscv-Prozessor zu konfigurieren, zu generieren und zu testen, ohne dass tiefgehende Kenntnisse über SpinalHDL oder die darunterliegende Toolchain erforderlich sind. 
Damit stellt die entwickelte GUI einen zentralen Beitrag dieser Arbeit dar, da sie den gesamten Workflow wesentlich vereinfacht und eine systematische Exploration verschiedener Prozessorarchitekturen ermöglicht.
