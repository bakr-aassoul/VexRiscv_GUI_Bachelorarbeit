# Systemintegration und FPGA-Evaluierung

Nach der erfolgreichen funktionalen Verifikation auf Komponentenebene (Kapitel 6) befasst sich dieses Kapitel mit der Integration des generierten Prozessors in ein Gesamtsystem und dessen Evaluierung auf FPGA-Systemebene. Ziel ist der empirische Nachweis, dass der durch die GUI konfigurierte VexRiscv-Kern in der Lage ist, als zentraler Prozessor in einem System-on-Chip (SoC) zu agieren, komplexe Software-Stacks (BIOS) auszuführen und über standardisierte Bus-Protokolle mit Peripherie sowie Speicher zu kommunizieren.

## Integration des generierten Prozessorkerns in ein LiteX-System-on-Chip

Die Überführung eines isolierten CPU-Kerns in ein lauffähiges FPGA-Design erfordert eine tragfähige Systemumgebung. Hierfür wurde das LiteX-Framework gewählt, da es eine automatisierte Generierung der notwendigen Infrastruktur, insbesondere des Wishbone-Bus-Interconnects, des Speicher-Controllers und der UART-Kommunikationsschnittstelle, ermöglicht.

### Automatische Schnittstellen-Transformation

Eine zentrale Herausforderung bei der Integration ist die Inkompatibilität der Schnittstellen: Der VexRiscv-Kern nutzt nativ getrennte, pfeilgerichtete Ports für Instruktionen (iBus) und Daten (dBus). Das LiteX-SoC hingegen erwartet bidirektionale Master-Interfaces gemäß dem Wishbone-Standard.

Die Lösung erfolgt softwareseitig im Backend der GUI (gui_backend.py). Im sogenannten „LiteX-Mode“ wird der Scala-Code des Prozessors vor der Verilog-Generierung dynamisch modifiziert. Dies geschieht durch einen rework-Block, der direkt auf die Netzliste des SpinalHDL-Modells zugreift:

- Entkopplung: Die Methoden p.iBus.setAsDirectionLess() lösen die Ports von ihrer internen Hierarchie.

- Protokoll-Konversion: Der Aufruf toWishbone() instanziiert Adapter-Logik, die die VexRiscv-Signale in das Wishbone-Protokoll (Address, Data, Strobe, Acknowledge) übersetzt.

- Namenskonvention: Damit LiteX die Anschlüsse automatisch zuordnen kann, werden die Schnittstellen explizit in iBusWishbone und dBusWishbone umbenannt.

Dieser automatisierte „Wrapper“-Ansatz stellt sicher, dass der generierte Verilog-Code "Drop-in"-kompatibel für das SoC ist, ohne dass manuelle Eingriffe in die Hardware-Beschreibungssprache nötig sind.

### SoC-Generierung und Boot-Vorgang

Das resultierende System wurde für das Pynq-Z1 Board synthetisiert, welches auf einem Xilinx Zynq-7000 SoC (XC7Z020) basiert. Dabei wird der VexRiscv vollständig in der Programmable Logic (PL) des FPGAs implementiert.

Die erfolgreiche Systemintegration manifestiert sich im Boot-Vorgang des LiteX-BIOS. Abbildung 7.1 zeigt den UART-Output unmittelbar nach dem Reset.

