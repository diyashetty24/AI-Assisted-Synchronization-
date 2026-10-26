# AI-Assisted Synchronization Algorithms

Student: Diya Shetty
USN: NNM24IS081
Course: Operating Systems
Institution: NMAM Institute of Technology, Nitte

## Overview

This project implements the Readers-Writers and Dining Philosophers synchronization problems using semaphores and monitors in Python. Each implementation generates an HTML simulation based on execution events.

## Project Structure

AI-Assisted-Synchronization-/
├── Readers_Writers/
│   ├── Monitor.py
│   ├── Semaphore.py
│   ├── Simlib.py
│   ├── Template.html
│   ├── rw_monitor.html
│   ├── rw_semaphore.html
│   └── README.md
├── dining_philosophers/
│   ├── Monitor.py
│   ├── Semaphore.py
│   ├── Simlib.py
│   ├── Template.html
│   ├── dp_monitor.html
│   └── dp_semaphore.html
├── ai_prompts/
│   └── prompt.md
├── REPORT.pdf
├── _pycache_

## Technologies

- Python and threading
- Semaphores, locks, and condition variables
- HTML, CSS, and JavaScript

How to Run

Open the relevant folder in VS Code and run:

python Semaphore.py
python Monitor.py

Run these commands separately in each program folder. Open the generated HTML files in a browser to view the simulations.

## Concepts Covered

- Race conditions and mutual exclusion
- Deadlock prevention
- Starvation and fairness
- Semaphore-based and monitor-based synchronization

## AI Assistance

ChatGPT was used to assist with understanding concepts and preparing documentation. Refer to ""ai_prompts/prompt.md"" (ai_prompts/prompt.md) for the AI prompt log.

  ## References

- "Python Threading Documentation" (https://docs.python.org/3/library/threading.html)
- "The Little Book of Semaphores" (https://greenteapress.com/wp/semaphores/)
