# GUI-gestützte Prozessorerzeugung


```{raw} latex
\large
```
Dieses Kapitel dokumentiert die softwareseitige Implementierung der Entwicklungsumgebung. Es beschreibt den Aufbau der grafischen Benutzeroberfläche (Frontend), die interne Verarbeitungslogik (Backend) sowie die Schnittstelle zur SpinalHDL-Toolchain.

Ein besonderer Fokus liegt auf dem Custom ALU Generator. Es wird detailliert erläutert, wie Benutzereingaben geparst, validiert und dynamisch in synthetisierbaren Scala-Quellcode übersetzt werden. Dies ermöglicht die Transformation des VexRiscv von einem statischen Modell zu einem durch den Anwender erweiterbaren Prozessorsystem.

```{raw} latex
\clearpage
```
---

```{raw} latex
\normalsize
```

## Konzeption und Aufbau der Benutzeroberfläche

Die Benutzeroberfläche wurde mit dem Ziel entwickelt, die Komplexität der darunterliegenden Hardwarebeschreibung zu kapseln. Die GUI ist in Python implementiert und nutzt moderne Bibliotheken zur Darstellung der Steuerelemente.

Der Aufbau gliedert sich in drei funktionale Bereiche:

- Basiskonfiguration: Auswahl der Architektur-Features über Checkboxen (z. B. Multiplikator, Divider, Caches). Hierbei werden logische Abhängigkeiten (Constraints) automatisch geprüft.

- Custom Instruction Designer: Ein dedizierter Bereich zur Definition eigener Hardware-Erweiterungen. Hier können Opcode, Instruktionsname und die funktionale Logik (z. B. arithmetische Operationen) eingegeben werden.

- Build-Steuerung: Schaltflächen zum Starten der Generierung, Synthese und Simulation sowie Statusanzeigen für den Fortschritt der externen Prozesse (SBT, Verilator).

**ABBILDUNG 5.1 Screenshot der Benutzeroberfläche mit konfigurierter Custom ALU**

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
:caption: Laden der Konfiguration im Frontend

import gui_backend as be
from plugin_registry import PLUGIN_PARAM_REGISTRY
cfg = be.load_config()  # Plugins, Custom-ALUs,
# Instanzen, Auto-Complete, LiteX-Mode
```

```{raw} latex
\end{minipage}
```

**Dynamische Plugin-Konfiguration**

Die Plugin-Auswahl wird dynamisch aus einer Liste erzeugt. Jede Option wird an eine BooleanVar gebunden, sodass die GUI später den Zustand aller Checkboxen auslesen kann:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: Erzeugung der Plugin-Auswahlelemente

vars_by_name = {}
for i, name in enumerate(plugin_names):
    v = tk.BooleanVar(value=(name in cfg["plugins"]))
    vars_by_name[name] = v
    ttk.Checkbutton(grid, text=name, variable=v)\
        .grid(row=i//2, column=i%2, sticky="w", padx=(0, 24))
```

```{raw} latex
\end{minipage}
```

Dieser Code zeigt, wie die GUI den Nutzerentscheid direkt in Python-Variablen abbildet und damit eine Basis für die spätere Code- und Plugin-Generierung schafft.

Der Auto-Complete-Mechanismus ergänzt fehlende Pflicht-Plugins und stellt sicher, dass ausschließlich architektonisch gültige CPU-Konfigurationen erzeugt werden.

**Thread-sichere Laufzeitprotokollierung**

Der Log-Bereich wird als Textfeld implementiert. Die Methode append_log() fügt neue Nachrichten hinzu und hält den Scrollbereich immer am Ende:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: Thread-sichere Protokollierung

def append_log(msg: str):
    def _do():
        txt.insert("end", msg)
        txt.see("end")
    root.after(0, _do)
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
:caption: Hintergrundausführung langer Operationen

