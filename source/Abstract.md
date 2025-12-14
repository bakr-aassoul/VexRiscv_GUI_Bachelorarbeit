Diese Bachelorarbeit beschäftigt sich mit der Konfiguration, Simulation und FPGA-basierten Evaluierung eines modularen RISC-V-Prozessors auf Basis des in SpinalHDL entwickelten VexRiscv-Kerns. 
Ziel der Arbeit ist die Entwicklung einer grafischen Benutzeroberfläche, die es ermöglicht, den Prozessor über ein flexibles Plugin-System zu konfigurieren und automatisch bis hin zu einem lauffähigen, System-on-Chip-fähigen Verilog-Design zu generieren. 
Die GUI abstrahiert die Komplexität der zugrunde liegenden Toolchain und führt Anwender schrittweise durch den gesamten Entwicklungsprozess, von der Auswahl der Architekturkomponenten über die Codegenerierung bis zur Simulation.

Zur funktionalen Überprüfung der erzeugten Prozessorkonfigurationen wird eine RTL-Simulation mit Verilator durchgeführt, deren Signalverläufe anschließend mit GTKWave analysiert werden. 
Aufbauend darauf erfolgt die Integration des generierten Prozessorkerns in ein LiteX-System-on-Chip, einschließlich der automatischen Erzeugung der für die FPGA-Implementierung erforderlichen Dateien, sowie die Implementierung auf einem Pynq-Z1-FPGA. Dadurch wird eine Evaluierung unter realen Hardwarebedingungen ermöglicht.

Die Ergebnisse zeigen, dass sich der VexRiscv durch die modulare Architektur und die entwickelte GUI effizient an unterschiedliche Anforderungen anpassen lässt und sowohl in Simulation als auch auf Hardware ein reproduzierbares und nachvollziehbares Verhalten aufweist.
Die Arbeit leistet damit einen Beitrag zur benutzerfreundlichen Exploration von RISC-V-Prozessorarchitekturen und stellt eine durchgängige Entwicklungsumgebung von der Konfiguration bis zur FPGA-Implementierung für Lehre, Forschung und prototypische Hardwareentwicklung bereit.

