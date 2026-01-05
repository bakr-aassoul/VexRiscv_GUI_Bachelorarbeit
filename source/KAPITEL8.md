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

Die in dieser Arbeit entwickelte GUI implementiert einen kontrollierten und parametrisierbaren Ansatz zur Integration benutzerdefinierter ALU-Instruktionen. Konkret wurde ein Erweiterungsmodell realisiert, bei dem Custom Instructions als zusätzliche Funktionseinheiten in der Execute-Stufe des VexRiscv-Prozessors eingebettet werden {cite}`Pap24`.

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

Innerhalb dieses Modells lassen sich bereits zahlreiche sinnvolle ISA-Erweiterungen umsetzen, wie sie auch in aktuellen RISC-V-Spezifikationen definiert sind {cite}`RIS19`. Der funktionale Umfang umfasst dabei insbesondere:

1. **Bitmanipulationen:** Operationen wie zyklische Rotationen (ROL/ROR), Bit-Spiegelungen (Reversal) oder Zähloperationen (Population Count, Leading Zero Count), die in der Standard-RISC-V-ISA (RV32I) mehrere Instruktionen erfordern würden.
2. **Sub-Word-Parallelism (SIMD):** Die gleichzeitige Verarbeitung mehrerer gepackter Datenworte innerhalb eines 32-Bit-Registers (z. B. vier parallele 8-Bit-Additionen für Bildverarbeitungsalgorithmen).
3. **Kryptografische Primitive:** Spezifische nicht-lineare Mischfunktionen und Substitutionsschritte (S-Box-Logik), wie sie in modernen Verschlüsselungsalgorithmen (z. B. ChaCha20, AES-Lightweight) benötigt werden.
4. **Bedingte Arithmetik:** Operationen wie `Min/Max` oder saturierende Arithmetik, die in Software teure bedingte Sprünge erfordern würden, in Hardware jedoch effizient durch Multiplexer realisiert werden können.

Ausgeschlossen sind hingegen Operationen, die sequenzielle Logik (interne Zustände), Speicherzugriffe oder komplexe, mehrzyklische Berechnungspfade (wie Divisionen oder Gleitkomma-Operationen) erfordern.

Da die Ausführung der unterstützten Operationen vollständig innerhalb eines Taktzyklus erfolgt, bleibt das bestehende Pipeline-Steuerungskonzept des VexRiscv unverändert {cite}`Pap24`. Es sind weder zusätzliche Stall-Signale noch erweiterte Hazard-Behandlungen notwendig.
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

Obwohl der VexRiscv-Plugin-Mechanismus prinzipiell die Implementierung solcher Einheiten erlaubt {cite}`Pap24`, wurde dieser Ansatz im Rahmen der vorliegenden Arbeit bewusst nicht umgesetzt. Der Fokus lag auf der Entwicklung einer stabilen, automatisierten Konfigurations- und Generierungsumgebung, nicht auf der Einführung komplexer Pipeline-Kontrollmechanismen.
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

Die theoretische Diskussion der Level-2- und Level-3-Ansätze verdeutlicht, dass weitergehende Erweiterungen zwar technisch möglich sind, jedoch mit einem deutlichen Anstieg der Systemkomplexität einhergehen. Wie Hennessy und Patterson darlegen, muss dieser Mehraufwand stets kritisch gegen den zu erwartenden Geschwindigkeitszuwachs (Speedup) abgewogen werden {cite}`HP17`. Die klare Abgrenzung dieser Erweiterungsstufen trägt dazu bei, die getroffenen Designentscheidungen transparent und nachvollziehbar zu machen.

Damit bildet dieses Kapitel die Grundlage für die abschließende Zusammenfassung und den Ausblick im folgenden Kapitel.







