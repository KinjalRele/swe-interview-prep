# Java vs Python Cheat Sheet
 
Quick reference for core Java syntax and fundamentals, with Python equivalents side by side — plus the data structures, I/O patterns, and algorithm templates needed for easy LeetCode/HackerRank problems.
 
## Contents
 
- [Syntax Quick Reference](#syntax-quick-reference)
- [Commonly Used Functions](#commonly-used-functions)
1. [Program Structure](#1-program-structure)
2. [Primitive Types & Variables](#2-primitive-types--variables)
3. [Operators & Control Flow](#3-operators--control-flow)
4. [Arrays & Strings](#4-arrays--strings)
5. [OOP Fundamentals](#5-oop-fundamentals)
6. [Collections](#6-collections)
7. [Exception Handling](#7-exception-handling)
8. [Generics](#8-generics)
9. [Lambdas & Streams](#9-lambdas--streams)
10. [Equality & the Object Contract](#10-equality--the-object-contract)
11. [Static Members, Constructors & Enums](#11-static-members-constructors--enums)
12. [Concurrency Basics](#12-concurrency-basics)
13. [File I/O, Casting & Null Handling](#13-file-io-casting--null-handling)
14. [Modules, Imports & Inheritance Rules](#14-modules-imports--inheritance-rules)
15. [Stacks, Queues & Frequency Counting](#15-stacks-queues--frequency-counting)
16. [Reading Input (stdin)](#16-reading-input-stdin)
17. [Recursion & Math Utilities](#17-recursion--math-utilities)
18. [Algorithm Templates](#18-algorithm-templates)
19. [Quick Snippets](#19-quick-snippets)
20. [Interview Gotchas](#20-interview-gotchas)
---
 
## Syntax Quick Reference
 
The one table to scan when a declaration slips your mind mid-problem — every other section shows the full context, this one is just the shape of the line itself.
 
| Declare a... | Java | Python |
|---|---|---|
| variable | `int x = 5;` | `x = 5` |
| constant | `final int X = 5;` | `X = 5` (convention only) |
| string | `String s = "hi";` | `s = "hi"` |
| array / list | `int[] arr = {1, 2, 3};` | `arr = [1, 2, 3]` |
| 2D array / list | `int[][] g = new int[3][3];` | `g = [[0]*3 for _ in range(3)]` |
| typed list | `List<String> names = new ArrayList<>();` | `names = []` (no type needed) |
| map / dict | `Map<String,Integer> m = new HashMap<>();` | `m = {}` |
| set | `Set<Integer> s = new HashSet<>();` | `s = set()` |
| class | `public class Foo { }` | `class Foo:` |
| field / instance variable | `private int x;` (declared in class body) | `self.x = x` (created inside `__init__`, no pre-declaration) |
| constructor | `public Foo(int x) { this.x = x; }` | `def __init__(self, x): self.x = x` |
| object (instance) | `Foo obj = new Foo(x);` | `obj = Foo(x)` (no `new` keyword) |
| subclass | `class Dog extends Animal { }` | `class Dog(Animal):` |
| method / function | `public int add(int a, int b) { return a+b; }` | `def add(a, b): return a + b` |
| static method | `static int add(int a, int b) { ... }` | `@staticmethod`<br>`def add(a, b): ...` |
| interface | `interface Foo { void bar(); }` | `class Foo(Protocol): def bar(self): ...` |
| abstract class | `abstract class Foo { abstract void bar(); }` | `class Foo(ABC):`<br>`&nbsp;&nbsp;&nbsp;&nbsp;@abstractmethod`<br>`&nbsp;&nbsp;&nbsp;&nbsp;def bar(self): ...` |
| generic class | `class Box<T> { }` | `class Box(Generic[T]):` |
| enum | `enum Day { MON, TUE }` | `class Day(Enum): MON = 1` |
| exception class | `class FooError extends RuntimeException { }` | `class FooError(Exception):` |
| lambda | `(a, b) -> a + b` | `lambda a, b: a + b` |
 
---
 
## Commonly Used Functions
 
The everyday toolbox — math, strings, arrays/lists, and maps/sets — gathered in one scan instead of spread across sections.
 
**I/O & type**
 
| Task | Java | Python |
|---|---|---|
| print | `System.out.println(x);` | `print(x)` |
| to string | `String.valueOf(x)` | `str(x)` |
| parse number | `Integer.parseInt(s)` / `Double.parseDouble(s)` | `int(s)` / `float(s)` |
| type check | `x instanceof String` | `isinstance(x, str)` |
 
**Math**
 
| Task | Java | Python |
|---|---|---|
| min / max | `Math.min(a,b)` / `Math.max(a,b)` | `min(a,b)` / `max(a,b)` |
| absolute value | `Math.abs(x)` | `abs(x)` |
| power | `Math.pow(b, e)` | `b ** e` / `pow(b, e)` |
| square root | `Math.sqrt(x)` | `math.sqrt(x)` |
| round | `Math.round(x)` | `round(x)` |
| random int | `new Random().nextInt(n)` | `random.randint(0, n-1)` |
 
**String**
 
| Task | Java | Python |
|---|---|---|
| length | `s.length()` | `len(s)` |
| upper / lower | `s.toUpperCase()` / `s.toLowerCase()` | `s.upper()` / `s.lower()` |
| contains | `s.contains(sub)` | `sub in s` |
| index of | `s.indexOf(sub)` | `s.find(sub)` |
| replace | `s.replace(a, b)` | `s.replace(a, b)` |
| starts / ends with | `s.startsWith(p)` / `s.endsWith(p)` | `s.startswith(p)` / `s.endswith(p)` |
| char at index | `s.charAt(i)` | `s[i]` |
 
**Array / List**
 
| Task | Java | Python |
|---|---|---|
| length | `arr.length` / `list.size()` | `len(list_)` |
| sort | `Arrays.sort(arr)` / `Collections.sort(list)` | `list_.sort()` / `sorted(list_)` |
| reverse | `Collections.reverse(list)` | `list_.reverse()` / `list_[::-1]` |
| contains | `list.contains(x)` | `x in list_` |
| add / remove | `list.add(x)` / `list.remove(x)` | `list_.append(x)` / `list_.remove(x)` |
| max / min / sum | `Collections.max(list)` / `.min(list)` | `max(list_)` / `min(list_)` / `sum(list_)` |
| copy | `new ArrayList<>(list)` | `list_.copy()` / `list_[:]` |
 
**Map / Set**
 
| Task | Java | Python |
|---|---|---|
| contains key | `map.containsKey(k)` | `k in dict_` |
| get with default | `map.getOrDefault(k, def)` | `dict_.get(k, def)` |
| keys / values / entries | `map.keySet()` / `.values()` / `.entrySet()` | `dict_.keys()` / `.values()` / `.items()` |
 
---
 
## 1. Program Structure
 
Java compiles to bytecode ahead of time; Python is interpreted line by line — no build step, no wrapping class required.
 
**Java**
```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, world");
    }
}
```
 
**Python**
```python
print("Hello, world")
```
 
| | Java | Python |
|---|---|---|
| Run | `javac` then `java` (compile, then run on the JVM) | `python3 hello.py` — runs directly, no compile step |
| Blocks | `{ }` braces | indentation |
 
---
 
## 2. Primitive Types & Variables
 
Java is statically typed with 8 fixed-size primitives. Python is dynamically typed — one `int` (arbitrary precision) and one `float` cover most of what Java splits into several types, and variables need no declared type.
 
| Java type | Size | Default | Python equivalent |
|---|---|---|---|
| `byte / short / int / long` | 8–64 bit | 0 | `int` — single type, no overflow, arbitrary precision |
| `float / double` | 32/64 bit | 0.0 | `float` — always double precision |
| `char` | 16-bit | `'\u0000'` | no char type — a length-1 `str` |
| `boolean` | 1 bit | false | `bool` — literals are `True` / `False` |
 
**Java**
```java
int age = 30;
double price = 9.99;
final int MAX = 100;
Integer boxed = age;  // autobox
```
 
**Python**
```python
age = 30
price = 9.99
MAX = 100  # convention only — not enforced
# everything is already an object, no boxing step
```
 
---
 
## 3. Operators & Control Flow
 
### Switch / match
 
**Java (14+)**
```java
String day = switch (n) {
    case 1, 7 -> "Weekend";
    case 2, 3, 4, 5, 6 -> "Weekday";
    default -> "Unknown";
};
```
 
**Python (3.10+)**
```python
match n:
    case 1 | 7:
        day = "Weekend"
    case 2 | 3 | 4 | 5 | 6:
        day = "Weekday"
    case _:
        day = "Unknown"
```
 
### Loops
 
**Java**
```java
for (int i = 0; i < n; i++) { }
for (String s : list) { }
while (cond) { }
do { } while (cond);
```
 
**Python**
```python
for i in range(n):
    pass
for s in lst:
    pass
while cond:
    pass
# no do-while — use while True: ... ; if not cond: break
```
 
### Operators worth remembering
 
- Java `&&` / `||` vs Python `and` / `or` — both short-circuit, Python just spells them out.
- Java `==` on objects is identity; Python `==` calls `.equals()`/`__eq__` by default for built-ins — use Python's `is` for identity (Python's `is` ≈ Java's `==` on references).
- No `++`/`--` in Python — use `i += 1`.
- Integer division direction differs: Java's `7 / -2` truncates toward zero (`-3`); Python's `7 // -2` floors toward negative infinity (`-4`).
---
 
## 4. Arrays & Strings
 
### Arrays / lists
 
**Java**
```java
int[] a = new int[5];
int[] b = {1, 2, 3};
int[][] grid = new int[3][3];
a.length
Arrays.sort(a);
```
 
**Python**
```python
a = [0] * 5
b = [1, 2, 3]
grid = [[0] * 3 for _ in range(3)]
len(a)
a.sort()   # in place; sorted(a) returns a copy
```
 
Python lists resize freely (no fixed length like a Java array); for a fixed-size, all-one-type buffer, Python has `array.array`, rarely used outside numeric code.
 
### String building
 
**Java**
```java
// String is immutable — each + allocates
StringBuilder sb = new StringBuilder();
sb.append("a").append(1);
sb.toString();
```
 
**Python**
```python
# str is immutable too — build a list, then join
parts = ["a", str(1)]
"".join(parts)
# or, most idiomatic: an f-string
f"{a}{1}"
```
 
### Common string methods
 
| Task | Java | Python |
|---|---|---|
| content equality | `a.equals(b)` | `a == b` |
| substring | `s.substring(start, end)` | `s[start:end]` (slice, end exclusive) |
| split | `s.split(regex)` | `s.split(sep)` / `re.split()` |
| trim whitespace | `s.trim() / s.strip()` | `s.strip()` |
| format | `String.format("%d-%s", n, s)` | `f"{n}-{s}"` |
| join | `String.join(", ", list)` | `", ".join(list_)` |
 
---
 
## 5. OOP Fundamentals
 
### Class definition, this / super
 
**Java**
```java
class Dog extends Animal {
    Dog(String name) {
        super(name);
        this.breed = "Lab";
    }
}
```
 
**Python**
```python
class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)
        self.breed = "Lab"
```
 
### Access control
 
Java enforces `public` / `protected` / `private` at compile time:
 
| | class | pkg | subclass | world |
|---|---|---|---|---|
| `public` | ✓ | ✓ | ✓ | ✓ |
| `protected` | ✓ | ✓ | ✓ | – |
| (default) | ✓ | ✓ | – | – |
| `private` | ✓ | – | – | – |
 
Python has no enforced access modifiers — it's convention only:
 
- `name` — public by convention, same as Java's default/public.
- `_name` — single underscore: "internal use", still fully accessible.
- `__name` — double underscore: name-mangled to `_ClassName__name`, the closest thing to Java's `private`, still reachable if you know the mangled name.
### Abstract class vs interface
 
**Java**
```java
abstract class Shape {
    abstract double area();
}
interface Drawable {
    void draw();
}
```
 
**Python**
```python
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self): ...
# no separate interface keyword — Python allows
# multiple inheritance directly, or use typing.Protocol
# for structural (duck-typed) interfaces
```
 
### Overloading vs overriding
 
- **Overriding** works the same way in both — redefine the method in the subclass. Java wants `@Override`; Python needs nothing (optionally `@typing.override`, 3.12+).
- **Overloading** (same name, different params) is resolved at compile time in Java. Python has no true overloading — the last `def` with that name wins. Emulate it with default args, `*args`/`**kwargs`, or `functools.singledispatch`.
---
 
## 6. Collections
 
| Java interface | Java impl. | Python equivalent |
|---|---|---|
| `List` | `ArrayList` | `list` |
| `List` | `LinkedList` | `collections.deque` |
| `Set` | `HashSet` | `set` |
| `Set` | `LinkedHashSet` | no direct equivalent — `dict.fromkeys(items)` as an ordered set |
| `Set` | `TreeSet` | no builtin — `sorted(a_set)`, or `sortedcontainers.SortedSet` |
| `Map` | `HashMap` | `dict` |
| `Map` | `LinkedHashMap` | `dict` — insertion order is guaranteed by the language since 3.7 |
| `Map` | `TreeMap` | no builtin — `sorted(d.items())`, or `sortedcontainers.SortedDict` |
 
### Custom ordering
 
**Java**
```java
class Person implements Comparable<Person> {
    public int compareTo(Person o) {
        return age - o.age;
    }
}
list.sort(Comparator.comparing(Person::getName)
                  .thenComparing(Person::getAge));
```
 
**Python**
```python
class Person:
    def __lt__(self, other):
        return self.age < other.age
 
people.sort(key=lambda p: (p.name, p.age))
```
 
---
 
## 7. Exception Handling
 
Java splits exceptions into **checked** (must be declared/caught) and **unchecked**. Python has no such split — every exception is effectively "unchecked."
 
**Java**
```java
try (BufferedReader r = new BufferedReader(...)) {
    // try-with-resources auto-closes r
} catch (IOException e) {
    throw new RuntimeException("failed", e);
} finally {
    // always runs
}
```
 
**Python**
```python
try:
    with open("f.txt") as r:  # auto-closes r
        ...
except OSError as e:
    raise RuntimeError("failed") from e
finally:
    pass  # always runs
```
 
### Common exceptions
 
| Java | Python |
|---|---|
| `NullPointerException` | `AttributeError` / `TypeError` (on `None`) |
| `ArrayIndexOutOfBoundsException` | `IndexError` |
| `ClassCastException` | `TypeError` |
| `IOException` | `OSError` |
| `IllegalArgumentException` | `ValueError` |
 
### Custom exception
 
**Java**
```java
class InsufficientFundsException extends RuntimeException {
    InsufficientFundsException(String msg) {
        super(msg);
    }
}
```
 
**Python**
```python
class InsufficientFundsError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
```
 
---
 
## 8. Generics
 
Java enforces generic types at compile time. Python's type hints look similar but are just hints — nothing stops you at runtime unless a separate tool (mypy, pyright) checks them.
 
**Java**
```java
class Box<T> {
    private T value;
    void set(T v) { value = v; }
    T get() { return value; }
}
static <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) > 0 ? a : b;
}
```
 
**Python**
```python
from typing import TypeVar, Generic
T = TypeVar("T")
class Box(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value
    def get(self) -> T:
        return self.value
```
 
Java's **PECS** wildcards (`? extends` / `? super`) map to `TypeVar(..., covariant=True/contravariant=True)` in Python — rarely written by hand outside library code.
 
---
 
## 9. Lambdas & Streams
 
Java's Stream API and functional interfaces have no dedicated equivalent in Python — plain functions, lambdas, and comprehensions cover the same ground.
 
**Java (8+)**
```java
List<String> names = people.stream()
    .filter(p -> p.getAge() > 18)
    .map(Person::getName)
    .sorted()
    .collect(Collectors.toList());
```
 
**Python**
```python
names = sorted(
    p.name for p in people if p.age > 18
)
# a comprehension is the idiomatic stand-in
# for filter + map + collect
```
 
A Java lambda can hold multiple statements in `{ }`; a Python `lambda` is a single expression only — anything more becomes a regular `def`. Method references (`Person::getName`) have no special syntax in Python — a bound method (`person.get_name`) or the class method itself (`str.upper`) is already a plain callable.
 
`Optional<T>` ≈ returning `None` and checking: `if value is not None: ...` or `value or default`. A generator expression `(x for x in ...)` is lazy like a stream; a list comprehension `[x for x in ...]` is eager, like calling `.collect()` right away.
 
---
 
## 10. Equality & the Object Contract
 
- Java's `==` on objects is identity; Python's `is` is the direct match for that. Python's `==` calls `__eq__`, which — like Java's default `Object.equals` — falls back to identity unless the class overrides it.
- Java's rule "override `equals()` ⇒ override `hashCode()`" has a Python parallel: defining `__eq__` without `__hash__` makes instances **unhashable** (Python sets `__hash__` to `None` for you) — you must define both.
- Java's `record` (16+) ≈ Python's `@dataclass` (3.7+) — both generate the constructor, `__repr__`/`toString`, and `equals`/`__eq__` from the declared fields.
**Java**
```java
record Point(int x, int y) {}
```
 
**Python**
```python
from dataclasses import dataclass
@dataclass(frozen=True)
class Point:
    x: int
    y: int
# frozen=True also adds a working __hash__
```
 
---
 
## 11. Static Members, Constructors & Enums
 
### Static fields & methods
 
**Java**
```java
class Counter {
    static int count = 0;
    Counter() { count++; }
    static int getCount() { return count; }
}
```
 
**Python**
```python
class Counter:
    count = 0
    def __init__(self):
        Counter.count += 1
 
    @classmethod
    def get_count(cls):
        return cls.count
 
    @staticmethod
    def utility():
        pass  # no self/cls — closest match to Java's static
```
 
Java's `static` maps to Python's `@staticmethod`. `@classmethod` has no direct Java equivalent — it's Python's idiom for factory methods that need to know the (possibly subclassed) type.
 
### Constructor overloading
 
**Java**
```java
class Point {
    int x, y;
    Point() { this(0, 0); }
    Point(int x, int y) {
        this.x = x; this.y = y;
    }
}
```
 
**Python**
```python
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
 
    @classmethod
    def origin(cls):  # alt-constructor pattern
        return cls(0, 0)
```
 
### Enums
 
**Java**
```java
enum Day { MONDAY, TUESDAY, WEDNESDAY }
Day d = Day.MONDAY;
```
 
**Python**
```python
from enum import Enum
class Day(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
d = Day.MONDAY
```
 
Both let enum members carry fields and methods of their own — a Java enum can define a constructor and per-constant bodies; a Python `Enum` subclass can define ordinary methods that every member shares.
 
---
 
## 12. Concurrency Basics
 
**Java**
```java
Runnable task = () -> System.out.println("running");
Thread t = new Thread(task);
t.start();
t.join();
 
// higher level — a managed pool
ExecutorService pool = Executors.newFixedThreadPool(4);
pool.submit(task);
pool.shutdown();
```
 
**Python**
```python
import threading
def task():
    print("running")
t = threading.Thread(target=task)
t.start()
t.join()
 
# higher level — a managed pool
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=4) as pool:
    pool.submit(task)
```
 
Java threads run truly in parallel across cores. CPython's GIL means `threading` only helps with I/O-bound waiting, not CPU-bound work — use `multiprocessing` for real parallelism, or `asyncio` for high-volume I/O-bound concurrency on a single thread:
 
```python
import asyncio
async def task():
    await asyncio.sleep(1)
    print("done")
asyncio.run(task())
# no Java equivalent until virtual threads (Project Loom, JDK 21+)
# made cheap, massively concurrent blocking-style threads a language feature
```
 
---
 
## 13. File I/O, Casting & Null Handling
 
### Reading a file
 
**Java**
```java
try (BufferedReader br =
        new BufferedReader(new FileReader("data.txt"))) {
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
}
```
 
**Python**
```python
with open("data.txt") as f:
    for line in f:
        print(line.strip())
```
 
### Parsing & casting
 
**Java**
```java
int n = Integer.parseInt("42");
double d = (double) someInt;   // widening
Object o = "hi";
String s = (String) o;      // narrowing — can throw ClassCastException
```
 
**Python**
```python
n = int("42")
d = float(some_int)
# objects keep their real type — there's no "cast" to perform;
# isinstance(o, str) checks type instead of converting one
```
 
### null vs None
 
- Java's `null` and Python's `None` both mean "no object here" — calling a method on either blows up: `NullPointerException` in Java, `AttributeError` in Python.
- Compare against Python's `None` with `is None` / `is not None`, not `==` — by convention, and because `==` could be overridden by a class in a way that misbehaves with `None`.
- `Optional<T>` makes "might be absent" explicit in a Java signature; Python leans on `None` plus a type hint like `Optional[str]` (from `typing`) that isn't enforced at runtime.
---
 
## 14. Modules, Imports & Inheritance Rules
 
### Packages & imports
 
**Java**
```java
package com.example.utils;
 
import java.util.List;
import java.util.ArrayList;
```
 
**Python**
```python
# file: utils/helpers.py — the file IS the module
import os
from collections import defaultdict
from .helpers import my_function  # relative, within a package
```
 
### Single vs multiple inheritance
 
**Java**
```java
// one parent class, many interfaces
class Dog extends Animal
        implements Comparable<Dog>, Runnable { }
```
 
**Python**
```python
# multiple full classes, directly
class Dog(Animal, Comparable, Runnable):
    pass
# conflicts resolve via MRO (C3 linearization) — inspect it with Dog.__mro__
```
 
Because Java allows only one parent class, `super.method()` unambiguously means "the one parent." Python's `super()` instead walks the class's MRO — with multiple inheritance it may call a method on a sibling class, not literally the first listed parent, which is a common source of surprise.
 
---
 
## 15. Stacks, Queues & Frequency Counting
 
The single highest-value pattern for easy problems: a stack for matching/undo problems, a queue for BFS, a map for O(1) lookups and counts.
 
### Stack
 
**Java**
```java
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1);
stack.push(2);
int top = stack.pop();   // 2
int peek = stack.peek();
```
 
**Python**
```python
stack = []
stack.append(1)
stack.append(2)
top = stack.pop()      # 2
peek = stack[-1]
```
 
### Queue
 
**Java**
```java
Deque<Integer> queue = new ArrayDeque<>();
queue.offer(1);
queue.offer(2);
int front = queue.poll();  // 1
```
 
**Python**
```python
from collections import deque
queue = deque()
queue.append(1)
queue.append(2)
front = queue.popleft()   # 1
```
 
Removing from the front of a plain Java `ArrayList` or a Python `list` is O(n) — that's why both languages reach for a deque (`ArrayDeque` / `collections.deque`) for queue behavior instead.
 
### Frequency counting
 
**Java**
```java
Map<Character, Integer> freq = new HashMap<>();
for (char c : s.toCharArray()) {
    freq.merge(c, 1, Integer::sum);
    // same as: freq.put(c, freq.getOrDefault(c, 0) + 1);
}
```
 
**Python**
```python
from collections import Counter
freq = Counter(s)
# or manually:
freq = {}
for c in s:
    freq[c] = freq.get(c, 0) + 1
```
 
---
 
## 16. Reading Input (stdin)
 
HackerRank-style problems parse raw stdin — the naive reader in each language is fine for small input, but slow enough to time out on large input.
 
**Java — simple**
```java
Scanner sc = new Scanner(System.in);
int n = sc.nextInt();
String line = sc.nextLine();
```
 
**Python — simple**
```python
n = int(input())
line = input()
parts = input().split()
```
 
**Java — fast, for large input**
```java
BufferedReader br =
    new BufferedReader(new InputStreamReader(System.in));
int n = Integer.parseInt(br.readLine());
String[] parts = br.readLine().split(" ");
```
 
**Python — fast, for large input**
```python
import sys
data = sys.stdin.read().split()
# then index/consume from the `data` list —
# far fewer function calls than one input() per line
```
 
A slow reader is a common, invisible cause of TLE (time limit exceeded) on HackerRank — `Scanner` and repeated `input()` calls are both noticeably slower than the buffered alternatives once input runs into the thousands of lines.
 
---
 
## 17. Recursion & Math Utilities
 
### Recursion
 
**Java**
```java
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```
 
**Python**
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```
 
Python's default recursion limit is ~1000 frames (`sys.setrecursionlimit()` to raise it) — deep unbounded recursion raises `RecursionError` there sooner than it would throw `StackOverflowError` in Java. An iterative rewrite (often with an explicit stack) sidesteps it in either language.
 
### Math utilities
 
**Java**
```java
Math.max(a, b); Math.min(a, b);
Math.abs(x); Math.pow(base, exp);
Math.floor(x); Math.ceil(x);
// no built-in gcd on Math — BigInteger has one:
BigInteger.valueOf(a).gcd(BigInteger.valueOf(b));
```
 
**Python**
```python
max(a, b); min(a, b)
abs(x); pow(base, exp)
import math
math.floor(x); math.ceil(x)
math.gcd(a, b)          # built in, unlike Java's Math
divmod(a, b)         # (quotient, remainder) in one call
```
 
---
 
## 18. Algorithm Templates
 
Skeletons for the three techniques that resolve a large share of easy (and plenty of medium) problems.
 
### Two-pointer
 
**Java**
```java
int left = 0, right = arr.length - 1;
while (left < right) {
    int sum = arr[left] + arr[right];
    if (sum == target) return new int[]{left, right};
    else if (sum < target) left++;
    else right--;
}
```
 
**Python**
```python
left, right = 0, len(arr) - 1
while left < right:
    total = arr[left] + arr[right]
    if total == target:
        return [left, right]
    elif total < target:
        left += 1
    else:
        right -= 1
```
 
### Sliding window
 
**Java**
```java
int left = 0, maxLen = 0;
Set<Character> seen = new HashSet<>();
for (int right = 0; right < s.length(); right++) {
    while (seen.contains(s.charAt(right))) {
        seen.remove(s.charAt(left));
        left++;
    }
    seen.add(s.charAt(right));
    maxLen = Math.max(maxLen, right - left + 1);
}
```
 
**Python**
```python
left = max_len = 0
seen = set()
for right, ch in enumerate(s):
    while ch in seen:
        seen.remove(s[left])
        left += 1
    seen.add(ch)
    max_len = max(max_len, right - left + 1)
```
 
### Binary search
 
**Java**
```java
int lo = 0, hi = arr.length - 1;
while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;
    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) lo = mid + 1;
    else hi = mid - 1;
}
return -1;
// built-in alternative:
Arrays.binarySearch(arr, target);
```
 
**Python**
```python
lo, hi = 0, len(arr) - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        lo = mid + 1
    else:
        hi = mid - 1
return -1
# built-in alternative:
import bisect
bisect.bisect_left(arr, target)
```
 
---
 
## 19. Quick Snippets
 
### Declaring a class
 
**Java**
```java
public class Car {
    private String model;
    private int year;
 
    public Car(String model, int year) {
        this.model = model;
        this.year = year;
    }
 
    public String getModel() { return model; }
}
// usage
Car car = new Car("Civic", 2022);
```
 
**Python**
```python
class Car:
    def __init__(self, model, year):
        self.model = model
        self.year = year
 
# usage — fields are public by default,
# no getter boilerplate needed
car = Car("Civic", 2022)
print(car.model)
```
 
### Reversing a string
 
**Java**
```java
// no built-in reverse on String itself
String reversed = new StringBuilder(s).reverse().toString();
 
// manual, two-pointer swap (common interview ask)
char[] c = s.toCharArray();
for (int i = 0; i < c.length / 2; i++) {
    char tmp = c[i];
    c[i] = c[c.length - 1 - i];
    c[c.length - 1 - i] = tmp;
}
```
 
**Python**
```python
# slice with a step of -1
reversed_s = s[::-1]
 
# or, without slicing
reversed_s = "".join(reversed(s))
```
 
### Loop patterns
 
**Java**
```java
// index + value
for (int i = 0; i < arr.length; i++) {
    System.out.println(i + ": " + arr[i]);
}
// break / continue
for (int i = 0; i < n; i++) {
    if (i == 3) continue;
    if (i == 7) break;
}
```
 
**Python**
```python
# index + value — no manual counter needed
for i, val in enumerate(arr):
    print(f"{i}: {val}")
# break / continue
for i in range(n):
    if i == 3:
        continue
    if i == 7:
        break
```
 
Java's `break`/`continue` can carry a label to jump out of an outer loop (`outer: for (...) { ... break outer; }`) — Python has no labeled break; the usual workarounds are a flag variable, wrapping the loops in a function and using `return`, or raising and catching a sentinel exception.
 
---
 
## 20. Interview Gotchas
 
- **Integer caching** — Java caches boxed `Integer` values from -128 to 127, so `==` on two boxed 100s is `true` but breaks at 200. CPython does the same for small ints (-5 to 256) as an implementation detail — `is` on two such ints looks equal by accident. Use `.equals()` / `==`, never identity, to compare values in either language.
- **String / literal interning** — `"a"=="a"` is `true` in both languages (pooled literals), but `new String("a")=="a"` is `false` in Java, and building a Python string dynamically can likewise fail an `is` check even when `==` succeeds.
- **Pass-by-value, always** — neither language has true pass-by-reference. A reference itself is passed by value, so a function can mutate the object it points to but never reassign the caller's variable to a different object.
- **Integer overflow** — Java's `int` silently wraps: `Integer.MAX_VALUE + 1` becomes `Integer.MIN_VALUE`. Python `int` has arbitrary precision — it never overflows.
- **finally always runs** — true in both languages, even after a `return`/`try` completes; a `return` placed inside `finally` silently swallows one from the `try` block, in Java and Python alike.
- **Fallthrough** — Java's classic colon-style `switch` falls through without `break`; the arrow form doesn't. Python's `match` never falls through at all — each `case` is independent.
- **Python: mutable default arguments** — `def f(x, cache=[]):` creates the list **once**, at function definition time, and every call without an explicit argument shares it. Default to `None` and create the mutable value inside the function body instead.
- **Python: late-binding closures** — a lambda created inside a loop captures the **variable**, not its value at that iteration: `[lambda: i for i in range(3)]` all return `2`. Fix by defaulting the argument: `lambda i=i: i`.
- **Python: the GIL** — CPython's Global Interpreter Lock lets only one thread execute Python bytecode at a time, so `threading` doesn't parallelize CPU-bound work the way Java threads do; use `multiprocessing` or native extensions for that.
 