def run_in_thread(fn):
    def target():
        try:
            with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                fn()
                out = buf.getvalue()
            append_log(out if out else "[done]\n")
        except Exception as e:
            append_log(repr(e) + "\n")
            messagebox.showerror("Error", repr(e))
        finally:
            set_buttons_state(True)

    set_buttons_state(False)
    threading.Thread(target=target, daemon=True).start()
```

```{raw} latex
\end{minipage}
```
Wichtige Mechanismen:
- **redirect_stdout** sammelt Backend-Ausgaben zentral ein
- **StringIO** Buffer speichert diese Ausgabe
- **append_log** überträgt diese Meldungen in den Logbereich
- Buttons werden während der Ausführung deaktiviert, danach wieder aktiviert

Auf diese Weise bleibt die GUI auch während länger laufender Toolchain-Schritte responsiv.

```{raw} latex
\clearpage
```
## Backend-Logik & Plugin-System (gui_backend.py)

### Plugin-Konstruktor-Registry

Alle Plugins des VexRiscv werden im Backend als Mapping von Namen zu Scala-Konstruktoren hinterlegt:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: Mapping der Plugin-Konstruktoren

PLUGIN_CTORS = {
    "IBusSimplePlugin": "new IBusSimplePlugin(resetVector=0x00000000l)",
    "RegFilePlugin": "new RegFilePlugin(regFileReadyKind=SYNC)",
    "MulPlugin": "new MulPlugin",
    "DivPlugin": "new DivPlugin",
    # weitere Plugins ...
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
:caption: Automatisch generierte Plugin-List

plugins = List(
    new IBusSimplePlugin(...),
    new RegFilePlugin(...),
    ...
    new DivPlugin()
)
```

```{raw} latex
\end{minipage}
```

### Parametrierbare Plugin-Instanzen (plugin_registry.py)

Neben der reinen Ein-/Auswahl über Checkboxen unterstützt das System parametrisierbare Plugin-Instanzen. Hierzu wird eine separate Registry verwendet, die den Aufbau der Parameter beschreibt:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: Parametrisierung über plugin\_registry.py

from dataclasses import dataclass
from typing import Any, Optional, List, Dict

@dataclass(frozen=True)
class ParamSpec:
    typ: str                 # "bool", "int", "hex_long", "enum", "string", "null"
    default: Any = None
    allowed: Optional[List[str]] = None   # für Enums
    nullable: bool = False
    min: Optional[int] = None
    max: Optional[int] = None

PLUGIN_PARAM_REGISTRY: Dict[str, Dict[str, ParamSpec]] = {
    "IBusSimplePlugin": {
        "resetVector": ParamSpec("hex_long", default="0x00000000l"),
        "cmdForkOnSecondStage": ParamSpec("bool", default=False),
        # weitere Parameter ...
    },
    "BranchPlugin": {
        "earlyBranch": ParamSpec("bool", default=True),
        "catchAddressMisaligned": ParamSpec("bool", default=False),
    },
    # weitere Plugins ...
}
```

```{raw} latex
\end{minipage}
```

Im Frontend wird auf Basis dieser Registry dynamisch ein Formular aufgebaut („Custom plugin instances (normal mode)“), in dem der Benutzer für eine gewählte Plugin-Klasse konkrete Parameterwerte festlegen kann. Diese Instanzen werden als *custom_instances* in der Konfiguration gespeichert und von *write_top()* später in konkrete Scala-Konstruktoren übersetzt.

```{raw} latex
\clearpage
```

### Konfigurationsverwaltung
Ein weiteres zentrales Snippet ist die Konfigurationsverwaltung:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: Laden der Konfiguration

def load_config():
    try:
        with open(CFG) as f:
            d = json.load(f)
    except Exception:
        d = {}

    return {
        "plugins":          d.get("plugins", []),
        "custom_alus":      d.get("custom_alus", []),
        "custom_instances": d.get("custom_instances", []),
        "out_dir":          d.get("out_dir", DEFAULT_OUT),
        "auto_complete":    bool(d.get("auto_complete", True)),
        "litex_mode":       bool(d.get("litex_mode", False))
    }
```

