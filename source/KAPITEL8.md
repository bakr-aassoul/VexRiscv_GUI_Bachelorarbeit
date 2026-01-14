# Erweiterung und Designraum der Custom-ALU-Integration
```{raw} latex
\large
```
In den vorangegangenen Kapiteln wurde die Implementierung und Evaluierung einer GUI-gestützten Entwicklungsumgebung zur Konfiguration und Erweiterung eines modularen VexRiscv-Prozessors vorgestellt. Ein zentraler Bestandteil dieser Arbeit ist die Möglichkeit, den Prozessor um benutzerdefinierte Instruktionen in Form sogenannter Custom ALUs zu erweitern.

Dieses Kapitel ordnet die im Rahmen der Arbeit realisierte Lösung in einen erweiterten architektonischen Kontext ein und diskutiert systematisch den Designraum möglicher Custom-ALU-Integrationsstufen. Ziel ist es, aufzuzeigen, welche Erweiterungen prinzipiell denkbar sind, welche Konsequenzen diese für Mikroarchitektur, Tooling und Verifikation haben und an welcher Stelle bewusst architektonische Grenzen gezogen wurden.
Dabei wird klar zwischen der implementierten Lösung und theoretisch möglichen, jedoch nicht realisierten Erweiterungen unterschieden.

```{raw} latex
\clearpage
```

```{raw} latex
\normalsize
```
## Einordnung der implementierten Lösung

Die in dieser Arbeit entwickelte GUI implementiert einen kontrollierten und parametrisierbaren Ansatz zur Integration benutzerdefinierter ALU-Instruktionen. Konkret wurde ein Erweiterungsmodell realisiert, bei dem Custom Instructions als zusätzliche Funktionseinheiten in der Execute-Stufe des VexRiscv-Prozessors eingebettet werden {cite}`Pap24a`.

Charakteristisch für diesen Ansatz sind:
- eine feste, durch die GUI validierte Instruktionskodierung innerhalb der reservierten RISC-V-Custom-Opcode-Bereiche,
- die Nutzung der vorhandenen Operandenpfade (rs1, rs2, Immediate),
- die Rückführung des Ergebnisses über den regulären Writeback-Pfad,
- sowie eine deterministische Single-Cycle-Ausführung ohne Veränderung des globalen Pipeline-Timings.

Die Erweiterung erfolgt dabei vollständig automatisiert durch die Generierung eines parametrierten Custom-ALU-Plugins in SpinalHDL. Die GUI abstrahiert diesen Prozess und stellt sicher, dass ausschließlich architektonisch gültige und syntaktisch korrekte Erweiterungen erzeugt werden.

Dieser Ansatz stellt den Kernbeitrag der Arbeit dar und bildet die Grundlage für die nachfolgenden theoretischen Betrachtungen.

```{raw} latex
\clearpage
```
## Level-1-Erweiterungen: Parametrisierte Single-Cycle Custom ALUs

Die implementierte Lösung entspricht einem Level-1-Erweiterungsmodell, bei dem benutzerdefinierte Instruktionen als einzyklische ALU-Operationen realisiert werden. Diese Erweiterungsstufe ist besonders geeignet für GUI-gestützte Entwicklungsumgebungen, da sie einen günstigen Kompromiss zwischen Flexibilität und Hardwarekomplexität bietet.

Innerhalb dieses Modells lassen sich bereits zahlreiche sinnvolle ISA-Erweiterungen umsetzen, wie sie auch in aktuellen RISC-V-Spezifikationen definiert sind {cite}`RISCV19`. Der funktionale Umfang umfasst dabei insbesondere:

1. **Bitmanipulationen:** Operationen wie zyklische Rotationen (ROL/ROR), Bit-Spiegelungen (Reversal) oder Zähloperationen (Population Count, Leading Zero Count), die in der Standard-RISC-V-ISA (RV32I) mehrere Instruktionen erfordern würden.
2. **Sub-Word-Parallelism (SIMD):** Die gleichzeitige Verarbeitung mehrerer gepackter Datenworte innerhalb eines 32-Bit-Registers (z. B. vier parallele 8-Bit-Additionen für Bildverarbeitungsalgorithmen).
3. **Kryptografische Primitive:** Spezifische nicht-lineare Mischfunktionen und Substitutionsschritte (S-Box-Logik), wie sie in modernen Verschlüsselungsalgorithmen (z. B. ChaCha20, AES-Lightweight) benötigt werden.
4. **Bedingte Arithmetik:** Operationen wie `Min/Max` oder saturierende Arithmetik, die in Software teure bedingte Sprünge erfordern würden, in Hardware jedoch effizient durch Multiplexer realisiert werden können.

Ausgeschlossen sind hingegen Operationen, die sequenzielle Logik (interne Zustände), Speicherzugriffe oder komplexe, mehrzyklische Berechnungspfade (wie Divisionen oder Gleitkomma-Operationen) erfordern.

Da die Ausführung der unterstützten Operationen vollständig innerhalb eines Taktzyklus erfolgt, bleibt das bestehende Pipeline-Steuerungskonzept des VexRiscv unverändert {cite}`Pap24a`. Es sind weder zusätzliche Stall-Signale noch erweiterte Hazard-Behandlungen notwendig.
Der Verifikationsaufwand beschränkt sich somit auf die funktionale Korrektheit der jeweiligen Operation, was eine effiziente Validierung mittels RTL-Simulation und Wellenformanalyse erlaubt.

Diese Eigenschaften machen Level-1-Custom-ALUs besonders geeignet für den Einsatz in Lehr- und Forschungsumgebungen sowie für reproduzierbare Architektur-Explorationen, wie sie im Rahmen dieser Arbeit angestrebt wurden.

```{raw} latex
\clearpage
```


## Level-2-Erweiterungen: Mehrzyklische und gepipeline Custom Units

Eine weiterführende Erweiterungsstufe besteht in der Integration mehrzyklischer oder intern gepipeline Custom Units. Solche Einheiten würden es erlauben, komplexere Operationen abzubilden, deren Berechnung nicht innerhalb eines einzelnen Taktzyklus abgeschlossen werden kann, beispielsweise breitbandige Multiplikationen, CRC-Berechnungen oder komplexe Datenpermutationen.

Architektonisch erfordert dieser Ansatz jedoch eine tiefere Integration in die Pipeline-Steuerung des Prozessors. Insbesondere müssten Mechanismen zur:
- expliziten Steuerung des Ausführungsbeginns,
- Signalisierung von Busy- und Done-Zuständen,
- gezielten Unterbrechung oder Verzögerung der Execute-Stufe,
- sowie zur korrekten Interaktion mit Branch-Flushes und Exceptions

implementiert werden.

Darüber hinaus steigt der Verifikationsaufwand signifikant, da neben der funktionalen Korrektheit auch das zeitliche Verhalten über mehrere Taktzyklen hinweg überprüft werden muss.

Obwohl der VexRiscv-Plugin-Mechanismus prinzipiell die Implementierung solcher Einheiten erlaubt {cite}`Pap24a`, wurde dieser Ansatz im Rahmen der vorliegenden Arbeit bewusst nicht umgesetzt. Der Fokus lag auf der Entwicklung einer stabilen, automatisierten Konfigurations- und Generierungsumgebung, nicht auf der Einführung komplexer Pipeline-Kontrollmechanismen.
Level-2-Custom-Units stellen jedoch eine realistische Erweiterungsmöglichkeit für weiterführende Arbeiten dar, etwa im Kontext einer Masterarbeit oder eines vertiefenden Forschungsprojekts.

```{raw} latex
\clearpage
```
## Level-3-Erweiterungen: Vollständig generierte ALU-Datenpfade aus der GUI

