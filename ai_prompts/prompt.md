# AI Prompt Log

Student: Diya Shetty (NNM24IS081)
AI Tool Used: ChatGPT (OpenAI), chat interface
Assignment: AI-Assisted Synchronization Algorithms with Program-Generated HTML Simulation

## 1. Initial Prompt

I uploaded the Operating Systems Programming Assignment PDF and asked ChatGPT how to start the assignment. I requested a structured plan and guidance for implementing the four synchronization problems: Readers-Writers using semaphores, Readers-Writers using monitors, Dining Philosophers using semaphores, and Dining Philosophers using monitors. I also asked for help understanding the requirement for program-generated HTML simulations based on actual execution data.

## 2. Important Follow-up Prompts

- Asked for step-by-step instructions to understand the assignment requirements and organize the work.
- Asked for help understanding the four Python implementations using semaphores, locks, and condition variables.
- Asked for explanations of how the programs record execution events and generate HTML simulations using the shared helper module and HTML template.
- Asked for help understanding how to run the programs in Python and view the generated HTML files in a browser.
- Asked for help preparing the GitHub repository structure, README, AI prompt log, references, and assignment report.
- Asked for help reviewing the assignment report, including the implementation explanations, execution traces, semaphore-versus-monitor comparison, simulation screenshots, and academic-integrity declaration.

## 3. What I Changed or Did Myself

- Added my name, USN, and GitHub repository information to the assignment report.
- Organized the assignment files for the Readers-Writers and Dining Philosophers problems.
- Reviewed the implementation explanations and documentation for the four synchronization approaches.
- Prepared the report with execution traces, comparison tables, simulation screenshots, references, and an AI usage summary.

Additional verification: Record the actual program runs, HTML generation, screenshots, and code modifications completed personally before submitting this log.

## 4. Reflection: Limitations and Improvements

HTML Replay

The HTML simulations replay execution events recorded by the programs. The replay and visualization should be checked to ensure that the displayed states and event sequence accurately correspond to the recorded execution data. An improvement would be to make replay timing reflect the recorded time differences between events.

Fairness and Starvation

Python semaphores and condition variables do not guarantee strict first-in-first-out scheduling. Therefore, starvation cannot be completely ruled out in every implementation.

Readers-Writers Problem

The semaphore-based implementation follows a readers-preference approach. If readers continue arriving, a waiting writer may be delayed indefinitely. The monitor-based implementation gives preference to waiting writers, reducing the possibility of writer starvation, although readers may experience delays when writers continue arriving.

Dining Philosophers Problem

The semaphore-based solution uses an additional room semaphore initialized to three, limiting the number of philosophers competing for chopsticks at the same time and preventing circular wait in this implementation. The monitor-based solution checks and allocates both chopsticks together, avoiding the hold-and-wait condition. Starvation is still theoretically possible because strict fairness is not guaranteed.

## 5. Acknowledgement

ChatGPT was used as an AI-assisted learning and documentation tool to help understand synchronization concepts, organize the assignment, and prepare explanatory material. The final submission should be checked against the actual source code and program outputs. I am responsible for verifying the implementation, documenting the assistance used, and understanding the submitted work for the viva and live demonstration.