```{raw} latex
\end{minipage}
```
Damit bleibt die gesamte GUI zwischen Sitzungen konsistent.

```{raw} latex
\clearpage
```
### Implementierung des Custom ALU Generators

Die Kerninnovation dieser Arbeit ist die dynamische Erzeugung von Hardware-Code. Während Standard-Plugins lediglich instanziiert werden, muss für Custom Instructions neuer Scala-Quellcode generiert werden. Dies erfolgt über eine Template-Engine im Backend.

Die Funktion write_custom_alu_file baut das Scala-Plugin schrittweise auf. Zunächst wird der Kopf der Klasse und die Decoder-Konfiguration definiert. Hier wird das Bitmuster der Instruktion festgelegt:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: Generator Teil 1: Decoder-Setup

def write_custom_alu_file(name: str, opcode_suffix: str, logic_body: str):
   # Einrückung für den Scala-Code vorbereiten
    indented_logic = "\n          ".join(logic_body.splitlines())
    # Template für ein VexRiscv-Plugin (Teil 1: Setup)
    scala_code = f"""
package vexriscv.demo
import spinal.core._
import spinal.lib._
import vexriscv._
import vexriscv.plugin._

class {name} extends Plugin[VexRiscv] {{
  object IS_{name.upper()} extends Stageable(Bool)

  override def setup(pipeline: VexRiscv): Unit = {{
    import pipeline.config._
    // Opcode pattern: 0000000----------000-----{opcode_suffix}
    val instructionPattern = M"0000000----------000-----{opcode_suffix}"
    val decoderService = pipeline.service(classOf[DecoderService])

    decoderService.add(
      key = instructionPattern,
      values = List(
        IS_{name.upper()}        -> True,
        REGFILE_WRITE_VALID      -> True,
        BYPASSABLE_EXECUTE_STAGE -> True,
        BYPASSABLE_MEMORY_STAGE  -> True,
        RS1_USE                  -> True,
        RS2_USE                  -> True
      )
    )
  }}
"""
```

```{raw} latex
\end{minipage}
```
Dieser Abschnitt nutzt den *DecoderService*, um die Pipeline für den neuen Opcode zu konfigurieren. Das *instructionPattern* maskiert die Operanden-Bits (mit -), sodass nur der Opcode und das Suffix gematcht werden. Die Liste *values* definiert das Verhalten der CPU:

- *IS_NAME*: Markiert die Instruktion als aktiv in der Pipeline.

- *REGFILE_WRITE_VALID*: Signalisiert, dass ein Ergebnis in das Registerfile zurückgeschrieben wird.

- *RS1_USE / RS2_USE*: Veranlasst das Lesen der Quellregister, bevor die Execute-Stufe erreicht wird.

Im zweiten Schritt wird die eigentliche Hardware-Logik in die Execute-Stufe der Pipeline injiziert. Hier wird der vom Benutzer eingegebene Logik-String (*indented_logic*) in die Hardware-Beschreibung eingefügt:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: Generator Teil 2: Logik-Injection und File-IO

    # Fortsetzung des Templates (Teil 2: Build & Injection)
    scala_code += f"""
  override def build(pipeline: VexRiscv): Unit = {{
      import pipeline._
      import pipeline.config._
      execute plug new Area {{
          import execute._
          val rs1 = input(RS1)
          val rs2 = input(RS2)
          // Injection der User-Logik
          {indented_logic}
          
          when(input(IS_{name.upper()})) {{
             output(REGFILE_WRITE_DATA) := result.asBits
          }}
      }}
  }}
}}
"""
    demo_dir = os.path.dirname(LAUNCHER)
    filename = os.path.join(demo_dir, f"{name}.scala")
   
    with open(filename, "w") as f:
        f.write(scala_code)
```

```{raw} latex
\end{minipage}
```


