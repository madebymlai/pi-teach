# Topic learning outcomes

Read this when creating or revising `topics/*.md`. A topic specifies what the student must know and be able to do, not the explanation that teaches it. Ground these requirements in the course sources and write in the course's language.

## Structure

```md
# <Topic>

## Scope
<Included tasks and boundaries; name adjacent material that belongs elsewhere.>

## Prerequisites
<Subject-specific dependencies needed on entry, linked to prerequisite topics where available. For an introductory topic with none, state that no prior course topic is required.>

## Required knowledge
<Named definitions, statements, notation, conditions, or distinctions the student must recall.>

## Skills and verification
| Observable skill | Task and criteria for an adequate answer |
| --- | --- |
| <Action on a specified object> | <Task conditions, required output, reasoning, and checks> |

## Exam requirements and sources
<Exact files, PDF pages, sections, or exercise numbers supporting the requirements. Distinguish confirmed assessment requirements, proposed checks, and unresolved facts.>
```

## Make outcomes testable

Use actions with objects: state a definition with its conditions, classify a relation and justify it, construct a counterexample, derive a formula, or reconstruct a proof. Replace vague goals such as "understand inclusion" with "decide whether one finite set is a subset of another, checking every element or identifying a counterexample". Keep capabilities and skills in one section.

Each skill needs a matching verification task and a criterion based on the answer's content, not merely its length or a completed checkbox. Specify permitted aids when they affect interpretation. Proposed checks and thresholds are teaching decisions, not official exam rules; label them accordingly. Prerequisites are subject-specific knowledge or skills whose absence would block this topic. Exclude generic literacy and skills taught by the topic itself; a template section is not a reason to invent dependencies.

Knowledge entries identify what must be recalled; put definitions explained at length, worked examples, proof walkthroughs, and model answers in lessons. The topic remains a concrete requirements sheet, without a theoretical-summary section. Link directly to the supporting source pages rather than duplicating their exposition.

## Ownership and revision

`lessons/lessons.md` owns lesson listings and links its topic headings to these sheets. Topic pages contain no lesson lists or personal scores. `learning-records/` owns evidence of actual performance, assistance, and retention; an outcome listed here is a target, not a claim of mastery.

Before converting an existing topic, re-read it and preserve student annotations and work. Retain unique teaching content in an appropriate lesson before removing it from the topic. A format change does not alter the agreed exam scope or roadmap.

The sheet is ready when every skill has a concrete check, requirements have traceable sources or an explicit uncertainty, and explanations, solutions, lesson lists, and personal progress remain in their respective documents.
