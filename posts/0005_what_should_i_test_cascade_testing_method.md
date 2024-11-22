---
title: What should I test? - The Cascade Testing Method
date: 2024-11-22
tags:
  - testing
  - development
  - methodology
  - TDD
  - programming
---

For a long time, convincing people to create automated tests during development wasn't easy. Whether the argument was
longer development time or lack of usefulness, there was always pushback. Nowadays, this has changed for the
better—whatever methodology you choose for development, tests are an integral part of it in the vast majority of cases.
The problem, at least as I see it now, isn't if we should write tests, but what we should write tests for in a realistic
and pragmatic way.

Of course, we could be purists and try to test not just every line of code, but every logical outcome of each line.
The first problem with this approach is that I don't think any tool actually enables you to do that. 
We have test coverage tools, but at least the ones I know only cover code execution, not logical outcomes. 
More importantly, this approach is unattainable, too burdensome, and would likely lead to test breakage with each and
every code change.

When discussing testing approaches, TDD (Test-Driven Development) is the first thing that comes to mind: write the 
acceptance test, then integration tests, then unit tests, iterating and refactoring at each step. And to be honest, 
on paper it sounds amazing. In practice, I've never managed to fully accomplish this. 
It could be a "skill issue" on my part, but to me, the TDD approach usually fails the pragmatism smell test, 
especially in the day-to-day reality of incoming tasks and deadlines. 
Even discounting that, at some point I really feel overwhelmed by it—it's just too much effort for very little gain in 
my experience.

## Enter the Cascade Testing Method

Lately, I've developed something I'm calling the "Cascade Testing Method." It works like this: develop your code (either together with tests or tests after—that doesn't matter), but always start by testing the "happy path." Test that your main functionality works as envisioned.

Here's a very simple example: imagine a CLI tool that takes two numbers and outputs their sum. Write an integration test that calls the entrypoint function with 2, 2 and expects 4.

After establishing the happy path, create tests for obvious—and I mean very obvious—corner cases. In the same example, write a test that passes "2, R" as parameters and verify that the program behaves nicely, fails gracefully, or tells the user that the input isn't supported (whatever the expected behavior should be).

Finally, when bugs arrive (and they will) after the code starts being used, then apply a TDD-like approach to solve each bug.

## Why This Works Better

First of all, it works better for me, not for everyone, so YMMV(Your Mileage May Vary). But I think it's a good approach for a few reasons:

This approach addresses what I find to be the most tedious part of TDD: writing tests before the code exists. With Cascade Testing, the interfaces and behaviors are already in place, and you know your "happy path" is working. When a bug appears, you write a test to replicate it—which isn't always easy, but often replicating the bug is more than half the work of solving it. Then you modify the code with the new test in place until it passes. Of course, this simple example can branch out significantly during bug investigation.

I've been using this method for some time now, and I'm pleased with the results. It really removes a lot of the cognitive load around what to test, which was always something that bothered me. It provides a practical balance between coverage and maintainability while ensuring that real-world issues are properly addressed through test-driven bug fixes.