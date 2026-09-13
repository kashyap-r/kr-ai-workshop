## Multi-threading vs Multiprocessing vs Aynchronous Programming (asyncio)

**Multithreading:** multiple threads inside one process.
**Multiprocessing:** multiple independent Python processes.
**Asyncio:** usually one thread + one event loop, switching between 
tasks whenever one is waiting.

Example: 
Suppose you own a restaurant and need to prepare 5 customer orders.

Normal Sequential Execution of tasks... 
Order 1 ──────────► done
                    Order 2 ──────────► done
                                        Order 3 ──────────► done

If each order takes 5 seconds, Total time taken = 15 seconds
So, for 5 orders, total time taken is 25 seconds.

### Multithreading

Imagine one kitchen with several chefs, but they share the same 
workspace, refrigerator, utensils, and ingrdients. 

            Python Process
       ┌──────────────────────┐
       │ Thread 1 ── Task A   │
       │ Thread 2 ── Task B   │
       │ Thread 3 ── Task C   │
       └──────────────────────┘
             Shared Memory

Threads belong to the same process, so they share memory. 

with threading, the same 3 orders will take a total of 5 seconds 
asssuming each order takes exactly 5 seconds each. 

This works well because while one thread waits for network I/O, Python can run another.

Where multithreading is good
It is especially useful for I/O-bound work, such as:
    API calls
    Database queries
    Downloading files
    Reading/writing files
    Web scraping
    Socket communication

There is, however, an important Python-specific concept here: the GIL — Global Interpreter Lock.

In regular CPython, historically, only one thread could execute Python bytecode at a time under the GIL. That means threads were generally not the best way to speed up pure Python CPU-heavy workloads.

Conceptually:
Thread 1  ████          ████
Thread 2      ████          ████
Thread 3          ████
          ↑
     CPU execution alternates
Threads can still be extremely useful because waiting on I/O releases opportunities for other threads to run.

### Multiprocessing

Multiprocessing is fundamentally different.
Instead of, 
        One process
        ├── Thread 1
        ├── Thread 2
        └── Thread 3

I create:
Process 1      Process 2      Process 3
Python         Python         Python
Task A         Task B         Task C
  │              │              │
CPU Core 1     CPU Core 2     CPU Core 3

Each process has its own python interpreter and memory space. 
Now imagine, a machine with four CPU Cores:
CPU Core 1 ── Process 1 ── Calculation 1
CPU Core 2 ── Process 2 ── Calculation 2
CPU Core 3 ── Process 3 ── Calculation 3
CPU Core 4 ── Process 4 ── Calculation 4

These calculations can genuinely run in parallel.
That makes multiprocessing appropriate for CPU-bound work. 

Examples: 
    Image processing
    Video encoding
    Large mathematical calculations
    Data transformations
    Scientific computing
    ML preprocessing
    Simulation

Note: Processes are heavier than threads. 

So, comparison, 
Thread
   ↓
shares process memory
cheap to create
easy communication

Process
   ↓
separate memory
more expensive to create
requires IPC / serialization


### Asyncio

There may be 1 proces, 1 thread, 1 CPU core and yet the program can 
efficiently manage thousands of concurrent tasks. 

The secret is event loop:
                EVENT LOOP
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
      Task A      Task B      Task C
        │           │           │
      waiting     waiting     running
       HTTP          DB

Instead of creating threads, tasks voluntarily give control back to 
the event loop when they are waiting.

The keyword is: "await" 

If you compare the examples, notice that this looks similar to the multithreading example.

But internally it is very different.

Threading

The operating system is switching between threads.
OS Scheduler

Thread A
    ↓
Thread B
    ↓
Thread C

Asyncio

Your Python event loop decides which coroutine should run.
Python Event Loop

Task A
  │
  └── await network
           ↓
         Task B
           │
           └── await database
                    ↓
                  Task C

This is called cooperative concurrency. 

| Property             | Multithreading                      | Multiprocessing   | Asyncio             |
| -------------------- | ----------------------------------- | ----------------- | ------------------- |
| Execution units      | Threads                             | Processes         | Coroutines/tasks    |
| Memory               | Shared                              | Separate          | Shared              |
| CPU cores            | Usually limited for Python CPU work | Multiple cores    | Usually one         |
| True CPU parallelism | Usually not the main benefit        | **Yes**           | No                  |
| Best for             | I/O                                 | CPU               | Lots of I/O         |
| Creation cost        | Medium                              | High              | Very low            |
| Communication        | Easy                                | More expensive    | Easy                |
| Race conditions      | Possible                            | Less shared state | Fewer, but possible |
| Typical scale        | Tens/hundreds threads               | Few processes     | Thousands of tasks  |
| Python mechanism     | `threading`                         | `multiprocessing` | `asyncio`           |

### Where all the three can appear in one application 

A production python service may use all the three.. 

                  FastAPI Server
                       │
                   asyncio
                       │
           ┌───────────┼────────────┐
           ▼           ▼            ▼
        OpenAI      Vector DB    Database
        request      request      request

                       │
                       ▼
              CPU-heavy PDF parsing
                       │
                 Process Pool
                 ┌─────┼─────┐
                 ▼     ▼     ▼
                CPU1  CPU2  CPU3

Note: The thumb rule to follow ... 

                   What kind of task?
                          │
               ┌──────────┴──────────┐
               │                     │
            CPU-bound             I/O-bound
               │                     │
               ▼                     ▼
       Multiprocessing       How many I/O tasks?
                                     │
                         ┌───────────┴───────────┐
                         │                       │
                     Moderate                 Massive
                         │                       │
                         ▼                       ▼
                  Multithreading             Asyncio

CPU-heavy → Multiprocessing
I/O-heavy → Threads or Asyncio
Huge numbers of concurrent I/O operations → Asyncio

One subtle distinction: concurrency vs parallelism
Concurrency means:
A
   B
A
   B
A
Several tasks are making progress during the same period 

Parallelism means:
CPU 1: AAAAAAAAAAAAA
CPU 2: BBBBBBBBBBBBB
CPU 3: CCCCCCCCCCCCC
Several tasks are literally executing simultaneously.

So, roughly, 
Asyncio        → concurrency
Threads        → concurrency, often useful for I/O
Multiprocessing → parallelism

Sequential Execution looks like this ...
TIME →

File 1  ████████
File 2          ████████
File 3                  ████████
File 4                          ████████
File 5                                  ████████

        0    2    4    6    8    10 sec

Each operation waits for the previous one 
5 × 2 seconds = 10 seconds

Threading
Threads overlap the waiting periods.
TIME →

Thread 1 / File 1  ████████
Thread 2 / File 2  ████████
Thread 3 / File 3  ████████
Thread 4 / File 4  ████████
Thread 5 / File 5  ████████

                   0       2 sec

Asyncio
Asyncio produces similar timing but uses a completely different mechanism.
                  EVENT LOOP
                      │
      ┌───────────────┼──────────────┐
      ↓               ↓              ↓
    Task 1          Task 2          Task 3
      │               │              │
    await           await          await
      │               │              │
      └───────────────┼──────────────┘
                      ↓
                  Event Loop