---
category: "Go"
topic: "Benchmarking"
---

# Benchmarking

- Are benchmark functions named starting with 'Benchmark'? [YES/NO]
- Do benchmark functions accept '*testing.B' as a parameter? [YES/NO]
- Is 'b.ResetTimer()' used if setup code is expensive? [YES/NO]
- Are benchmarks run with the '-bench' flag? [YES/NO]
- Is 'b.ReportAllocs()' used to track memory allocations? [YES/NO]
- Are benchmarks isolated from external side effects? [YES/NO]