Die eigentliche Rechenlogik wird schließlich über *execute plug new Area* direkt in die Execute-Stufe der CPU injiziert. Dies ist ein „Hardware-Injection“-Pattern: Der Scala-Code der *logic_body*-Variable (z. B. *rs1 + rs2*) wird an dieser Stelle als Hardware-Schaltung instanziiert. Das Ergebnis wird auf den *REGFILE_WRITE_DATA*-Pfad gelegt, wodurch es im WriteBack-Stage im Zielregister landet. Durch diesen Aufbau garantiert der Generator, dass die benutzerdefinierte Logik vollzyklisch in die Pipeline integriert ist, ohne Timing-Probleme oder Ressourcenkonflikte mit der Standard-ALU zu verursachen.

### Generierung der Scala-Topdatei

Die Funktion write_top() fungiert als Orchestrator des Generierungsprozesses. Ihre Aufgabe ist es, die abstrakte Konfiguration aus der Python-Umgebung in eine valide, kompilierbare Scala-Anwendung zu überführen, die anschließend von der SpinalHDL-Toolchain ausgeführt werden kann.

Dieser Prozess verläuft in drei logischen Phasen:

- **Materialisierung der Custom-Instruktionen:** Zunächst iteriert das Backend über alle definierten Custom ALUs. Für jede ALU wird die in Abschnitt 5.5 beschriebene Funktion write_custom_alu_file() aufgerufen, um die logische Definition in eine physische .scala-Quelldatei im Projektverzeichnis zu schreiben. Erst durch diesen Schritt stehen die neuen Klassen dem Build-System zur Verfügung.

- **Aggregation der Komponenten:** Im nächsten Schritt wird die vollständige Liste der CPU-Plugins zusammengestellt. Hierbei werden die Standard-Plugins (basierend auf der Checkbox-Auswahl) und die Konstruktoren der soeben generierten Custom-ALU-Klassen (new MyAlu()) zu einer gemeinsamen Liste vereinigt. Das Backend stellt dabei sicher, dass die Reihenfolge der Plugins den Anforderungen des VexRiscv-Frameworks entspricht.

- **Synthese des Entry-Points:** Abschließend generiert die Funktion den eigentlichen Einstiegspunkt für das Build-System: das Scala-Singleton-Objekt VexRiscvTopFromGui. Diese Datei enthält die main-Methode, welche die VexRiscv-Klasse mit der konfigurierten Plugin-Liste instanziiert und den Aufruf SpinalConfig(...).generateVerilog(...) ausführt.

Durch diesen Ansatz wird die Python-Laufzeitumgebung sauber von der JVM-basierten Hardware-Generierung entkoppelt. Das Python-Skript erzeugt lediglich den Quellcode, während SBT und SpinalHDL im anschließenden Schritt die eigentliche Elaborierung der Schaltung übernehmen.

Zuerst iteriert die Funktion über alle definierten Custom-ALUs und materialisiert diese als physische Dateien auf der Festplatte. Gleichzeitig werden die Konstruktoren (new MyAlu()) für die Plugin-Liste vorbereitet: 

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: Top-Level Teil 1: Materialisierung der ALUs

def write_top(selected_plugins, litex_mode: bool):
    cfg = load_config()
    custom_alus = cfg.get("custom_alus", [])

    # 1. Generiere alle Custom-ALU Dateien
    custom_alu_constructors = []
    for alu in custom_alus:
        name = alu.get("name")
        opcode = alu.get("opcode")
        logic = alu.get("logic")
        if name and opcode and logic:
            write_custom_alu_file(name, opcode, logic)
            custom_alu_constructors.append(f"new {name}()")
```

```{raw} latex
\end{minipage}
```

Im nächsten Schritt wird der Scala-Quellcode zusammengesetzt. Die Standard-Plugins und die neu erzeugten Custom-Plugins werden zu einer gemeinsamen Liste vereint und in die VexRiscvConfig injiziert:
```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python