**Abbildung 7.1: Boot-Log des integrierten VexRiscv-SoCs. Der Screenshot zeigt die erfolgreiche Initialisierung des Systems. Zu erkennen sind:
Die kundenspezifische Begrüßungsmeldung („Hello from Bakr's VexRiscv...“), die belegt, dass der eigene Software-Build ausgeführt wird.
Die Erkennung der CPU („VexRiscv @ 125MHz“) und des Wishbone-Busses.
Die Speicherbereiche (ROM: 32 KiB, SRAM: 8 KiB).**

Die Konsolenausgabe liefert den Nachweis für das korrekte Zusammenspiel von Hardware und Software:

- Software-Toolchain: Die Ausgabe der kundenspezifischen Nachricht („Hello from Bakr's VexRiscv...“) beweist, dass der C-Code korrekt mit dem RISC-V GCC Cross-Compiler übersetzt wurde und der Prozessor den Maschinencode interpretiert.

- Taktfrequenz: Die Erkennung von „125 MHz“ bestätigt, dass die Clock Domain Crossing und die PLL-Konfiguration des FPGAs korrekt sind.

- Speicher-Initialisierung: Die Anzeige der Speicherbereiche (ROM: 32 KiB, SRAM: 8 KiB) zeigt, dass der Wishbone-Interconnect die Adressräume korrekt mappt.

## FPGA-Implementierung mit Vivado

Die physische Umsetzung des Designs erfolgte mit der Xilinx Vivado Design Suite. In diesem Schritt durchläuft der generierte Verilog-Code die Phasen Synthese, Place & Route sowie Bitstream-Generierung.

### Hierarchie und Struktur

Die Projektstruktur in Vivado verdeutlicht die Einbettung des Softcores.

**Abbildung 7.2: Hierarchie-Ansicht im Vivado-Projekt. Man erkennt, dass der generierte Kern (VexRiscv) als Subkomponente in das Top-Level-Design des Pynq-Z1 eingebettet ist. Dies bestätigt die korrekte strukturelle Integration des Verilog-Codes.**

Wie in der Abbildung ersichtlich, fungiert das Modul digilent_pynq_z1 als Top-Level-Wrapper, der die physikalischen Pins des FPGAs definiert. Der generierte VexRiscv-Kern ist als Sub-Modul instanziiert. Diese strikte Kapselung ermöglicht es, den Prozessorkern bei Bedarf neu zu generieren (z. B. mit anderen Plugins), ohne das gesamte SoC-Layout in Vivado ändern zu müssen.

### Timing und Ressourcen

Die Implementierung konnte erfolgreich abgeschlossen werden. Besonders hervorzuheben ist das Timing Closure: Das Design erreichte die Ziel-Systemfrequenz von 125 MHz ohne negative Slack-Werte (Setup/Hold-Time Violations). Dies indiziert, dass die durch SpinalHDL erzeugte Pipeline-Struktur effizient genug ist, um auf dem Artix-7-Fabric des Pynq-Z1 mit hoher Geschwindigkeit betrieben zu werden.

## Hardware-Tests und Speicherzugriffe
Um die Integrität der Datenbus-Anbindung (dBusWishbone) zu verifizieren, wurden manuelle Speicherzugriffe über die LiteX-Konsole durchgeführt. Dabei wurde geprüft, ob Daten korrekt in den SRAM geschrieben und wieder gelesen werden können.

### Schreib- und Lesetest (Memory R/W)

Zur Überprüfung des Arbeitsspeichers (SRAM) wurden Testmuster geschrieben und zurückgelesen.

**Abbildung 7.3: Verifikation der Speicherzugriffe über die Konsole.
Schreibvorgang: Es wurde der Wert 0xAABBCCDD an die Adresse 0x10000004 geschrieben.
Lesevorgang: Der Rückgabewert lautet dd cc bb aa.**

- Schreibvorgang: Der Befehl mem_write schrieb den hexadezimalen Wert 0xAABBCCDD an die Speicheradresse 0x10000004. Diese Adresse liegt im Basisbereich des SRAMs (Offset 0x4), wie im Memory-Map des SoCs definiert.

- Lesevorgang: Der Befehl mem_read lieferte die Datenbytes zurück.
  
**Analyse der Byte-Reihenfolge (Endianness):** 

Das Ergebnis in Abbildung 7.3 demonstriert eine fundamentale Eigenschaft der RISC-V-Architektur: Little-Endian. Der 32-Bit-Wert 0xAABBCCDD wird byteweise so abgelegt, dass das niedrigstwertige Byte (0xDD) an der niedrigsten Adresse gespeichert wird. Die Konsolenausgabe dd cc bb aa bestätigt, dass die gesamte Kette, vom VexRiscv-Core über den Wishbone-Adapter bis zum Speichercontroller, die Byte-Reihenfolge (Byte Ordering) korrekt handhabt.

### Adressraum-Validierung

Ein ergänzender Test prüfte das Verhalten bei Zugriffen auf nicht definierte Speicherbereiche (Out-of-Bounds Access).

**Abbildung 7.4: Zugriff auf undefinierte Speicherbereiche. Ein Lesezugriff auf die Adresse 0x82001000 (außerhalb des definierten SRAMs) liefert ff ff ff ff. Dies ist das erwartete Verhalten für einen leeren Bus, da keine Komponente antwortet (Open Bus).**

Ein Lesezugriff auf 0x82001000 (außerhalb des SRAM-Adressraums) liefert ff ff ff ff. Dies entspricht dem erwarteten Verhalten eines offenen Busses (Open Bus) im Wishbone-Standard, da kein Slave das Acknowledge-Signal sendet. Dieser Test bestätigt, dass der Adress-Decoder des SoCs fehlerhafte Zugriffe korrekt isoliert und das System nicht zum Absturz bringt.

## Fazit der Evaluierung

Die FPGA-basierte Evaluierung erbrachte den empirischen Nachweis der Systemreife des entwickelten Designs. Das System bootet zuverlässig, führt das LiteX-BIOS aus und demonstriert damit das korrekte Zusammenwirken von Fetch-Pfad, Kontrollfluss-Logik und Speicherzugriff. Gleichzeitig validiert der erfolgreiche Betrieb die im Backend implementierte automatisierte Schnittstellen-Transformation, welche eine nahtlose Einbindung des VexRiscv-Kerns in die Wishbone-basierte LiteX-Systemarchitektur ermöglicht. 
Der abgeschlossene Timing-Closure-Prozess bei 125 MHz sowie die konsistenten Speicher-Lese-/Schreibtests bestätigen die funktionale und zeitliche Stabilität des generierten Designs. Insgesamt zeigt die Evaluierung, dass die entwickelte GUI nicht nur als Simulationswerkzeug dient, sondern synthetisierbaren, in realen System-on-Chip-Umgebungen lauffähigen Hardware-Code erzeugt.
