# Interview Conceptual Q&A
 
A reference of interview questions and answers spanning Java/OOP fundamentals through senior/staff-level system design, security, observability, DevOps, and process topics. Each answer includes a plain-English translation underneath the technical points.
 
## Table of Contents
 
- [Design Patterns & Principles](#design-patterns--principles) (8)
- [Backend & System Design](#backend--system-design) (18)
- [Availability & Latency](#availability--latency) (14)
- [Node.js, Retries & Resilience](#nodejs-retries--resilience) (3)
- [Spring, Microservices & Testing](#spring-microservices--testing) (10)
- [Docker, Kubernetes & CI/CD](#docker-kubernetes--cicd) (6)
- [GraphQL vs REST](#graphql-vs-rest) (3)
- [SQL & Databases](#sql--databases) (6)
- [Algorithms](#algorithms) (7)
- [Distributed Systems](#distributed-systems) (4)
- [Rate Limiting & API Design](#rate-limiting--api-design) (4)
- [Security Fundamentals](#security-fundamentals) (6)
- [Observability](#observability) (4)
- [Frontend & Angular](#frontend--angular) (7)
- [Git & Build Tools](#git--build-tools) (5)
- [CI/CD Tools & GCP](#cicd-tools--gcp) (5)
- [Agile & Scrum](#agile--scrum) (5)
- [OOP & Language Concepts](#oop--language-concepts) (14)
- [Data Structures & Collections](#data-structures--collections) (9)
- [General CS Fundamentals](#general-cs-fundamentals) (8)
- [Concurrency & JVM Basics](#concurrency--jvm-basics) (6)
---
 
## Design Patterns & Principles
 
**Q: What is the Singleton pattern, and what's a common pitfall?**
 
- Ensures a class has exactly one instance and provides a global access point to it
- Common pitfall: a naive lazy implementation isn't thread-safe — two threads can both pass the null check and create two instances
- Fix: an enum singleton, double-checked locking with `volatile`, or the initialization-on-demand holder idiom
*In plain English: Only one of these is ever allowed to exist in the whole program, like there's only one “the president” at a time.*
 
**Q: What is the Factory pattern?**
 
- Delegates object creation to a separate method/class instead of calling `new` directly
- Lets the caller depend on an interface/abstract type rather than a concrete class
- Useful when the exact subclass to create depends on runtime input
*In plain English: Instead of building the thing yourself, you ask a helper to build it and hand it to you.*
 
**Q: What is the Builder pattern, and when would you reach for it?**
 
- Constructs a complex object step by step through chained method calls, then a final `build()`
- Avoids constructors with many optional parameters (the "telescoping constructor" problem)
- Common for immutable objects — the final object is only built once, at the end of the chain
*In plain English: You build something piece by piece with a chain of “.with this, .with that” calls instead of one giant, confusing constructor.*
 
**Q: What is the Observer pattern?**
 
- Defines a one-to-many dependency: when a subject changes state, all registered observers are notified automatically
- Basis for event-driven systems, UI listeners, pub/sub messaging
- In Java: a list of listener interfaces the subject notifies, rather than the deprecated `java.util.Observer`
*In plain English: Other parts of the code “subscribe” to get notified automatically whenever something changes — like a notification system.*
 
**Q: What is the Strategy pattern?**
 
- Defines a family of interchangeable algorithms behind a common interface, selected at runtime
- Lets you swap behavior without changing the class that uses it
- Example: passing a different `Comparator` into `sort()` to change the ordering strategy
*In plain English: You can swap out how something gets done without touching the code that uses it.*
 
**Q: What is dependency injection, and why does it matter?**
 
- A class receives its dependencies from the outside (constructor, setter, or a framework) instead of creating them itself
- Decouples classes from concrete implementations — easier to test (swap in mocks) and reconfigure
- Frameworks like Spring manage creation and injection automatically via an IoC container
*In plain English: Instead of a class building its own tools, someone hands it the tools it needs — easier to swap and test.*
 
**Q: What are the SOLID principles?**
 
- **S**ingle Responsibility — a class should have one reason to change
- **O**pen/Closed — open for extension, closed for modification
- **L**iskov Substitution — subtypes must be substitutable for their base types without breaking correctness
- **I**nterface Segregation — prefer many small, specific interfaces over one large general one
- **D**ependency Inversion — depend on abstractions, not concrete implementations
*In plain English: Five rules of thumb for writing code that's easier to change later without breaking everything else.*
 
**Q: Composition vs inheritance — which is generally preferred?**
 
- **Inheritance** ("is-a") — a subclass extends a parent, inheriting its implementation but tightly coupling the two
- **Composition** ("has-a") — a class holds a reference to another and delegates to it
- "Favor composition over inheritance" — more flexible, avoids the fragile base class problem, no single-parent lock-in
*In plain English: “Has-a” (built from parts) is usually safer and more flexible than “is-a” (extending a parent class).*
 
---
 
## Backend & System Design
 
**Q: What does idempotency mean, and why does it matter for an API?**
 
- An idempotent operation produces the same result no matter how many times it's applied
- `GET`, `PUT`, `DELETE` are expected to be idempotent by convention; `POST` typically isn't
- Matters for retries — a client safely retrying a timed-out request shouldn't double-charge a card or double-create a record
*In plain English: Doing it once or doing it five times gives the exact same result — safe to retry without messing anything up.*
 
**Q: What is the N+1 query problem?**
 
- Fetching a list of N parent records triggers one extra query per parent to fetch related child data — N+1 queries instead of 2
- Common with ORMs (Hibernate/JPA) using lazy-loaded associations accessed inside a loop
- Fixed with eager fetching / joins, or batching the child lookups into a single query
*In plain English: Instead of one trip to the database, you accidentally make one trip per item — way slower than it needs to be.*
 
**Q: What are the ACID properties of a database transaction?**
 
- **Atomicity** — all operations in a transaction succeed, or none do
- **Consistency** — a transaction moves the database from one valid state to another
- **Isolation** — concurrent transactions don't see each other's intermediate state
- **Durability** — once committed, changes survive a crash
*In plain English: The guarantees that a database change either fully happens or doesn't happen at all, even if something crashes halfway.*
 
**Q: Cache-aside vs write-through — what's the difference?**
 
- **Cache-aside** (lazy loading) — the app checks the cache first; on a miss, reads the DB and populates the cache itself
- **Write-through** — every write goes to the cache and the DB together, keeping them in sync but adding write latency
- Cache-aside suits read-heavy workloads; write-through suits data that must always stay fresh
*In plain English: Cache-aside: check the fast storage first, only bother the slow database if it's missing. Write-through: update both together, every time.*
 
**Q: Message queue vs a direct REST call — when would you use each?**
 
- **REST call** — synchronous, request/response; the caller waits, and is tightly coupled to the callee being up
- **Message queue** — asynchronous; a producer drops a message and moves on, a consumer processes it independently
- Queues decouple services, smooth traffic spikes, and enable retry/dead-letter handling without blocking the caller
*In plain English: REST: ask and wait for an answer right now. Queue: drop off a task and let someone else handle it whenever they get to it.*
 
**Q: What is Kafka, and what's it used for?**
 
- A distributed event streaming platform — essentially a durable, append-only log that scales horizontally
- Producers publish messages to topics; consumers read them independently, which decouples services
- Common uses: event-driven architectures, activity/log aggregation, stream processing, buffering high-throughput data between systems
*In plain English: A system for reliably passing streams of events between services — like a shared inbox lots of programs can read from.*
 
**Q: What is a Kafka topic, partition, and offset?**
 
- **Topic** — a named stream/category of messages, like a table
- **Partition** — a topic is split into ordered, append-only partitions so it can be written to and read in parallel
- **Offset** — a message's position within its partition; each consumer tracks the offsets it has already read
*In plain English: Topic = the name of the stream. Partition = one lane of it so multiple readers can work at once. Offset = your bookmark for how far you've read.*
 
**Q: How does Kafka differ from a traditional message queue like RabbitMQ or SQS?**
 
- Kafka retains messages for a configurable period (or indefinitely) regardless of consumption — multiple consumers can independently re-read the same data
- A traditional queue typically removes a message once it's been consumed/acknowledged — a one-time delivery model
- Kafka is built for high-throughput streaming via partitioning; traditional queues focus more on per-message routing and acknowledgment semantics
*In plain English: Kafka keeps messages around after they're read so others can replay them; a normal queue deletes a message once someone's picked it up.*
 
**Q: What is a consumer group in Kafka?**
 
- A set of consumers that share the work of reading a topic — each partition is consumed by only one member of the group at a time
- Lets you scale consumption horizontally by adding consumers, up to one per partition
- Different consumer groups are independent of each other — each group gets its own full copy of the stream
*In plain English: A team of readers splitting up the work of reading a stream, so no two teammates read the same message.*
 
**Q: What does Kafka guarantee about message ordering, and what about delivery guarantees?**
 
- Ordering is only guaranteed within a single partition, not across the whole topic — messages with the same key always route to the same partition, preserving per-key order
- **At-most-once** — a message might be lost, never duplicated (offset committed before processing)
- **At-least-once** — a message might be processed more than once, never lost (offset committed after processing; the common default)
- **Exactly-once** — each message processed exactly once, via idempotent producers/transactions — supported, but more involved to configure correctly
*In plain English: Order is only guaranteed within one lane, not the whole stream — and messages might get handled once, more than once, or (rarely) missed, depending on setup.*
 
**Q: What is a circuit breaker, and why use one?**
 
- Stops calling a failing downstream service after enough consecutive failures, "tripping" instead of piling up slow/failing requests
- After a cooldown it goes "half-open," letting a few test requests through to see if the dependency recovered
- Prevents cascading failures — one slow/down service can't exhaust the threads/connections of everything that calls it
*In plain English: If a service keeps failing, stop hammering it for a while instead of making things worse — like a fuse that trips.*
 
**Q: Horizontal vs vertical scaling — what's the trade-off?**
 
- **Vertical** — add more CPU/RAM to a single machine; simple, but hits a hard ceiling and stays a single point of failure
- **Horizontal** — add more machines/instances behind a load balancer; scales further and more resilient
- Horizontal scaling requires the app to be stateless, or to externalize state (session store, shared cache/DB)
*In plain English: Vertical: give one computer more power. Horizontal: add more computers to share the work.*
 
**Q: What is database indexing, and what's the trade-off?**
 
- A separate data structure (usually a B-tree) that lets the database find rows without scanning the whole table
- Turns a lookup from roughly O(n) into roughly O(log n)
- Trade-off: every index speeds up reads on that column but slows down writes (the index must update too) and adds storage
*In plain English: Like a book's index — it lets you jump straight to what you need instead of reading every page, but it costs a bit extra whenever the book changes.*
 
**Q: How do you design a system that handles high traffic and remains available?**
 
- Scale horizontally behind a load balancer instead of relying on one big machine, and keep the app stateless so any instance can handle any request
- Cache aggressively at multiple layers (CDN, app-level cache, DB query cache) to keep repeat reads off the database
- Add redundancy everywhere there's a single point of failure — multiple app instances, replicated databases, multi-AZ/multi-region deployment — plus health checks so a load balancer stops routing to an unhealthy instance
- Protect the system from itself under load with rate limiting, circuit breakers, and queues to smooth out spikes instead of falling over
*In plain English: Don't rely on one server — spread the work across many, cache what you can so you're not hitting the database for everything, have backups for every critical piece, and put guardrails in place so a traffic spike degrades gracefully instead of crashing everything.*
 
**Q: When do you choose a NoSQL database over a traditional SQL database?**
 
- SQL (relational) fits well-structured data with clear relationships where you need strong consistency and complex joins/transactions — e.g. financial records, order systems
- NoSQL fits when the schema is flexible or evolving, the data is naturally document/key-value/graph shaped, or you need to scale writes horizontally more easily than a relational DB typically allows
- It's not strictly either/or — many systems use both (polyglot persistence): relational for the core transactional data, a NoSQL store for something like session data, logs, or a product catalog
*In plain English: Reach for SQL when your data is structured and relationships matter and you need strong guarantees. Reach for NoSQL when your data doesn't fit neat tables, the shape keeps changing, or you need to scale out reads/writes more than a relational database comfortably allows.*
 
**Q: How do you plan for data redundancy and disaster recovery?**
 
- Replicate data across multiple nodes/availability zones (or regions, for the most critical systems) so losing one copy doesn't lose the data
- Take regular backups (and actually test restoring from them — a backup you've never restored is not a verified backup), with a retention policy that matches how far back you might need to recover
- Define RTO (recovery time objective — how long you can be down) and RPO (recovery point objective — how much data you can afford to lose) up front, since they drive how much redundancy/automation is actually worth building
- For the most critical systems, plan for and periodically test full failover to a secondary region, not just backups
*In plain English: Keep more than one copy of your data in more than one place, back it up on a schedule, actually test that the backups work, and know in advance how much downtime and data loss you can tolerate — that number decides how much redundancy you actually need to build.*
 
**Q: What trade-offs do you consider between consistency and availability?**
 
- Per the CAP theorem, during a network partition you have to pick: answer every request even if the data might be stale (availability), or refuse/delay answers until you're sure the data is current (consistency) — see the CAP theorem card for the full picture
- The right choice depends on what the data is used for — an account balance or inventory count usually needs strong consistency (showing the wrong number is worse than a slow response); a social feed, view count, or product recommendation can tolerate a stale read in exchange for staying fast and always responding
- This isn't always all-or-nothing per system — you can often choose per operation (strongly consistent for checkout, eventually consistent for "people also viewed")
*In plain English: When things go wrong, do you rather give people an answer that might be slightly out of date, or make them wait until you're sure it's correct? Money and inventory usually need "correct." A view counter or a "you might also like" list can afford to be a little behind.*
 
**Q: What factors do you consider when designing an inventory management system?**
 
- Correctness under concurrency is the core challenge — two orders can't both successfully claim the last unit of stock, so updates need proper locking/transactions or an atomic decrement, not a read-then-write race
- Decide between strong consistency (always show the true current count, at some latency/throughput cost) and a reservation/soft-hold model (briefly hold stock during checkout, release it if payment fails) depending on how strict "don't oversell" needs to be
- Model at the right granularity for the business — stock per warehouse/location, not just a single global count, if fulfillment is location-aware
- Keep a full audit trail of stock changes (received, sold, returned, adjusted) since inventory discrepancies need to be traceable back to a cause
*In plain English: The hard part is making sure two people can't both "buy" the last item at the same time. Beyond that: decide how strict you need to be about never overselling, track stock per location if that matters to the business, and keep a clear history of every change so you can explain any discrepancy later.*
 
---
 
## Availability & Latency
 
**Q: What does "five nines" (99.999%) availability actually mean?**
 
- The percentage of time a system is operational and able to serve requests
- 99.999% ("five nines") allows about 5 minutes of downtime per year; 99.9% ("three nines") allows about 8.7 hours per year
- Each additional nine gets exponentially more expensive/complex — more redundancy, faster failover, no single point of failure
*In plain English: The system is basically never down — working 99.999% of the time adds up to only about 5 minutes of downtime a whole year.*
 
**Q: What's the difference between availability and reliability?**
 
- **Availability** — the fraction of time a system is up and able to serve requests
- **Reliability** — the probability a system performs correctly over a period, without failing at all
- A system can be highly available (fast failover after crashes) but not very reliable (it crashes often), or the reverse
*In plain English: Availability is “is it up right now?” Reliability is “does it keep working without breaking at all?” — you can have one without the other.*
 
**Q: What is a single point of failure (SPOF), and how do you eliminate one?**
 
- Any single component whose failure takes down the whole system
- Eliminate with redundancy — multiple instances behind a load balancer, replicated databases, multi-AZ/multi-region deployment
- Automatic failover (promoting a replica) limits the impact when a component fails anyway
*In plain English: One part that, if it breaks, takes the whole system down with it — the goal is making sure nothing is that one weak link.*
 
**Q: What is a health check, and how does it get used?**
 
- A lightweight endpoint (e.g. `/health`) a load balancer or orchestrator polls to check if an instance can serve traffic
- An instance failing checks gets pulled out of rotation automatically, before users are affected
- **Liveness** (is the process running) vs **readiness** (is it ready to accept traffic) are different signals with different responses
*In plain English: A quick “are you okay?” ping systems send each other so a broken piece gets pulled out of rotation automatically.*
 
**Q: What's the difference between latency and throughput?**
 
- **Latency** — time for a single request to complete (e.g. milliseconds)
- **Throughput** — how many requests a system can handle per unit time (e.g. requests/sec)
- You can raise throughput (more parallel requests) while per-request latency stays flat or even climbs from queueing
*In plain English: Latency is how long one request takes. Throughput is how many requests get done overall — you can raise one without changing the other.*
 
**Q: Why track p95/p99 latency instead of the average?**
 
- An average hides outliers — a few very slow requests get masked by many fast ones
- p95/p99 shows what the slowest 5%/1% of requests actually experience — usually what drives complaints
- A system can post a great average while still failing a meaningful share of real users
*In plain English: An average can hide that some real users are having a slow, bad time — looking at the slowest 5% or 1% shows you that directly.*
 
**Q: What is tail latency, and why is it hard to fix?**
 
- The latency experienced by the slowest fraction of requests — the tail of the distribution (p99, p99.9)
- Hard to fix because it's often intermittent — GC pauses, resource contention, a slow downstream dependency, network jitter — and doesn't show up in average-case testing
- Mitigations: hedged/backup requests, sensible timeouts with retries, isolating noisy neighbors
*In plain English: The handful of unlucky, really slow requests — annoying because they're usually caused by random one-off hiccups, not one fixable bug.*
 
**Q: Where does latency typically come from in a web request, and where would you look first?**
 
- Network round-trip, DNS lookup, TLS handshake
- Server-side processing (business logic, serialization)
- Database query time — often the largest and most variable factor
- Downstream/dependency calls, each adding its own latency (and compounding on failures/timeouts)
- Start by finding the slowest link in the call chain — usually the database or an external dependency
*In plain English: It could be the network, the server doing work, or (most often) the database — check the slowest link in the chain first.*
 
**Q: How does caching reduce latency, and what's the risk?**
 
- Serves frequent requests from fast in-memory storage instead of hitting a slower backend/database
- Risk: staleness (serving outdated data), and a "thundering herd" when the cache expires and many requests hit the backend at once
- Mitigations: sensible TTLs, invalidating on writes, and request coalescing/locking on a cache miss
*In plain English: Keeping a fast copy of data close by so you don't ask the slow source every time — the risk is that copy going stale or everyone hitting the source at once when it expires.*
 
**Q: How is availability actually calculated?**
 
- `availability = uptime / (uptime + downtime) × 100%`, over a measurement period
- Often re-expressed as allowed downtime per year/month for a given "nines" target (e.g. 99.9% ≈ 43 minutes/month)
- In distributed systems, also computed as `successful requests / total requests` over a rolling window — "request-based" availability, rather than pure clock time
*In plain English: Basically: time it was working, divided by total time, turned into a percentage.*
 
**Q: How is p95/p99 latency actually calculated from raw request data?**
 
- Collect every request's latency over a time window, then sort the values ascending
- p95 is the value at the 95th percentile position — 95% of requests were faster, 5% were slower
- p99 is the same idea at the 99th percentile position
- At scale, exact sorting of every raw value doesn't hold up — monitoring systems approximate percentiles with histograms or algorithms like t-digest instead
*In plain English: Line up every request's speed from fastest to slowest, then look at the value 95% (or 99%) of the way down that list.*
 
**Q: How is error rate calculated?**
 
- `error rate = failed requests / total requests × 100%`, over a given window
- "Failed" usually means 5xx responses (server errors); some SLAs also count specific 4xx classes
- Tracked as a short rolling window (e.g. last 5 minutes), not a daily reset, so a spike is caught quickly rather than diluted by a full day of good traffic
*In plain English: Failed requests divided by total requests, as a percentage, usually looked at over just the last few minutes.*
 
**Q: How is throughput calculated, and how does it relate to latency?**
 
- `throughput = requests completed / time period` (e.g. requests per second — RPS/QPS)
- Distinct from concurrency (how many requests are in flight at once)
- Little's Law ties the three together: `concurrency ≈ throughput × average latency` — for fixed concurrency, higher latency per request means lower achievable throughput
*In plain English: How many requests finish per second — and if each one takes longer, you can't push through as many at once.*
 
**Q: What does a root cause analysis (RCA) or postmortem typically include?**
 
- A timeline — when the issue started, when it was detected, when it was mitigated, when it was fully resolved
- The actual root cause, not just the symptom — often found by repeatedly asking "why" (the "5 whys" technique) until you hit the real underlying issue
- Concrete action items to prevent recurrence, each with an owner — a postmortem with no follow-up work rarely prevents the next incident
*In plain English: What broke, when, why it really happened (not just the surface symptom), and exactly who's going to fix the underlying cause so it doesn't happen again.*
 
---
 
## Node.js, Retries & Resilience
 
**Q: What is the Node.js event loop, and why is Node single-threaded?**
 
- Node runs your JS on a single thread, but I/O work (disk, network, DB calls) is handed off to the system/libuv's thread pool under the hood — your code doesn't block waiting for it
- The event loop is what picks up finished I/O callbacks and runs them, phase by phase (timers, pending callbacks, I/O polling, `setImmediate`, close callbacks) — one at a time, in order
- Single-threaded JS execution means no shared-memory race conditions in your own code, but it also means one long synchronous, CPU-heavy operation blocks everything else — that's why CPU-bound work gets offloaded to worker threads or a separate service
*In plain English: Node handles one line of your code at a time, but it's smart about not sitting idle waiting for slow things like a database call — it kicks those off, moves on, and comes back to handle the result when it's ready. The catch: if you write code that hogs the single thread (a huge loop, heavy computation), everything else has to wait.*
 
**Q: What is exponential backoff, and why pair it with retry logic?**
 
- Retry logic re-attempts a failed call (a flaky network blip, a momentarily overloaded downstream service) instead of failing immediately
- Exponential backoff increases the wait between retries each time (e.g. 1s, 2s, 4s, 8s...) instead of retrying immediately or at a fixed interval — this gives a struggling downstream service room to recover instead of hammering it harder
- Usually paired with jitter (a small random offset added to each wait) so that many clients retrying at once don't all slam the service at the exact same moment — and with a max retry count or circuit breaker so you don't retry forever
*In plain English: If a call fails, don't just try again right away — wait a bit, and wait longer each time you fail again. That gives whatever's struggling downstream a chance to recover instead of getting hit even harder while it's already down.*
 
**Q: What is connection pooling, and why does it matter?**
 
- Opening a new database (or HTTP) connection is expensive — TCP handshake, auth, setup — so a connection pool keeps a set of already-open connections ready to reuse instead of creating one per request
- Requests borrow a connection from the pool, use it, and return it when done, instead of opening/closing one each time
- Sizing the pool matters — too small and requests queue up waiting for a free connection; too large and you can overwhelm the database with more concurrent connections than it can handle
*In plain English: Instead of opening a brand-new phone line every time you need to call the database, you keep a handful of lines already connected and just borrow one when you need it, then hand it back. Much faster than dialing fresh every single time.*
 
---
 
## Spring, Microservices & Testing
 
**Q: What's the difference between Spring and Spring Boot?**
 
- **Spring Framework** — a comprehensive framework for building Java apps (DI, AOP, MVC, etc.), but needs significant manual configuration
- **Spring Boot** — built on top of Spring, adds auto-configuration, an embedded server (Tomcat/Jetty), and starter dependencies
- Convention over configuration: sensible defaults you can override instead of wiring everything by hand
*In plain English: Spring Boot is Spring, pre-set-up for you, so you don't have to configure everything by hand just to get started.*
 
**Q: What is dependency injection in Spring, and what are the ways to do it?**
 
- Spring's IoC container creates and wires objects ("beans") together instead of you calling `new` directly
- Constructor injection (recommended — explicit, supports immutability), field injection (`@Autowired` on a field — common but harder to test), setter injection (for optional dependencies)
- Beans are found via component scanning (`@Component`, `@Service`, `@Repository`) or declared in a `@Configuration` class
*In plain English: Spring hands each class the other objects it needs instead of the class creating them itself.*
 
**Q: What's the difference between `@Component`, `@Service`, `@Repository`, and `@Controller`?**
 
- All four are stereotypes of `@Component` and get picked up by component scanning the same way
- `@Service` — a semantic label for business logic
- `@Repository` — a data-access class; Spring also translates its persistence exceptions into a consistent unchecked hierarchy
- `@Controller`/`@RestController` — handles HTTP requests
*In plain English: Different labels for “this class does X” (business logic, database access, or handling web requests) so Spring treats each one right.*
 
**Q: Monolith vs microservices — what's the actual difference?**
 
- **Monolith** — one deployable unit with all functionality, one codebase, usually one database
- **Microservices** — the app is split into independently deployable services, each owning its own data, talking over the network
- Trade-off: independent scaling/deployment vs. network complexity, distributed data consistency, and operational overhead
*In plain English: Monolith: one big program that does everything. Microservices: the same functionality split into many small programs that talk to each other.*
 
**Q: When is it actually worth moving from a monolith toward a service-oriented/microservices design?**
 
- When different parts of the system need to scale independently — e.g. an image-processing pipeline that needs far more capacity than the checkout flow shouldn't have to scale with it
- When separate teams need to own, deploy, and release different parts of the system on their own schedule, without stepping on each other's code or release cycles
- When one component's reliability or technology needs genuinely diverge from the rest (a different language/runtime, much stricter uptime requirements)
- It's not automatically the right call — for a small team or a system without those pressures, the operational overhead of services usually outweighs the benefit; "start with a monolith, split when it actually hurts" is a common and reasonable default
*In plain English: Split things into separate services when different parts genuinely need to scale, deploy, or be owned separately — not just because microservices are trendy. If nothing's actually straining against being one program, splitting it up usually just adds complexity for no real benefit.*
 
**Q: What challenges do microservices introduce that a monolith doesn't have?**
 
- A function call becomes a network call — it can fail, time out, or add latency where an in-process call couldn't
- No single database transaction can span services — needs patterns like sagas or eventual consistency instead
- Harder to trace one request across many services (distributed tracing becomes necessary), and more moving pieces to deploy/monitor/version
*In plain English: Splitting things up means pieces now talk over the network instead of directly — which can fail, lag, or get out of sync in ways one program never would.*
 
**Q: Unit test vs integration test — what's the difference?**
 
- **Unit test** — tests one method/class in isolation, dependencies mocked/stubbed; fast, no external systems
- **Integration test** — tests multiple components working together (e.g. a real or in-memory database); closer to real behavior, slower and more brittle
- The "test pyramid": many unit tests, fewer targeted integration tests
*In plain English: Unit test: check one small piece alone, with everything else faked. Integration test: check that the real pieces actually work together.*
 
**Q: Mock vs stub, in Mockito terms — what's the difference?**
 
- **Stub** — a fake object that returns canned responses, just to let the test run without hitting real dependencies
- **Mock** — a fake object that also records how it was called, so you can verify interactions afterward
- `when(...).thenReturn(...)` sets up stubbed behavior; `verify(...)` checks mock interactions
*In plain English: A stub just gives a fake answer when asked. A mock does that too, but also remembers how it was used, so you can double-check later.*
 
**Q: What makes a good code review, beyond just checking that it works?**
 
- Correctness first, but also readability (would a teammate understand this in six months) and whether it fits the codebase's existing patterns
- Check that tests actually cover the behavior change, and look for edge cases the tests might have missed
- Good feedback is specific and actionable, distinguishes "this is wrong" from "this is a preference," and doesn't block on nitpicks that don't affect correctness or maintainability
*In plain English: Don't just check that it runs — check that the next person to touch this code will actually understand it, and that the tests would catch it if it broke.*
 
**Q: How do you improve maintainability on a legacy code project?**
 
- Before changing anything risky, get a safety net in place — add characterization tests around the existing behavior so you can refactor without guessing whether you broke something
- Refactor incrementally, in small reviewable steps, rather than a risky big-bang rewrite — the "strangler fig" pattern (build the new path alongside the old, migrate traffic gradually, then remove the old code) works well for larger pieces
- Improve the parts you actually touch as you go (the "boy scout rule" — leave the code a little better than you found it) instead of trying to fix everything at once
- Address the root causes of decay going forward: tighten up code review, add tests to anything still uncovered, and document the tricky, non-obvious parts so the next person doesn't have to rediscover them
*In plain English: Don't rewrite it all at once — add tests so you know what "still works" means, then clean it up in small, safe steps, improving whatever you touch along the way instead of trying to fix everything in one risky push.*
 
---
 
## Docker, Kubernetes & CI/CD
 
**Q: Container vs virtual machine — what's the difference?**
 
- A VM virtualizes an entire machine, including its own OS kernel — heavier, slower to start, fully isolated
- A container shares the host OS kernel and only packages the app plus its dependencies — lighter, starts in seconds, less isolated
- Containers are about packaging/consistency; VMs are about full isolation
*In plain English: A VM is like a whole separate computer running inside yours. A container is a lightweight, portable box that shares your computer's engine.*
 
**Q: What problem does Docker actually solve?**
 
- Packages an app with all its dependencies (libraries, runtime, config) into one portable image
- Guarantees the same environment runs identically in dev, test, and production — no more "works on my machine"
- Images are built in layers and versioned/shared through a registry (Docker Hub or a private one)
*In plain English: It packages your app with everything it needs so it runs the exact same way on any machine — no more “works on my computer.”*
 
**Q: What does Kubernetes actually manage?**
 
- Orchestrates containers across a cluster — deciding where to run them, restarting them on crash, scaling them up/down
- Handles service discovery and load balancing across container replicas ("pods")
- Manages rollouts/rollbacks of new versions and self-heals by replacing failed pods automatically
*In plain English: It's the manager that decides where your containers run, restarts them if they crash, and scales them up or down automatically.*
 
**Q: What is a pod in Kubernetes?**
 
- The smallest deployable unit in Kubernetes — one or more tightly coupled containers sharing networking and storage
- Usually one main app container per pod, sometimes with a helper "sidecar" container
- Pods are ephemeral — Kubernetes creates/destroys them as needed, so nothing should rely on one specific pod surviving
*In plain English: The smallest unit Kubernetes runs — usually just one container (your app), sometimes with a small helper alongside it.*
 
**Q: What's a CI/CD pipeline, and what's the difference between CI and CD?**
 
- **CI** (Continuous Integration) — automatically building and testing code on every push, catching integration problems early
- **CD** (Continuous Delivery/Deployment) — automatically packaging, and for Deployment, releasing that tested code without manual steps
- A pipeline chains the stages: build → test → package → deploy, usually gated by required checks passing
*In plain English: CI: automatically test new code the moment it's pushed. CD: automatically ship that tested code out without someone doing it by hand.*
 
**Q: Blue-green vs canary deployment — what's the difference?**
 
- **Blue-green** — two full identical environments; switch all traffic from old to new at once, keep the old one ready for instant rollback
- **Canary** — roll the new version out to a small percentage of traffic first, watch metrics, then gradually increase
- Both reduce deployment risk vs. a hard cutover; canary catches problems earlier but rolls out more slowly
*In plain English: Blue-green: flip a switch and everyone instantly gets the new version, with an easy undo. Canary: let a small slice of users try it first.*
 
---
 
## GraphQL vs REST
 
**Q: What's the core difference between GraphQL and REST?**
 
- REST exposes fixed endpoints, each returning a fixed shape of data (e.g. `/users/1` returns the whole user object)
- GraphQL exposes a single endpoint where the client specifies exactly which fields it wants, in the query itself
- The server defines a schema (types and relationships); the client's query shape mirrors the response shape
*In plain English: REST: fixed menu, you get whatever the endpoint gives you. GraphQL: you ask for exactly the fields you want, and that's what comes back.*
 
**Q: What are over-fetching and under-fetching, and how does GraphQL address them?**
 
- **Over-fetching** — a REST response includes more fields than the client needs, wasting bandwidth/parsing
- **Under-fetching** — a REST response doesn't include enough, forcing extra requests to related endpoints
- GraphQL lets the client request exactly the fields it needs, across related types, in one request
*In plain English: Over-fetching: you got more data than you needed. Under-fetching: you didn't get enough and have to ask again. GraphQL lets you ask once, precisely.*
 
**Q: What are some trade-offs of GraphQL compared to REST?**
 
- Harder to cache — REST leans on HTTP caching by URL; GraphQL's single endpoint and flexible queries make that trickier
- A complex/nested query can put unpredictable load on the server — query complexity needs limiting/monitoring
- REST's uniform interface (standard verbs/status codes) is simpler to secure at the edge (rate limiting, gateways) than an arbitrary GraphQL query shape
*In plain English: It's more flexible, but harder to cache, and easier for someone to accidentally ask for something huge and slow.*
 
---
 
## SQL & Databases
 
**Q: SQL vs NoSQL — what's the actual difference?**
 
- **SQL** (PostgreSQL, SQL Server) — structured schema, tables with rows/columns, relationships enforced via foreign keys, strong ACID guarantees
- **NoSQL** (document/key-value/column/graph stores) — flexible or no fixed schema, built for horizontal scale and specific access patterns
- Choose based on the shape of your data and consistency needs — not "NoSQL is always faster"
*In plain English: SQL: data lives in neat, related tables with strict rules. NoSQL: looser structure, built to spread across many machines easily.*
 
**Q: What is a JOIN, and what are the common types?**
 
- Combines rows from two or more tables based on a related column
- **INNER JOIN** — only rows with matches in both tables
- **LEFT (OUTER) JOIN** — all rows from the left table, matched rows from the right (nulls where there's no match)
- **FULL OUTER JOIN** — all rows from both sides, matched where possible
*In plain English: Pulling matching rows from two tables together into one result, based on something they have in common.*
 
**Q: What is database normalization, and why would you denormalize?**
 
- **Normalization** — organizing tables to reduce data duplication and avoid update anomalies (splitting into related tables)
- **Denormalization** — deliberately duplicating some data to avoid expensive joins, trading storage/consistency risk for read speed
- Read-heavy systems often denormalize selectively (or lean on caching) once joins become a bottleneck
*In plain English: Normalization: don't repeat the same data in multiple places. Denormalization: repeat it on purpose anyway, to make reading faster.*
 
**Q: Primary key vs foreign key — what's the difference?**
 
- **Primary key** — uniquely identifies each row in its own table; can't be null, can't repeat
- **Foreign key** — a column in one table that references a primary key in another, enforcing referential integrity
- Foreign keys are how relational databases express relationships between tables
*In plain English: Primary key: this row's unique ID. Foreign key: a column pointing to another table's ID, linking the two together.*
 
**Q: What is a database transaction, and what does "rollback" mean?**
 
- A group of operations executed as a single unit — either all succeed (commit) or none do
- If something fails partway through, a rollback undoes every change made so far, returning the database to its prior state
- This is what gives you the "Atomicity" in ACID
*In plain English: A batch of changes that either all go through together or none of them do — if something goes wrong, everything gets undone.*
 
**Q: How would you shard a database for geographical and time-series data?**
 
- **Geographic sharding** — partition by region/location (e.g. one shard per country or data center), so data stays close to the users/services that access it most, which also helps with latency and data-residency requirements
- **Time-series sharding** — partition by time range (e.g. one shard/partition per day, week, or month), since time-series data is usually written once and queried by recent range — old partitions can be archived or dropped wholesale instead of deleted row by row
- The two can combine (shard by region, then sub-partition each region's shard by time), and most relational databases support this via native range/list partitioning rather than requiring a fully custom sharding layer
- Pick a shard key that matches your actual query patterns — sharding by something you rarely filter on just adds complexity without the performance benefit
*In plain English: Split the data by location so each region's data lives close to where it's used, and split it by time so old data can be archived in whole chunks instead of hunting down individual old rows. Combine both if you need to — but only shard along the lines you actually query by.*
 
---
 
## Algorithms
 
**Q: What is selection sort, and how does it work?**
 
- Repeatedly find the smallest remaining item and move it to the front, one pass at a time
- Each pass shrinks the "unsorted" part of the list by one, until nothing's left to scan
- O(n²) — for each of the n items, you scan through up to n remaining items to find the next smallest
*In plain English: Keep pulling out the smallest thing left in the pile and setting it down next in line, until the pile's empty.*
 
**Q: What is quicksort, and why is "divide and conquer" the key idea?**
 
- Pick a "pivot" element, then split everything else into a pile smaller than it and a pile bigger than it
- Recursively sort each pile the same way, then glue smaller-pile + pivot + bigger-pile back together
- Average case O(n log n); worst case O(n²) if you keep picking a bad pivot, like always picking the first element of an already-sorted list
*In plain English: Pick one item as a rough dividing line, shove everything smaller to one side and everything bigger to the other, then repeat that trick on each side.*
 
**Q: What is breadth-first search (BFS), and what problem is it built for?**
 
- Explores a graph level by level using a queue — visit all of a node's direct neighbors before moving on to neighbors-of-neighbors
- Finds the shortest path in an *unweighted* graph — fewest hops, not shortest distance
- Classic use: figuring out the shortest chain of connections between two people in a network
*In plain English: Check everyone one step away first, then everyone two steps away, and so on, until you find who you're looking for — that guarantees the shortest chain.*
 
**Q: What is Dijkstra's algorithm, and how is it different from BFS?**
 
- Finds the shortest path in a *weighted* graph, where edges have different costs, not just fewest hops
- Keeps a running "cheapest cost found so far" for every node, and always processes the cheapest unprocessed node next
- Doesn't work correctly if the graph has negative-weight edges — that case needs a different algorithm (Bellman-Ford)
*In plain English: Like BFS, but each connection has a price tag — you always chase the cheapest route so far instead of just the fewest steps.*
 
**Q: What is a greedy algorithm, and why doesn't it always give the perfect answer?**
 
- At every step, pick whatever looks best right now, without worrying about the overall picture
- Classic example: scheduling the most classes into one classroom by always picking whichever remaining class ends soonest
- Usually fast and "good enough," but never looks back to reconsider an earlier choice — so it can miss the true best solution
*In plain English: Just grab the best-looking option at each step and never second-guess it — fast, and often good enough, but not guaranteed to be the best possible answer.*
 
**Q: What is dynamic programming, in simple terms?**
 
- Break a big problem into smaller, overlapping subproblems, solve each one once, and reuse those answers instead of recalculating them
- Classic example: a thief filling a knapsack — work out the best value for smaller bag sizes first, building up a table, until you reach the actual bag size
- Tell-tale sign a problem wants DP: it's asking for a best/max/min answer, and smaller versions of the same question keep showing up while solving it
*In plain English: Solve the small, easy versions of the problem first, write down the answers, and build up to the big version instead of solving the same small pieces over and over.*
 
**Q: What is K-nearest neighbors (KNN)?**
 
- To classify something new, look at the "K" most similar existing examples and go with whatever category most of them belong to
- Classic example: is this fruit an orange or a grapefruit — compare it to its closest known neighbors by size and color, then vote
- Simple and intuitive, but gets slower as the dataset grows, since a new item gets compared against everything already known
*In plain English: Find the handful of most similar things you already know the answer for, and go with whatever most of them are.*
 
---
 
## Distributed Systems
 
**Q: What is the CAP theorem?**
 
- In a distributed system, you can only fully guarantee two of three things at once: **C**onsistency (every read gets the latest write), **A**vailability (every request gets a response), and **P**artition tolerance (the system keeps working even when network links between nodes fail)
- Partition tolerance isn't really optional in a real distributed system — networks fail — so in practice the real choice is between consistency and availability *during* a partition
- Traditional relational databases tend to lean CP; many NoSQL stores (Cassandra, DynamoDB) lean AP by default, though most systems let you tune this
*In plain English: When part of the network can't talk to the rest, you have to choose: give everyone an answer even if it might be slightly outdated, or refuse to answer until you're sure it's correct.*
 
**Q: What's the difference between strong consistency and eventual consistency?**
 
- **Strong consistency** — every read immediately reflects the latest write, no matter which node answers
- **Eventual consistency** — replicas converge to the same value eventually, but a read right after a write might return stale data
- Eventual consistency trades a small staleness window for higher availability and lower latency — fine for a "like" count, not for an account balance
*In plain English: Strong consistency means everyone sees the update instantly. Eventual consistency means everyone will see it eventually, but for a moment some people might still see the old version.*
 
**Q: What is sharding (database partitioning)?**
 
- Splitting a large dataset across multiple database instances ("shards"), each holding a subset of the data
- Lets you scale writes horizontally past what one machine can handle, since each shard only serves a portion of the traffic
- Introduces new problems: queries spanning multiple shards get harder, and rebalancing data when shards are added/removed takes real care
*In plain English: Instead of one giant filing cabinet, split the files across several smaller cabinets so no single one gets overloaded.*
 
**Q: What is consistent hashing, and what problem does it solve?**
 
- Maps both data and servers onto the same conceptual ring; each piece of data goes to the nearest server clockwise from its hash position
- Solves the problem plain `hash(key) % number_of_servers` has — adding or removing one server would normally remap almost everything
- With consistent hashing, adding/removing a server only reshuffles the data near that one point on the ring, not the whole dataset
*In plain English: A smarter way to assign data to servers so that adding or removing one server only shuffles a small slice of the data instead of nearly all of it.*
 
---
 
## Rate Limiting & API Design
 
**Q: What are the common rate-limiting algorithms, and how do they differ?**
 
- **Token bucket** — a bucket refills with tokens at a fixed rate; each request spends a token, requests are rejected once it's empty, but bursts up to the bucket's size are allowed
- **Leaky bucket** — requests queue up and get processed at a fixed, steady rate, smoothing out bursts rather than allowing them
- **Sliding window** — counts requests in a moving time window (e.g. the last 60 seconds), avoiding the sharp reset-boundary problem of a fixed window
*In plain English: Different ways to say "slow down" to a client — some allow short bursts, some force a perfectly steady trickle.*
 
**Q: Why would you rate-limit an API in the first place?**
 
- Protects backend resources (database, downstream services) from being overwhelmed by one client or a traffic spike
- Enforces fair usage across clients so one heavy user can't starve everyone else
- Mitigates abuse — brute-force login attempts, scraping, denial-of-service attempts
*In plain English: Stops one user (or attacker) from hogging the system or knocking it over for everyone else.*
 
**Q: How do you version an API without breaking existing clients?**
 
- Common approaches: a version in the URL (`/v1/users`), a custom header, or content negotiation via the `Accept` header — URL versioning is simplest and most common
- Add new fields as optional, and never remove or repurpose an existing field's meaning, to stay backward compatible without bumping the version
- When a real breaking change is unavoidable, run the new version alongside the old one and give clients a deprecation window before retiring it
*In plain English: Let old clients keep working exactly as before, while new clients can opt into the new behavior.*
 
**Q: What makes an API change "breaking" vs "non-breaking"?**
 
- **Non-breaking** — adding a new optional field, a new endpoint, or a new optional query parameter
- **Breaking** — removing or renaming a field, changing a field's type or meaning, making a previously optional field required, or changing what a status code means
- Rule of thumb: if an old client, unaware of the change, would misbehave or crash on the new version, it's breaking
*In plain English: If someone using the old version of your API would suddenly get errors or wrong results without changing anything on their end, you broke it.*
 
---
 
## Security Fundamentals
 
**Q: What's the difference between authentication and authorization?**
 
- **Authentication** — verifying who you are (logging in with a password, token, etc.)
- **Authorization** — verifying what you're allowed to do, once your identity is known
- Authentication always happens first, then authorization — mixing the two up is a common source of security bugs
*In plain English: Authentication checks your ID at the door. Authorization checks which rooms you're actually allowed into.*
 
**Q: What's the difference between a JWT and a traditional session, and how does OAuth fit in?**
 
- **Session** — the server stores who's logged in, and gives the client an opaque session ID cookie that points back to it
- **JWT** (JSON Web Token) — a signed token carrying the user's claims directly, so the server can verify it without a lookup; stateless, but harder to revoke early since nothing's being tracked server-side
- **OAuth** is a separate concept — a protocol for delegated authorization (letting an app access your data on another service without your password); JWTs are often the token format OAuth issues
*In plain English: A session is a claim ticket the server keeps a matching stub for. A JWT is more like a sealed, signed note that already says everything about you on its face. OAuth is the process of letting one app vouch for you to another, without sharing your actual password.*
 
**Q: What are SQL injection, XSS, and CSRF, in brief?**
 
- **SQL injection** — attacker sneaks SQL syntax into user input that gets concatenated directly into a query; prevented with parameterized queries/prepared statements
- **XSS** (cross-site scripting) — attacker gets a malicious script to run in another user's browser, usually via unescaped content; prevented by escaping/sanitizing output
- **CSRF** (cross-site request forgery) — a malicious site tricks a logged-in user's browser into making an unwanted request elsewhere; prevented with CSRF tokens or `SameSite` cookies
*In plain English: SQL injection sneaks commands into your database through a form field. XSS sneaks a script into a page another user views. CSRF tricks your browser into doing something on your behalf without you meaning to.*
 
**Q: What does HIPAA mean for how you build healthcare software?**
 
- HIPAA protects PHI (protected health information) — anything that ties health data to an identifiable person, like a name next to a prescription or diagnosis
- In practice that means: encrypt PHI at rest and in transit, log who accessed what and when (audit trails), enforce least-privilege access so people only see the data their role needs, and never put PHI in places it shouldn't be — plain-text logs, error messages, URLs, or non-prod environments
- Third parties that touch PHI (cloud vendors, analytics tools) generally need a signed Business Associate Agreement (BAA) before you can send them data
*In plain English: If it's health data tied to a real person, treat it as extra-sensitive — encrypt it, keep a record of who touched it, only let people see what they actually need for their job, and never let it leak into a log file or a test environment by accident.*
 
**Q: What is role-based access control (RBAC)?**
 
- Instead of granting permissions to individual users one by one, you define roles (e.g. `ADMIN`, `PHARMACIST`, `VIEWER`) and attach permissions to the role
- Users get assigned one or more roles, and inherit whatever permissions those roles carry — so onboarding/offboarding and audits are about managing role membership, not chasing individual permission grants
- Follows the principle of least privilege — every role should have the smallest set of permissions it needs to do its job, nothing more
*In plain English: Instead of deciding permissions person-by-person, you define a handful of "job titles" with fixed access levels, then just assign people to a job title. Way easier to manage and audit than tracking permissions per individual.*
 
**Q: How do you develop and enforce database confidentiality policies?**
 
- Start by classifying data (public, internal, confidential, restricted/PHI) so you know which fields actually need protecting, rather than treating everything the same
- Enforce least-privilege access at the database level too, not just the application — role-based grants on schemas/tables/columns, so a compromised app credential doesn't automatically expose everything
- Encrypt sensitive columns at rest and require encrypted connections in transit; mask or tokenize sensitive fields in non-production environments and logs
- Audit and log access to sensitive data, and review those policies periodically — a policy that's never reviewed tends to drift out of date as the schema and team change
*In plain English: Know which data is actually sensitive, lock it down so only the people/services that truly need it can see it, encrypt it, keep it out of logs and test environments, and keep a record of who accessed what.*
 
---
 
## Observability
 
**Q: What's the difference between logs, metrics, and traces?**
 
- **Logs** — discrete, timestamped events with detail about what happened at a specific point ("user 123 failed login at 10:02:03")
- **Metrics** — numeric measurements aggregated over time (request count, error rate, p95 latency) — good for dashboards and alerting, not individual event detail
- **Traces** — follow a single request as it moves through multiple services, showing where time was spent at each hop
*In plain English: Logs are the diary entries. Metrics are the dashboard gauges. Traces are the GPS route showing everywhere one specific request went.*
 
**Q: What problem does distributed tracing actually solve?**
 
- In a microservices system, one user request can touch many services — a trace stitches all those calls together under one shared trace ID
- Without it, debugging a slow or failed request means manually correlating logs across many separate services by timestamp — slow and error-prone
- Tools like Jaeger, Zipkin, or OpenTelemetry visualize this as a timeline showing which service/hop took the most time
*In plain English: It's a receipt that follows a request through every service it touches, so you can see exactly where it slowed down or broke.*
 
**Q: How do you approach debugging an issue across an entire system of applications?**
 
- Start by narrowing scope — use logs, metrics, and traces to figure out which service the problem actually originates in, rather than guessing
- Reproduce it in the smallest environment that still shows the behavior, then narrow further with a bisecting mindset — is it this service, this dependency, this recent deploy?
- Correlate across systems using a shared identifier (request ID/trace ID) so you can line up what each service was doing for the same request
- Once found, fix the root cause, add a regression test, and consider whether better monitoring/alerting would have caught it sooner next time
*In plain English: Use your logs, metrics, and traces to figure out which piece is actually misbehaving, narrow it down step by step instead of guessing, and once you find it, make sure you'd catch it faster next time.*
 
**Q: What kind of instrumentation do you add to support a high-performance architecture?**
 
- Latency metrics per endpoint/operation, broken down by percentile (p50/p95/p99), not just an average — averages hide the slow tail that actually hurts users
- Throughput and error-rate metrics, so you can tell a slow system from a failing one, and set alerts on both
- Resource-level metrics (CPU, memory, connection pool usage, queue depth) to catch a bottleneck before it becomes a user-facing outage
- Distributed tracing across service boundaries, so a slow request can be pinpointed to the exact hop causing it instead of guessing across the whole call chain
*In plain English: Measure how long things take (not just on average — the slow outliers matter most), how much is succeeding vs failing, how close each piece is to running out of resources, and where exactly time gets spent on a single request as it crosses services.*
 
---
 
## Frontend & Angular
 
**Q: What's the difference between TypeScript and JavaScript?**
 
- TypeScript is a superset of JavaScript that adds static typing, compiled ("transpiled") down to plain JavaScript before it runs
- Catches type-related bugs at compile time instead of at runtime — e.g. calling a method that doesn't exist on a given type
- Adoptable gradually (use `any` to opt out of checking in places) — it doesn't change how the code runs, only how it's checked beforehand
*In plain English: JavaScript with a spellchecker for types bolted on, which gets stripped away before the code actually runs.*
 
**Q: What is a component's lifecycle in Angular, and what are the key hooks?**
 
- Angular components pass through defined stages, and Angular calls a matching "hook" method at each one so you can run code at the right moment
- `ngOnInit` — runs once, after Angular sets the component's inputs; the usual place to fetch initial data
- `ngOnChanges` — runs whenever an `@Input` value changes; `ngOnDestroy` — runs right before removal, the place to clean up subscriptions/timers
*In plain English: Angular taps you on the shoulder at specific moments in a component's life — when it's born, when its inputs change, and right before it's torn down — so you can hook in your own code then.*
 
**Q: What is an Observable in RxJS, and how is it different from a Promise?**
 
- A Promise resolves once with a single value (or error); an Observable can emit multiple values over time, and can be cancelled
- Nothing happens until you `subscribe()` to an Observable — it's "lazy," unlike a Promise, which starts running the moment it's created
- RxJS operators (`map`, `filter`, `switchMap`, `debounceTime`, ...) transform and combine streams of values declaratively
*In plain English: A Promise is a single delivery that's already on its way. An Observable is more like a subscription — a stream of deliveries that only starts once you sign up for it, and that you can cancel any time.*
 
**Q: What does two-way data binding mean in Angular?**
 
- Changes in the component's data automatically update the view, and changes in the view (like typing into an input) automatically update the component's data
- Written with `[(ngModel)]` ("banana in a box") — shorthand for binding a property and listening for its change event at the same time
- Contrasts with one-way binding, where data only flows in a single direction (component → view, or view → component)
*In plain English: Update the data and the screen updates itself; type into the screen and the data updates itself — they stay in sync automatically, in both directions.*
 
**Q: What's the difference between `==` and `===` in JavaScript?**
 
- `==` converts both sides to the same type before comparing if they differ (type coercion) — can give surprising results, e.g. `'5' == 5` is `true`
- `===` compares both value and type, with no coercion — the generally recommended default
- Coercion rules for `==` are complex enough that most style guides just say "always use `===`" unless coercion is specifically wanted
*In plain English: `===` asks "are these really the same, type included?" `==` asks the looser, more surprising question "can I squint and call these the same?"*
 
**Q: What's the difference between `let`, `const`, and `var` in JavaScript?**
 
- `var` — function-scoped and "hoisted" (usable, as `undefined`, before its declaration line); mostly considered legacy now
- `let` — block-scoped, can be reassigned; `const` — block-scoped, can't be reassigned (though an object/array it points to can still be mutated)
- Modern style generally defaults to `const`, uses `let` only when reassignment is actually needed, and avoids `var` entirely
*In plain English: `const` is a label you can't move to a different box. `let` is a label you can move. `var` is the old, looser way that causes more surprises.*
 
**Q: What does a Jest test typically consist of, and what's a mock in that context?**
 
- `describe()` groups related tests; `it()`/`test()` defines one test case; `expect()` makes assertions about the result
- `jest.fn()` creates a mock function you can control the return value of and check how it was called — Jest's equivalent of what Mockito does in Java
- `jest.mock()` can replace an entire module/dependency with a fake version, isolating the unit under test from things like real API calls
*In plain English: You describe what you're testing, say what should happen, and check that it actually did — swapping in fake stand-ins for anything you don't want the test actually touching.*
 
---
 
## Git & Build Tools
 
**Q: What's the difference between merge and rebase in Git?**
 
- **Merge** — creates a new "merge commit" tying two branches' histories together, preserving exactly what happened, messy intermediate commits included
- **Rebase** — replays your branch's commits on top of the target branch one by one, producing a clean, linear history, but rewrites commit hashes
- Rule of thumb: rebase your own local, unpushed work to keep history clean; merge (never rebase) once a branch is shared with others
*In plain English: Merge keeps the messy true story of what happened. Rebase rewrites your part of the story to look like it happened in a clean, straight line — but only do that to history nobody else has seen yet.*
 
**Q: What does interactive rebase (`git rebase -i`) let you do?**
 
- Lets you edit a range of commits before they're applied — reorder them, squash several into one, reword messages, or drop a commit entirely
- Commonly used to clean up a messy feature branch — turning 15 "wip" commits into 2–3 meaningful ones before opening or merging a pull request
*In plain English: A chance to tidy up your commit history before showing it to anyone else — like editing a rough draft before you hand it in.*
 
**Q: What's the difference between `git fetch` and `git pull`?**
 
- `git fetch` — downloads the latest commits/branches from the remote but doesn't touch your working branch
- `git pull` — fetch immediately followed by a merge (or rebase, if configured) into your current branch
- `fetch` is the safer default when you want to look at what changed before integrating it
*In plain English: Fetch just checks what's new without touching your work. Pull checks what's new and immediately mixes it into your work.*
 
**Q: What is a merge conflict, and how do you resolve one?**
 
- Happens when Git can't automatically combine changes because the same lines were edited differently on both sides being merged
- Git marks the conflicting section with `<<<<<<<` / `=======` / `>>>>>>>` markers; you edit it to the correct final content, then stage and commit
- Frequent small commits/merges and communicating who's touching what reduces how often these happen
*In plain English: Git found two people's edits to the same lines and can't guess which one you want — so it hands both versions back to you to pick or blend by hand.*
 
**Q: What do Gradle and Maven actually do for a Java project?**
 
- Both are build automation tools — they compile code, manage dependencies (downloading libraries from a repository), run tests, and package the result (a JAR/WAR)
- Maven configures builds declaratively in XML (`pom.xml`) with a fairly rigid lifecycle
- Gradle uses a more flexible script (Groovy or Kotlin DSL) and is generally faster, thanks to incremental builds and caching
*In plain English: Both are the assembly line that turns your source code plus its dependencies into a runnable package — Maven is more rigid and standardized, Gradle is more flexible and usually faster.*
 
---
 
## CI/CD Tools & GCP
 
**Q: What's the difference between Jenkins and GitHub Actions?**
 
- **Jenkins** — a self-hosted, highly configurable automation server you install and maintain yourself, pipelines defined in a Jenkinsfile
- **GitHub Actions** — CI/CD built into GitHub itself, hosted by GitHub, workflows defined in YAML files living in the repo
- Jenkins offers more control and a huge plugin ecosystem; GitHub Actions is simpler to set up with less infrastructure to maintain, if your code's already on GitHub
*In plain English: Jenkins is a powerful tool you run and maintain yourself. GitHub Actions is the same idea, but built in and managed for you if your code already lives on GitHub.*
 
**Q: What is Argo CD, and how does it fit into a Kubernetes CI/CD setup?**
 
- A GitOps continuous delivery tool for Kubernetes — it watches a Git repo holding your desired cluster state and automatically syncs the real cluster to match it
- Instead of a pipeline pushing changes directly to the cluster, you commit the change to Git, and Argo CD pulls and applies it — Git becomes the single source of truth
- Makes rollbacks trivial (just revert the Git commit) and gives an audit trail of every change made to the cluster
*In plain English: Instead of manually pushing changes to your cluster, you just update a file in Git, and Argo CD notices and makes the real cluster match it automatically.*
 
**Q: What does a tool like Rancher add on top of raw Kubernetes?**
 
- A management layer/UI for operating one or more Kubernetes clusters — provisioning, user access control, monitoring, and app catalogs, all in one place
- Useful when managing multiple clusters (dev/staging/prod, or multi-cloud) without hand-running `kubectl` against each one separately
- Kubernetes itself has no built-in multi-cluster management UI — tools like Rancher fill that gap
*In plain English: A control panel that lets you see and manage several Kubernetes clusters at once, instead of typing commands into each one separately.*
 
**Q: What is a platform like Harness generally used for?**
 
- A continuous delivery platform focused on automating and de-risking deployments — progressive/canary rollouts, automated rollback on bad metrics, approval gates
- Sits later in the pipeline than CI tools like Jenkins/GitHub Actions — CI builds and tests the artifact, a CD platform like Harness decides how it safely reaches production
*In plain English: Once your code is built and tested, a tool like this handles rolling it out safely — a little at a time, watching for problems, and pulling it back automatically if something looks wrong.*
 
**Q: What are GCP Cloud Storage and BigQuery each used for?**
 
- **Cloud Storage** — object storage for files/blobs (images, backups, logs, data lake files), similar to AWS S3
- **BigQuery** — a serverless data warehouse for running fast SQL queries over huge datasets, without managing any servers or indexes yourself
- Common pattern: raw data lands in Cloud Storage, then gets loaded into BigQuery for analysis
*In plain English: Cloud Storage is a giant hard drive for files. BigQuery is a tool for asking huge piles of data questions in plain SQL, fast, without running your own database servers.*
 
---
 
## Agile & Scrum
 
**Q: What's the difference between Scrum and Kanban?**
 
- **Scrum** — fixed-length iterations (sprints, usually 1–4 weeks) with defined ceremonies and a sprint backlog that's locked for the sprint
- **Kanban** — continuous flow; work items move across a board as capacity allows, no fixed iteration length, work pulled as capacity opens up
- Scrum suits teams that benefit from a predictable planning rhythm; Kanban suits teams with more unpredictable, continuously arriving work (like support/ops)
*In plain English: Scrum plans work in fixed-length chunks with a set routine. Kanban just keeps a steady stream of work flowing across a board, picked up as people have room for it.*
 
**Q: What are the standard Scrum ceremonies, and what's each one for?**
 
- **Sprint planning** — the team commits to a set of work for the upcoming sprint
- **Daily standup** — a short daily sync on progress and blockers
- **Sprint review** — demo the completed work to stakeholders; **Sprint retrospective** — the team reflects on what to change next sprint
*In plain English: Plan what you'll do, check in daily on how it's going, show off what got finished, then talk honestly about what to do better next time.*
 
**Q: What are story points, and why not just estimate in hours?**
 
- A relative measure of effort/complexity/uncertainty for a piece of work, rather than a literal time estimate
- Different people work at different speeds, so estimating in points (often 1, 2, 3, 5, 8, 13) forces the team to agree on relative size instead of false precision in hours
- Velocity (points completed per sprint) becomes a team-level planning tool, without pretending individual task durations are perfectly predictable
*In plain English: Instead of guessing exact hours (which nobody's ever great at), the team just agrees "this is about twice as much work as that one" and plans around those relative sizes.*
 
**Q: What's the difference between the product backlog and the sprint backlog?**
 
- **Product backlog** — the full, prioritized list of everything that could be worked on, maintained by the product owner
- **Sprint backlog** — the subset the team commits to for the current sprint, plus the plan for delivering it
- The product backlog is constantly reprioritized/groomed; the sprint backlog stays stable once a sprint starts
*In plain English: The product backlog is the entire wish list. The sprint backlog is just the slice of that list the team promised to actually finish this round.*
 
**Q: How does Agile actually influence day-to-day software design decisions?**
 
- Favors incremental, evolvable design over a large upfront design phase — you design enough to build the next slice of value, then let the design adapt as requirements become clearer
- Encourages breaking work into small, independently shippable increments, which pushes toward loosely coupled, modular design almost as a side effect
- Regular retrospectives and continuous feedback mean technical debt and design issues get surfaced and addressed incrementally, rather than piling up until a rewrite feels necessary
*In plain English: Instead of designing the whole system perfectly upfront, you build it in small working pieces and let the design evolve as you learn more — which naturally pushes toward smaller, more flexible pieces instead of one big rigid plan.*
 
---
 
## OOP & Language Concepts
 
**Q: What is a class?**
 
- A blueprint/template that defines the fields (state) and methods (behavior) its objects will have
- Declared once, in one place — takes up no memory for actual data until something instantiates it
- Can be instantiated many times, each time producing a separate object
*In plain English: The recipe or template — it describes what something will have and do, but isn't a real thing yet by itself.*
 
**Q: What is an object?**
 
- A specific instance of a class, created with `new`
- Has its own copy of the class's instance fields (state), while sharing the class's method definitions
- Lives on the heap; a variable holding it is really just a reference to that memory
*In plain English: An actual thing made from that recipe — you can make as many as you want, each with its own values.*
 
**Q: What are the four pillars of OOP?**
 
- **Encapsulation** — bundling data with the methods that act on it, hiding internal state
- **Abstraction** — exposing only essential behavior, hiding implementation
- **Inheritance** — a class acquiring fields/methods from a parent
- **Polymorphism** — the same call behaving differently depending on the actual object type
*In plain English: Four big ideas behind this style of code: hide the messy details, keep data and behavior together, reuse a parent's code, and let the same action behave differently depending on what it's acting on.*
 
**Q: How do you know when to use procedural logic instead of an object-oriented approach?**
 
- Procedural (a straightforward sequence of function calls operating on data) fits simple, linear logic well — a script, a data transformation pipeline, a small utility — where there isn't much shared state or need to model real-world "things"
- OOP earns its keep when you have meaningful state plus behavior that belongs together, multiple related variations of a concept (polymorphism), or a system that will keep growing and needs clear boundaries between parts
- The two aren't mutually exclusive in practice — plenty of OOP codebases have small procedural helper methods/utility classes for logic that's genuinely just "do A, then B, then C"
*In plain English: If it's basically a straight list of steps operating on some data, procedural is simpler and fine. Reach for objects when you have state and behavior that naturally belong together, or several variations of the same idea that need to behave differently.*
 
**Q: What's the difference between encapsulation and abstraction?**
 
- Encapsulation is *how* — bundling fields as private and exposing them through methods
- Abstraction is *why* — hiding complexity so the caller only sees what a thing does, not how
- Example: an interface is abstraction; making its implementing class's fields private is encapsulation
*In plain English: Encapsulation is hiding the messy internal details. Abstraction is showing only the simple “what it does” part to whoever's using it.*
 
**Q: What's the difference between method overloading and overriding?**
 
- **Overloading** — same method name, different parameter list, resolved at compile time
- **Overriding** — a subclass redefines a parent's method with the identical signature, resolved at runtime via dynamic dispatch
- Overloading is about having multiple versions; overriding is about replacing one
*In plain English: Overloading: same name, different inputs, same class. Overriding: a child class swaps in its own version of a parent's method.*
 
**Q: What's the difference between an abstract class and an interface?**
 
- Abstract class — can hold state, constructors, and a mix of implemented/unimplemented methods; a class can extend only one
- Interface — no state (only constants), traditionally only method signatures (though `default`/`static` methods are now allowed); a class can implement many
- Reach for an abstract class when subclasses share real state/behavior; reach for an interface to describe a capability
*In plain English: Abstract class: a partly-built parent you finish filling in. Interface: just a promise of “you must be able to do these things,” with no shared code of its own (traditionally).*
 
**Q: What does the `static` keyword mean?**
 
- Belongs to the class itself, not to any one instance
- Exactly one copy, shared across every object
- Accessible without creating an instance (`ClassName.member`)
*In plain English: Belongs to the whole class, not to any one object made from it — like a shared counter everyone sees the same value of.*
 
**Q: What does `final` mean on a variable, method, and class?**
 
- **Variable** — can only be assigned once
- **Method** — subclasses can't override it
- **Class** — can't be subclassed at all (e.g. `String` is final)
*In plain English: Locked — can't be reassigned (variable), can't be overridden (method), or can't be extended (class).*
 
**Q: What's the difference between `==` and `.equals()`?**
 
- `==` compares references for objects (are these the same object in memory?) and values for primitives
- `.equals()` compares content — but only meaningfully if the class overrides it
- Default `.equals()` (inherited from `Object`) is just identity, same as `==`
*In plain English: `==` checks “is this the literal same object,” while `.equals()` checks “do these look the same,” if the class bothered to define what “the same” means.*
 
**Q: Why must you override `hashCode()` whenever you override `equals()`?**
 
- The contract requires that equal objects produce equal hash codes
- Break it and hash-based collections (`HashMap`, `HashSet`) silently misbehave
- Two "equal" objects can land in different buckets and the collection won't recognize them as duplicates
*In plain English: If two things are supposed to count as “equal,” they also need the same short fingerprint, or lookups relying on that fingerprint quietly break.*
 
**Q: What's the difference between checked and unchecked exceptions?**
 
- **Checked** — extends `Exception` (not `RuntimeException`); must be declared with `throws` or caught, enforced by the compiler
- **Unchecked** — extends `RuntimeException`; no declaration required
- Unchecked usually signals a programming bug (null dereference, bad cast) rather than a recoverable condition
*In plain English: Checked: the compiler forces you to handle it. Unchecked: it doesn't — usually because it signals a coding mistake, not something recoverable.*
 
**Q: Why is `String` immutable in Java?**
 
- Safe to share and cache — the string pool interns literals
- Thread-safe with no locking needed
- Safe as `HashMap` keys since the hash code can't change after insertion
- Any "modification" (`concat`, `replace`, ...) returns a new `String` instead of mutating the original
*In plain English: Once created, a String can never change — which makes it safe to share around without worrying someone else quietly alters it.*
 
**Q: What's the difference between `String`, `StringBuilder`, and `StringBuffer`?**
 
- `String` — immutable
- `StringBuilder` — mutable, fast, for building strings in a loop; not thread-safe
- `StringBuffer` — same idea with synchronized methods; thread-safe but slower, rarely the right default today
*In plain English: String never changes once made. StringBuilder is a fast scratchpad for building text piece by piece. StringBuffer is that scratchpad, safe to share across threads (at a speed cost).*
 
---
 
## Data Structures & Collections
 
**Q: What's the difference between an array and an `ArrayList`?**
 
- Array — fixed size set at creation, can hold primitives directly
- `ArrayList` — resizes dynamically (grows an internal array behind the scenes)
- `ArrayList` can only hold objects (primitives get autoboxed), with a bit more overhead per element
*In plain English: An array is a fixed-size box you set the size of upfront. An ArrayList is a similar box that can grow or shrink as needed.*
 
**Q: When would you use a `LinkedList` over an `ArrayList`?**
 
- Frequent insertions/removals at the ends or middle — `LinkedList` does it in O(1) once at the node
- Same operation on `ArrayList` is O(n) (shifting elements)
- Random access by index — `ArrayList` wins, O(1) versus O(n) to walk the list
*In plain English: LinkedList is better for constantly adding/removing things in the middle. ArrayList is better for quickly jumping to a specific spot.*
 
**Q: How does a `HashMap` work internally?**
 
- Keys are hashed (`hashCode()`); the hash determines which internal "bucket" (array slot) the entry goes into
- Collisions within a bucket are handled with a linked list, or a balanced tree once a bucket gets large enough (Java 8+)
- Average-case `get`/`put` is O(1); worst case degrades toward O(log n) with treeification, or O(n) without it
*In plain English: It uses a quick fingerprint of each key to decide which “drawer” to file it in, so it can find things almost instantly.*
 
**Q: What's the difference between `HashMap`, `LinkedHashMap`, and `TreeMap`?**
 
- `HashMap` — no ordering guarantee
- `LinkedHashMap` — preserves insertion order (or can be configured for access order, useful for an LRU cache)
- `TreeMap` — keeps keys sorted at all times, backed by a red-black tree — O(log n) operations instead of O(1)
*In plain English: HashMap: no particular order. LinkedHashMap: remembers the order things were added. TreeMap: always keeps things sorted.*
 
**Q: What's the difference between `List`, `Set`, and `Map`?**
 
- `List` — ordered, index-accessible, allows duplicates
- `Set` — no duplicates, no guaranteed index access
- `Map` — key/value pairs, no duplicate keys
- All three are interfaces with multiple implementations trading off ordering, sorting, and performance differently
*In plain English: List: an ordered lineup, duplicates allowed. Set: no duplicates, order not guaranteed. Map: pairs of labels and values, like a dictionary.*
 
**Q: In which situations would you specifically reach for "set" logic?**
 
- Deduplication — collapsing a collection down to its distinct values with no manual duplicate-checking
- Fast membership testing — checking "have I seen this before?" or "is this in the allowed list?" in O(1) instead of scanning a list in O(n)
- Mathematical set operations for comparing two collections — union (everything in either), intersection (`retainAll`, what's in both), and difference (`removeAll`, what's only in one) — useful for things like "which users are in both groups" or "what changed between two snapshots"
*In plain English: Reach for a Set whenever you care about "does this exist?" or "no duplicates allowed" more than order — it's the right tool for deduping, fast lookups, and comparing two groups of things (what's shared, what's different).*
 
**Q: What's the difference between `Comparable` and `Comparator`?**
 
- `Comparable` — implemented by the class itself, defines one natural ordering (`compareTo`)
- `Comparator` — a separate object defining an ordering from the outside (`compare`)
- Use `Comparator` for multiple orderings, or when you can't modify the class
*In plain English: Comparable: the object itself says how it sorts, by default. Comparator: someone else defines a custom sort order from outside, whenever needed.*
 
**Q: What is a fail-fast iterator?**
 
- An iterator (default for `ArrayList`/`HashMap`) that throws `ConcurrentModificationException`
- Triggered by structural modification during iteration, other than through the iterator's own `remove()`
- It's a safety check that catches bugs, not a concurrency guarantee
*In plain English: If you change a list mid-loop the wrong way, it throws an error right away instead of quietly corrupting things.*
 
**Q: Why can't you use a mutable object as a `HashMap` key safely?**
 
- If the key's fields change after insertion, its hash code changes too
- The map still looks in the bucket matching its *original* hash
- The entry effectively becomes unreachable by `get()` even though it's still in the map
*In plain English: If you change the thing you used as a key after storing it, the map can no longer find it — it's essentially lost, even though it's still technically in there.*
 
---
 
## General CS Fundamentals
 
**Q: What is Big-O notation?**
 
- Describes how an algorithm's time (or space) requirement grows as input size grows
- Focuses on the dominant term, ignoring constants
- Common orders: O(1) constant, O(log n) logarithmic, O(n) linear, O(n log n), O(n²) quadratic
- Describes worst-case growth rate, not exact runtime
*In plain English: A rough way to describe “how much slower does this get as the input grows” — without worrying about exact seconds.*
 
**Q: What's the time complexity of common list/array operations?**
 
- Access by index — O(1) for array/ArrayList
- Search (unsorted) — O(n)
- Search (sorted, binary search) — O(log n)
- Insert/delete at the end — O(1) amortized
- Insert/delete at front or middle — O(n) for an array-backed list (shifting), O(1) for a linked list once at the node
*In plain English: Grabbing something by position is instant; searching an unsorted list means checking everything one by one; adding to the end is quick, but squeezing into the middle means shifting stuff over.*
 
**Q: What's the difference between stack memory and heap memory?**
 
- **Stack** — method call frames, local variables, references; fast, fixed-size per thread, automatically freed when a method returns
- **Heap** — all objects (created with `new`); shared across threads, managed by the garbage collector; larger but slower to allocate from
*In plain English: The stack holds short-lived, per-function info that clears itself automatically. The heap holds your actual objects, which stick around until nothing needs them and the garbage collector cleans up.*
 
**Q: Is Java pass-by-value or pass-by-reference?**
 
- Java is always pass-by-value
- For objects, the value passed is the reference itself
- A method can mutate the object it points to, but reassigning the parameter never affects the caller's original variable
*In plain English: You're never handed the original variable — you're handed a copy of the address of where the object lives, so you can change what's inside but not swap it for something else entirely.*
 
**Q: What is recursion?**
 
- A function solves a problem by calling itself on a smaller version of the same problem
- Each call adds a frame to the call stack; the stack unwinds as calls return, combining results back up
- Needs a base case (stops the calls) and a recursive case (shrinks the problem toward that base case) to terminate
*In plain English: A function that solves a problem by calling a smaller version of itself, over and over, until it hits a simple case it can answer directly.*
 
**Q: What's the difference between recursion and iteration?**
 
- **Recursion** — a function calls itself on a smaller subproblem, relying on the call stack, until a base case stops it
- **Iteration** — uses a loop and explicit variables instead
- Recursion is often more readable for naturally recursive structures (trees, backtracking) but risks stack overflow on deep input
- Iteration is typically more memory-efficient
*In plain English: Recursion: a function calling itself repeatedly. Iteration: a plain loop. Recursion often reads more naturally for some problems but can run out of room if it goes too deep.*
 
**Q: What makes a recursive function correct?**
 
- A **base case** that stops the recursion without a further call
- A **recursive case** that makes measurable progress toward that base case on every call (e.g. a smaller `n`)
- Missing or unreachable base case ⇒ infinite recursion ⇒ stack overflow
*In plain English: It needs a stopping point, and it needs to actually get closer to that stopping point every time — or it just goes forever and crashes.*
 
**Q: Array vs linked list — what are the actual trade-offs?**
 
- **Array** — contiguous memory, O(1) random access, cache-friendly; fixed size (or costly resize), O(n) mid-list insert/delete
- **Linked list** — flexible size, O(1) insert/delete once positioned; O(n) access by index, extra memory per node, worse cache locality
*In plain English: Array: fast to jump around in, but resizing is a hassle. Linked list: easy to grow and rearrange, but slow to jump to a specific spot.*
 
---
 
## Concurrency & JVM Basics
 
**Q: What's the difference between a process and a thread?**
 
- **Process** — an independent program in execution with its own memory space
- **Thread** — a unit of execution within a process
- Threads in the same process share memory (heap, static fields) — cheap communication, but needs synchronization
*In plain English: A process is a whole separate running program. A thread is one of possibly several tasks running inside that same program, sharing its memory.*
 
**Q: What is a deadlock, and how do you prevent one?**
 
- Happens when two or more threads each hold a lock the other needs, and neither can proceed
- Example: thread A holds lock 1 and waits for lock 2, while thread B holds lock 2 and waits for lock 1
- Prevent by acquiring locks in a consistent global order, keeping locked sections small, or using timeouts on lock attempts
*In plain English: Two tasks are each waiting on something the other one is holding, so neither can ever move forward — like two people each waiting for the other to go first at a doorway, forever.*
 
**Q: What does the `synchronized` keyword do?**
 
- Ensures only one thread at a time can execute a given method or block for a given object's lock (monitor)
- Other threads trying to enter block until the lock is released
- Provides mutual exclusion, at the cost of throughput if overused
*In plain English: Puts a lock on a piece of code so only one thread can run it at a time — so two things can't step on each other's toes.*
 
**Q: What's the difference between concurrency and parallelism?**
 
- **Concurrency** — structuring a program to handle multiple tasks that make progress over overlapping time periods; may take turns on a single core
- **Parallelism** — actually executing multiple tasks at the exact same instant; requires multiple cores
*In plain English: Concurrency: juggling multiple things by switching between them. Parallelism: actually doing multiple things at the exact same moment, on separate cores.*
 
**Q: What is the JVM, and what does it actually do?**
 
- Runs compiled bytecode (`.class` files) rather than source directly — "write once, run anywhere"
- Handles memory management (allocation + garbage collection)
- Just-in-time compiles hot code paths to native machine code
- Provides security sandboxing
*In plain English: The engine that actually runs your compiled Java code, cleans up unused memory, and is why Java code runs the same way on any machine.*
 
**Q: What is garbage collection, in plain terms?**
 
- The JVM's automatic process for reclaiming heap memory used by unreachable objects
- No manual `free()` like in C
- Runs periodically and can introduce brief pauses — why GC tuning matters for latency-sensitive services
*In plain English: The automatic cleanup crew that frees up memory from objects nobody's using anymore, so you don't have to delete them yourself.*
 
---
 