:linenos:
:caption: Top-Level Teil 2: Aggregation und Entry-Point

    if not litex_mode:
        # 2. Kombiniere Standard- und Custom-Plugins
        ordered_keys = order_plugins(list(by_class.keys()))
        standard_plugin_lines = [by_class[p] for p in ordered_keys]

        all_plugin_lines = standard_plugin_lines + custom_alu_constructors
        full_plugin_list_str = ",\n      ".join(all_plugin_lines)

        body = f"""\
    val cpuConfig = VexRiscvConfig(plugins = List(
       {full_plugin_list_str}
    ))
    SpinalConfig(targetDirectory = "{out_dir}").generateVerilog(
      new VexRiscv(cpuConfig)
    )
    """
    else:
       # (Code für LiteX-Mode und Wishbone-Busanbindung...)
       pass 

    # 3. Erzeuge den finalen Scala-Code
    scala = f"""
package vexriscv.demo
import vexriscv._; import vexriscv.plugin._
import spinal.core._; import spinal.lib._

object VexRiscvTopFromGui {{
  def main(args: Array[String]) {{
    {body}
  }}
}}
"""
    with open(LAUNCHER, "w") as f:
        f.write(scala)

```

```{raw} latex
\end{minipage}
```

```{raw} latex
\clearpage
```
### LiteX-Mode und Wishbone-Busanbindung

Für die Integration des erzeugten Prozessors in ein LiteX-SoC reicht es nicht aus, lediglich eine feste, kompatible Plugin-Liste zu verwenden. LiteX basiert intern auf einem Wishbone-Bus, während die VexRiscv-Plugins ihre eigenen Bus-Schnittstellen (z. B. `iBus` und `dBus`) bereitstellen. Damit LiteX den Prozessor als Wishbone-Master einbinden kann, müssen diese internen Busse in Wishbone-Interfaces konvertiert und entsprechend benannt werden.

Genau dies geschieht im LiteX-Mode im Rahmen eines `rework`-Blocks im generierten Scala-Code:
```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: Wishbone-Anbindung im LiteX-Mode (Scala)
else:
     body = f"""\
SpinalConfig(targetDirectory = "{out_dir}" ).generateVerilog {
  val cpuConfig = VexRiscvConfig(plugins = List(
    /* LITEX\_FIXED Pluginliste, u. a. IBusCachedPlugin, DBusCachedPlugin */
  ))

  val cpu = new VexRiscv(cpuConfig)

  cpu.rework {
    for (p <- cpuConfig.plugins) p match {
      case p: IBusCachedPlugin =>
        p.iBus.setAsDirectionLess()
        master(p.iBus.toWishbone()).setName("iBusWishbone")

      case p: DBusCachedPlugin =>
        p.dBus.setAsDirectionLess()
        master(p.dBus.toWishbone()).setName("dBusWishbone")

      case _ =>
    }
  }

  cpu
}
"""

