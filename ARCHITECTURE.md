# `pyru` Architecture: A Deep Dive into Performance Engineering

This document details the architectural decisions and the iterative optimization process that makes `pyru` the fastest Python web scraper.

## Core Philosophy

The guiding principle of `pyru` is to delegate all performance-critical work to a hyper-optimized Rust core while providing a user-friendly Python interface. Python is excellent for scripting and user interfaces, but for raw, concurrent I/O and CPU-bound parsing, Rust is unparalleled.

## Architectural Diagram

```mermaid
graph TD
    subgraph User Interface
        A[Python CLI (`click`)]
    end

    subgraph Python Runtime
        B[Asyncio Event Loop]
    end
    
    subgraph FFI Bridge
        C[`pyo3-asyncio`]
    end

    subgraph Rust Core (`rust_scraper.so`)
        D[Tokio Async Runtime] --> E{Concurrency Limiter (`Semaphore`)};
        E --> F[HTTP/1.1 Client (`reqwest`)];
        F --> G[TLS (`rustls`)];
        G --> H[Async I/O (`io_uring`)];
        D --> J[HTML Parsing (`scraper`)];
        J --> K[Memory Allocator (`mimalloc`)];
    end

    subgraph OS Kernel
        I[Linux Kernel TCP/IP Stack]
    end

    A -- Invokes --> B;
    B -- Bridges to --> C;
    C -- Spawns --> D;
    H -- Syscalls --> I;
    I --> L[Internet];

    style A fill:#336791,stroke:#fff,stroke-width:2px,color:#fff
    style B fill:#336791,stroke:#fff,stroke-width:2px,color:#fff
    style C fill:#f37321,stroke:#fff,stroke-width:2px,color:#fff
    style D fill:#b34b3e,stroke:#fff,stroke-width:2px,color:#fff
    style E fill:#b34b3e,stroke:#fff,stroke-width:2px,color:#fff
    style F fill:#b34b3e,stroke:#fff,stroke-width:2px,color:#fff
    style G fill:#b34b3e,stroke:#fff,stroke-width:2px,color:#fff
    style H fill:#b34b3e,stroke:#fff,stroke-width:2px,color:#fff
    style J fill:#b34b3e,stroke:#fff,stroke-width:2px,color:#fff
    style K fill:#b34b3e,stroke:#fff,stroke-width:2px,color:#fff
    style I fill:#444,stroke:#fff,stroke-width:2px,color:#fff
```

## The Optimization Journey: A Layer-by-Layer Breakdown

`pyru`'s performance is not the result of a single trick, but a systematic optimization of every layer of the software stack.

### 1. Application Layer: Rust Core
The most significant decision was to write the performance-critical path in Rust. The `scrape_all_urls` function orchestrates the entire process, using `tokio` to manage thousands of concurrent tasks without the overhead of system threads.

### 2. Protocol Layer: Fine-Tuned HTTP
- **HTTP/1.1 by Default:** While HTTP/2 is excellent for multiplexing streams over a single connection, our benchmark revealed that for a high volume of short-lived, independent connections, the lower setup cost of HTTP/1.1 provided a measurable performance advantage.
- **`TCP_NODELAY`:** This option is enabled to disable Nagle's algorithm, reducing latency by sending packets as soon as they are ready.

### 3. TLS Layer: `rustls`
We explicitly use `reqwest`'s `rustls-tls` feature. This replaces the default dependency on the system's OpenSSL library (`native-tls`) with a pure Rust implementation of TLS. This eliminates the overhead of C Foreign Function Interface (FFI) calls, which, while small, are significant in a tight, high-throughput loop.

### 4. Memory Management: `mimalloc`
The default system memory allocator is a general-purpose tool. We replaced it with `mimalloc`, a high-performance allocator from Microsoft designed for multi-threaded, concurrent applications. It excels at handling many small, short-lived allocations with less contention and fragmentation.

### 5. Compiler Optimizations: PGO and LTO
- **Profile-Guided Optimization (PGO):** This is the pinnacle of compiler optimization. We compile `pyru` in three stages:
    1.  An instrumented build that collects performance data.
    2.  A benchmark run that generates a detailed profile of "hot" code paths.
    3.  A final build where the compiler uses this profile to make more intelligent optimization decisions (e.g., better inlining and branch prediction).
- **Link-Time Optimization (LTO):** This allows the compiler to perform optimizations across the entire crate, not just on a per-module basis.
- **`target-cpu=native`:** This instructs the compiler to generate machine code specifically for the CPU it is being compiled on, allowing it to use the most modern and efficient instruction sets available.

### 6. I/O Subsystem: `io_uring`
On Linux, we configure `tokio` to use the `io_uring` interface. This is the most advanced I/O API available, offering a true asynchronous, zero-copy interface to the kernel that significantly reduces system call overhead compared to older APIs like `epoll`.

### 7. OS Kernel: TCP Tuning
For the final benchmark, we tuned the Linux kernel's TCP/IP stack via `sysctl`:
- `net.ipv4.tcp_tw_reuse=1`: Allows the kernel to reuse sockets in the `TIME_WAIT` state for new connections, critical for our benchmark's connection profile.
- `net.ipv4.tcp_fin_timeout=15`: Reduces the time sockets are held after closing, freeing up system resources faster.

### 8. Code Quality: Micro-Optimizations
The final step was to refine the Rust code itself to eliminate redundant work:
- **Parse Selector Once:** The CSS selector is parsed only once and shared across all concurrent tasks using an `Arc<Selector>`.
- **Avoid Allocations:** The HTML body is converted to a `String` with minimal allocations, and result vectors are pre-allocated with a known capacity.

This relentless, full-stack approach is the secret to `pyru`'s performance.