Die maximale Form der Erweiterbarkeit wäre die vollständige Generierung beliebiger ALU-Datenpfade direkt aus der grafischen Benutzeroberfläche, beispielsweise durch das Emitieren frei formulierbarer SpinalHDL-Codefragmente. Ein solcher Ansatz würde es Anwendern erlauben, das Verhalten der Execute-Stufe nahezu uneingeschränkt zu definieren.

Dieser Grad an Flexibilität geht jedoch mit erheblichen Nachteilen einher. Die GUI würde ihre Rolle als Konfigurations- und Automatisierungswerkzeug verlieren und sich funktional zu einer vereinfachten Hardware-Entwurfsumgebung entwickeln, die Eigenschaften klassischer EDA-Tools aufweist.
Damit verbunden sind:
- der Verlust syntaktischer und semantischer Garantien,
- eine deutlich erhöhte Fehleranfälligkeit des Build-Prozesses,
- ein kaum begrenzbarer Verifikationsaufwand,
- sowie eine reduzierte Nachvollziehbarkeit und Reproduzierbarkeit der erzeugten Hardware.

Insbesondere im akademischen Kontext wäre eine solche Lösung nur schwer als zuverlässiges Werkzeug zu rechtfertigen. Aus diesen Gründen wurde dieser Ansatz bewusst ausgeschlossen. Die entwickelte GUI verfolgt stattdessen das Ziel, kontrollierte Erweiterbarkeit innerhalb klar definierter architektonischer Grenzen bereitzustellen.

```{raw} latex
\clearpage
```
## Abgrenzung und Bewertung des Designraums

Die vorangegangene Betrachtung zeigt, dass der Designraum der Custom-ALU-Integration ein breites Spektrum möglicher Erweiterungen umfasst. Die in dieser Arbeit umgesetzte Level-1-Lösung stellt dabei einen bewusst gewählten Punkt in diesem Designraum dar, der eine hohe praktische Relevanz bei gleichzeitig überschaubarem Implementierungs- und Verifikationsaufwand bietet.

Die theoretische Diskussion der Level-2- und Level-3-Ansätze verdeutlicht, dass weitergehende Erweiterungen zwar technisch möglich sind, jedoch mit einem deutlichen Anstieg der Systemkomplexität einhergehen. Wie Hennessy und Patterson darlegen, muss dieser Mehraufwand stets kritisch gegen den zu erwartenden Geschwindigkeitszuwachs (Speedup) abgewogen werden {cite}`HP17b`. Die klare Abgrenzung dieser Erweiterungsstufen trägt dazu bei, die getroffenen Designentscheidungen transparent und nachvollziehbar zu machen.

Damit bildet dieses Kapitel die Grundlage für die abschließende Zusammenfassung und den Ausblick im folgenden Kapitel.

# Einordnung und Diskussion der Arbeitsergebnisse

```{raw} latex
\large
```
Um den wissenschaftlichen Beitrag dieser Arbeit abschließend zu bewerten, ist ein direkter Vergleich mit existierenden Entwicklungsmethoden im RISC-V-Ökosystem sowie eine kritische Diskussion der methodischen Grenzen notwendig. Dieses Kapitel ordnet die entwickelte Lösung in den aktuellen Forschungsstand ein, grenzt sie von reinen Simulationswerkzeugen ab und beleuchtet die getroffenen Designentscheidungen hinsichtlich ihrer Limitationen.

```{raw} latex
\clearpage
```

```{raw} latex
\normalsize
```

## Einordnung in den Forschungsstand

Der Ansatz, Hardware durch Software-Generatoren zu beschreiben, ist in der RISC-V-Forschung fest etabliert. Ein prominentes Beispiel hierfür ist der **Rocket Chip Generator** der UC Berkeley {cite}`Asanovic16` . Ähnlich wie die in dieser Arbeit verwendete Kombination aus VexRiscv und SpinalHDL nutzt auch Rocket Chip eine in Scala eingebettete Sprache (Chisel), um Hardware parametrisch zu beschreiben. Ein wesentlicher Unterschied besteht jedoch in der Zielsetzung und Zugänglichkeit. Während Rocket Chip primär auf High-Performance-Kerne abzielt und für seine hohe Komplexität sowie eine steile Lernkurve bekannt ist, demokratisiert die vorliegende Arbeit den Generator-Ansatz. Durch die Abstraktion der textbasierten Komplexität mittels einer grafischen Oberfläche (GUI) wird auch Einsteigern ohne tiefgehende Code-Kenntnisse die Generierung valider Hardware ermöglicht.

