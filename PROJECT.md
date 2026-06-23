# Final cloud computing project, a.y. 2025-26

## 1. Context

Modern cloud applications increasingly rely on large-scale distributed data processing pipelines exposed through service-oriented architectures. 
In many real-world scenarios, backend analytics systems based on Hadoop and Spark are integrated with REST services that allow users or external
applications to submit jobs, monitor execution status, and retrieve computed results.

## 2. Goal of the project

The project must be developed by the same groups of three students that were used to carry out laboratories in class.
Each group must design and implement a cloud-oriented distributed analytics system including the following elements:
- Hadoop MapReduce;
- Apache Spark;
- REST-based service interaction;
- containerized deployment.

## 3. Dataset selection

Students must autonomously identify and collect a dataset of at least:
- 1–1.5 GB in size.

Example dataset categories include:
- textual datasets;
- system logs;
- web datasets;
- graph/network datasets;
- IoT datasets;
- multimedia metadata;
- mobility traces;
- open government datasets.

The dataset choice must be properly motivated in the final project report.

## 4. Use case and analytics workflow

Each group must autonomously define:
- the application scenario;
- the analytics objective;
- the distributed processing workflow.

Examples of possible analytics workflows include:
- multi-stage filtering and aggregation;
- ranking systems;
- recommendation pipelines;
- graph analytics;
- similarity analysis;
- trend detection;
- anomaly detection;
- distributed statistics extraction.

The application domain and analytics workflow are intentionally left open, 
allowing each group of students to design its own distributed data-processing use case.
The proposed workflow must be sufficiently non-trivial and appropriate for distributed execution.

## 5. Hadoop implementation

The Hadoop implementation must consist of at least two non-iterative MapReduce jobs in cascade, written in Java.
To reach the maximum grade, students are encouraged to consider and properly motivate:
- combiners or in-mapper combining;
- custom partitioning strategies;
- setup() and cleanup() methods;
- custom writables;
- more than one reducer;
- performance comparison against a Python-based, non-parallel execution.

## 6. Spark implementation

Students must implement an equivalent solution using Apache Spark, which:
- must be developed in Python;
- must reproduce the same analytics workflow implemented in Hadoop;
- must allow a meaningful comparison with the Hadoop solution and, optionally, with the Python non-parallel solution.

## 7. REST-based architecture

The project must expose the distributed analytics functionalities through a REST-oriented architecture. 
In particular, students must develop:
- a REST client interface (e.g., terminal-based, web-based, graphical). The interface must allow users to:
  - start Hadoop/Spark jobs;
  - select execution parameters;
  - retrieve results and execution statistics.
- a containerized (Docker) REST server. This server acts as an intermediate layer between the client interface and the distributed backend.

## 8. Experimental evaluation

Students must perform an experimental evaluation, which should compare Hadoop and Spark considering aspects such as:
- execution time;
- memory usage;
- CPU utilization;
- impact of configuration parameters (e.g., number of input splits, number of reducers);
- test with multiple dataset sizes.

## 9. Project tracking and final report

Students must create a private GitHub or GitLab repository, where they have to periodically commit project changes.
The private repository must be shared only with the professors, using usernames carlo.vallati and carlo.puliafito (GitLab) or warner83 and cpuliafito (GitHub).
Students must also submit a brief technical report (recommended length: 4-5 pages) including:
- application scenario;
- dataset description;
- architecture description;
- MapReduce workflow pseudocode;
- REST architecture description;
- experimental evaluation;
- discussion of results.