```

```{raw} latex
\end{minipage}
```

Die Integration des generierten Prozessors in ein LiteX-SoC stellt besondere Anforderungen an die Hardwareschnittstellen, die über die bloße Auswahl von Plugins hinausgehen. Während VexRiscv intern eigene Schnittstellenprotokolle für Instruktions- und Datenbusse verwendet, basiert die LiteX-Systemarchitektur primär auf dem Wishbone-Standard. Damit der VexRiscv-Kern als Master in diesem Bus-System agieren kann, ist eine explizite Adaptierung der Schnittstellen notwendig.

Im LiteX-Mode der GUI wird dieser Prozess automatisiert. Um eine stabile SoC-Integration zu gewährleisten, wird zunächst die freie Plugin-Wahl durch eine vordefinierte, validierte Konfiguration (*LITEX_FIXED*) ersetzt, die unter anderem Caches (Instruction- und Data-Cache) beinhaltet.

Der entscheidende technische Schritt erfolgt jedoch nach der Initialisierung der CPU im sogenannten rework-Block des generierten Scala-Codes. Dieser Mechanismus erlaubt es, die Hardware-Struktur nachträglich zu modifizieren, bevor der Verilog-Code erzeugt wird. Das Backend iteriert dabei über die konfigurierten Plugins und identifiziert die Bus-Schnittstellen:

- **Entkopplung:** Die internen Interfaces (*p.iBus*, *p.dBus*) werden mittels *setAsDirectionLess()* von ihrer ursprünglichen Hierarchie gelöst.
- **Transformation:** Die Methode *toWishbone()* konvertiert die nativen VexRiscv-Schnittstellen in standardkonforme Wishbone-Signale (Adress-, Daten-, Strobe- und Acknowledge-Leitungen).
- **Benennung:** LiteX setzt spezifische Signalnamen voraus, um die CPU-Ports automatisch mit dem System-Interconnect verbinden zu können. Daher werden die neuen Wishbone-Master explizit als *iBusWishbone* (für Befehle) und dBusWishbone (für Daten) benannt.

Ohne diesen Transformationsschritt würde der generierte Prozessor zwar intern korrekt arbeiten, besäße jedoch keine kompatiblen Anschlüsse, um mit dem Speichercontroller oder der Peripherie des LiteX-SoCs zu kommunizieren. Der LiteX-Mode stellt somit sicher, dass der generierte Verilog-Kern "Drop-in"-kompatibel für die FPGA-Gesamtsysteme ist.


### Build- und Simulationsablauf

Die Funktion generate() steuert den gesamten Buildprozess:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: Starten der Codegenerierung

def generate():
    _, verilog, _ = get_paths()
    selected = read_selected()
    cfg = load_config()
    litex_mode = cfg.get("litex_mode", False)
    write_top(selected, cfg["litex_mode"])
    run('sbt "runMain vexriscv.demo.VexRiscvTopFromGui"', cwd=ROOT)
    run(f'ls -lh "{verilog}"')
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
:caption: Starten der Simulation

def simulate():
    # Pfad zur C++ Testbench
    out_dir, verilog, vcd = get_paths()
    tb = os.path.join(ROOT, "tb_gui.cpp")

    if not os.path.exists(verilog):
        generate()
    
    # Verilator Aufruf
    run(f'verilator -cc "{verilog}" --exe "{tb}" --trace -Wno-WIDTH --build -o simv', cwd=ROOT)
    
    # Ausführen der Simulation
    os.makedirs(out_dir, exist_ok=True)
    run(f'./obj_dir/simv "{vcd}"', cwd=ROOT)
```

```{raw} latex
\end{minipage}
```

Die resultierende Wellenform kann direkt visualisiert werden:

```{raw} latex
\begin{minipage}{\linewidth}
```

```{code-block} python
:linenos:
:caption: Öffnen der Wellenform

def wave():
    _, _, vcd = get_paths()
    run(f'gtkwave "{vcd}" &', cwd=ROOT, check=False)
```

```{raw} latex
\end{minipage}
```

Damit bildet das Backend die gesamte technische Toolchain ab:

- Scala-Generierung
- SBT-Kompilierung
- Verilog-Übersetzung
- Simulation mit verilator
- Wellenform-Analyse mit GTKWave

```{raw} latex
\clearpage
```

## Zusammenfassung

Die GUI vereint zwei komplementäre Komponenten zu einer vollständigen, benutzerfreundlichen Entwicklungsumgebung. 
Das Frontend in main.py übernimmt die Benutzerinteraktion, das Threading und die Live-Protokollierung aller Systemausgaben, während das Backend in gui_backend.py die technische Umsetzung der Prozessorerzeugung, einschließlich Codegenerierung, Plugin-Mapping und der Integration in die Build- und Simulationswerkzeuge, realisiert. 
Durch dieses Zusammenspiel wird eine Plattform geschaffen, die es ermöglicht, den VexRiscv-Prozessor zu konfigurieren, zu generieren und zu testen, ohne dass tiefgehende Kenntnisse über SpinalHDL oder die darunterliegende Toolchain erforderlich sind. 
Damit stellt die entwickelte GUI einen zentralen Beitrag dieser Arbeit dar, da sie den gesamten Workflow wesentlich vereinfacht und eine systematische Exploration verschiedener Prozessorarchitekturen ermöglicht.