Im industriellen Kontext werden vergleichbare Werkzeuge wie **Codasip Studio** eingesetzt, um anwendungsspezifische Prozessoren (ASIPs) zu entwerfen {cite}`Codasip` . Diese kommerziellen Tools verfolgen im Kern dasselbe Ziel wie die vorliegende Arbeit, nämlich die Automatisierung von Hardware-Design (RTL) und Software-Tools (Compiler) aus einer High-Level-Beschreibung. Die Abgrenzung liegt hierbei vor allem im Lizenzmodell und der Zielgruppe. Während Codasip eine kostenintensive Enterprise-Lösung darstellt, bietet die entwickelte GUI einen Open-Source-basierten Zugang. Dieser ist speziell für die Lehre und Rapid Prototyping optimiert und erfordert keinerlei proprietäre Lizenzgebühren.

## Abgrenzung zu Simulatoren

Für pädagogische Zwecke existieren Tools wie **Ripes**, die eine visuelle Simulation von RISC-V-Pipelines ermöglichen und den Datenfluss grafisch darstellen {cite}`Ripes`. Die hier vorgestellte Lösung grenzt sich davon deutlich ab, da Ripes rein auf die Software-Simulation auf PC-Ebene beschränkt ist. Im Gegensatz dazu erzeugt der entwickelte Ansatz synthetisierbare Hardware. Der generierte Prozessor läuft folglich nicht nur im Simulator, sondern wurde, wie in Kapitel 7 demonstriert, physisch auf einem FPGA (Pynq-Z1) in ein SoC integriert und unter realen Taktbedingungen validiert.

## Vergleich der Konfigurationsmethodik

Der etablierte Workflow zur Erstellung eines **VexRiscv-Prozessors** basiert traditionell auf der manuellen Modifikation von Scala-Quelltexten {cite}`Pap24`, bei der Entwickler Konfigurationsklassen im Code instanziieren und Plugins programmatisch verknüpfen müssen. Der Beitrag dieser Arbeit besteht darin, diese fehleranfällige manuelle Konfiguration durch eine validierende GUI-Schicht zu ersetzen. Insbesondere die Integration von **Custom Instructions** wurde signifikant vereinfacht. Der entwickelte **Custom ALU Generator** schreibt den notwendigen SpinalHDL-Code, wie den Decoder-Service und die Pipeline-Injection, vollautomatisch. Anwender müssen lediglich die logische Operation definieren, was die Einstiegshürde für ISA-Erweiterungen erheblich senkt.

## Methodische Limitationen

Um den Fokus der Bachelorarbeit zu wahren, wurden spezifische Einschränkungen gegenüber dem vollen Funktionsumfang des VexRiscv vorgenommen. Hinsichtlich der Komplexität der Recheneinheiten werden ausschließlich Single-Cycle-Instruktionen unterstützt (Level 1), während Multi-Cycle-Operationen oder Einheiten mit internem Zustand von der GUI nicht generiert werden. Ein weiterer Fokus lag auf Bare-Metal-Anwendungen (RV32I/M). Die komplexe Konfiguration einer Memory Management Unit (MMU) für Linux-Support ist im VexRiscv zwar möglich, wurde in der GUI jedoch nicht abgebildet. Schließlich fixiert die Generierung die Schnittstelle auf den Wishbone-Standard, um die Kompatibilität mit dem verwendeten LiteX-SoC sicherzustellen, obwohl VexRiscv nativ auch andere Bus-Protokolle wie AXI oder Avalon unterstützen würde.
