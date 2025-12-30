Diese Bachelorarbeit beschäftigt sich mit der Konfiguration, Simulation und FPGA-basierten Evaluierung eines modularen RISC-V-Prozessors auf Basis des in SpinalHDL entwickelten VexRiscv-Kerns. 

Ziel der Arbeit ist die Entwicklung einer grafischen Benutzeroberfläche (GUI), die über die reine Selektion vorhandener Komponenten hinausgeht: Sie ermöglicht es, den Prozessor durch einen integrierten Code-Generator um anwendungsspezifische Befehlssatzerweiterungen (Custom Instructions) zu ergänzen. 
Die GUI abstrahiert dabei die Komplexität der zugrunde liegenden Hardwarebeschreibungssprache und transformiert benutzerdefinierte Logik vollautomatisch in synthetisierbaren SpinalHDL-Code. 
Anwender werden so schrittweise durch den gesamten Entwicklungsprozess geführt, von der Definition eigener Recheneinheiten über die Generierung des Prozessordesigns bis zur Simulation.

Zur funktionalen Überprüfung der erzeugten Konfigurationen und Erweiterungen wird eine RTL-Simulation mit Verilator durchgeführt. Die Signalverläufe, einschließlich der internen Abläufe der generierten Custom ALUs, werden anschließend mit GTKWave analysiert und verifiziert.
Aufbauend darauf erfolgt die Integration des Prozessors in ein LiteX-System-on-Chip sowie die Implementierung auf einem Pynq-Z1-FPGA, wodurch eine Evaluierung der Leistungsfähigkeit unter realen Hardwarebedingungen möglich wird.

Die Ergebnisse zeigen, dass sich der VexRiscv durch die entwickelte GUI und den integrierten Code-Generator nicht nur effizient konfigurieren, sondern gezielt um anwendungsspezifische Instruktionen erweitern lässt. Das System weist dabei sowohl in der Simulation als auch auf der Hardware ein reproduzierbares Verhalten auf.

Die Arbeit leistet damit einen Beitrag zur benutzerfreundlichen Exploration von RISC-V-Architekturen und stellt eine durchgängige Entwicklungsumgebung für das Design spezialisierter Hardwarebeschleuniger in Lehre und Forschung bereit.
