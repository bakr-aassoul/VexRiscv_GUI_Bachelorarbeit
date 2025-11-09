# SpinalHDL Documentation by Bakr

## Overview

This repository serves as a comprehensive, beginner-friendly guide to **SpinalHDL** a modern, type-safe HDL embedded in Scala. It introduces the language’s fundamentals and walks through examples covering simulation and code generation. You'll explore core concepts using small modules, all the way up to complex designs like the **VexRiscv** processor.
h
### Highlights
- Signal types and module creation (`Bool`, `UInt`, `Bundle`, etc.)
- Registers vs. wires (`Reg(...)` vs. direct `val`)
- Control flow constructs (`when`, `otherwise`)
- Simulation workflows with `SimConfig.withWave`
- Generating synthesizable Verilog/VHDL
- Real-world examples: comparator, counter, clock divider, PWM
- Advanced design: modular VexRiscv CPU with a plugin system

---

##  Prerequisites

- **Java JDK** (Java 11 or above)
- **Scala 2.13**
- **sbt** (Scala Build Tool)
- Optional but recommended:
  - **IntelliJ IDEA** with Scala plugin
  - **Verilator** or **GHDL** for simulation

Refer to the [Getting Started with SpinalHDL](https://spinalhdl.github.io/SpinalDoc-RTD/master/SpinalHDL/Getting%20Started) guide for help with setup. 

---

##  Documentation with Sphinx + Markdown
I used **Sphinx with Markdown** (via MyST or recommonmark) to author documentation in docs/source/, and generate both HTML and PDF outputs.
