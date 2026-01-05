# Zusammenfassung und Ausblick

## Zusammenfassung
Ziel dieser Bachelorarbeit war die Konzeption, Implementierung und Evaluierung einer GUI-gestützten Entwicklungsumgebung zur Konfiguration und Erweiterung eines modularen RISC-V-Prozessors auf Basis des VexRiscv-Kerns. Im Mittelpunkt stand dabei die Automatisierung des Entwurfsprozesses von der Auswahl architektonischer Komponenten über die Generierung benutzerdefinierter Instruktionen bis hin zur Simulation und FPGA-basierten Ausführung.

Zu diesem Zweck wurde eine grafische Benutzeroberfläche entwickelt, die den VexRiscv-Prozessor nicht nur parametrierbar macht, sondern gezielt um anwendungsspezifische Recheneinheiten in Form von Custom ALUs erweitert. Die GUI abstrahiert die Komplexität der zugrunde liegenden Hardwarebeschreibungssprache SpinalHDL und ermöglicht es Anwendern, ISA-Erweiterungen auf einer höheren Abstraktionsebene zu definieren. Die daraus resultierenden Konfigurationen werden vollautomatisch in synthetisierbaren Scala- und Verilog-Code übersetzt.

Die funktionale Korrektheit der erzeugten Prozessorkonfigurationen wurde durch eine RTL-Simulation mit Verilator sowie eine detaillierte Signalverifikation mittels GTKWave nachgewiesen. Insbesondere konnte gezeigt werden, dass die generierten Custom Instructions korrekt dekodiert, ausgeführt und in den regulären Writeback-Pfad integriert werden.
Darüber hinaus wurde der durch die GUI erzeugte Basis-Prozessorkern erfolgreich in ein LiteX-System-on-Chip integriert und auf einem Pynq-Z1-FPGA implementiert. Der fehlerfreie Boot-Vorgang des Systems, konsistente Speicherzugriffe sowie ein erfolgreiches Timing Closure bei der Ziel-Taktfrequenz belegen die Systemreife des generierten Hardwaredesigns.

Zusammenfassend zeigt diese Arbeit, dass sich der VexRiscv-Prozessor mithilfe einer GUI-gestützten Entwicklungsumgebung effizient konfigurieren und reproduzierbar erweitern lässt. Die Kombination aus modularer Prozessorarchitektur, automatisierter Codegenerierung und strukturierter Verifikation stellt einen durchgängigen Workflow dar, der insbesondere für Lehr-, Forschungs- und Prototyping-Zwecke geeignet ist.

## Ausblick

Die im Rahmen dieser Arbeit entwickelte Entwicklungsumgebung bildet eine solide Grundlage für weiterführende Erweiterungen und Untersuchungen. Ein naheliegender Ansatz besteht in der Erweiterung des Custom-ALU-Konzepts um mehrzyklische oder intern gepipeline Recheneinheiten, wie sie in Kapitel 8 theoretisch diskutiert wurden. Solche Erweiterungen würden es erlauben, komplexere Operationen mit höherem Ressourcenbedarf abzubilden und die Grenzen der Pipeline-Steuerung systematisch zu untersuchen.

Ein weiterer Entwicklungsschritt könnte in der Vertiefung der Evaluierung liegen, beispielsweise durch eine quantitative Analyse von Flächenbedarf, Taktfrequenz und Energieverbrauch unterschiedlicher Prozessorkonfigurationen. Insbesondere der Vergleich zwischen Standard-ALU-Operationen und benutzerdefinierten Instruktionen könnte Aufschluss über den praktischen Nutzen domänenspezifischer Hardware-Erweiterungen liefern.

Auch auf Seiten der Benutzeroberfläche bestehen Erweiterungspotenziale. Denkbar wäre etwa die Integration höherer Abstraktionsebenen für Custom Instructions, beispielsweise durch vordefinierte Funktionsblöcke oder domänenspezifische Beschreibungsformen, die weiterhin innerhalb klar definierter architektonischer Grenzen operieren.
Darüber hinaus könnte die Entwicklungsumgebung um didaktische Funktionen erweitert werden, etwa zur Visualisierung von Pipeline-Abläufen oder zur automatischen Generierung von Testprogrammen.

Abschließend bietet die entwickelte GUI einen flexiblen und robusten Einstiegspunkt für die Exploration modularer RISC-V-Architekturen. Sie zeigt, dass durch gezielte Automatisierung und klare architektonische Abgrenzungen leistungsfähige Hardware-Entwurfswerkzeuge entstehen können, die sowohl technische Tiefe als auch Benutzerfreundlichkeit vereinen. Damit leistet diese Arbeit einen Beitrag zur praktischen Vermittlung und Weiterentwicklung konfigurierbarer Prozessorarchitekturen.
