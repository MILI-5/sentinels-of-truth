@"
# Sentinels of Truth

AI-powered multi-agent claim verification and knowledge-base system.

## Overview

Sentinels of Truth is a multi-agent verification system that investigates user-submitted claims, checks available evidence against a knowledge base, and produces a final decision.

The system uses a graph-based agent workflow to process claims through multiple stages:

1. **Alpha Agent** — analyzes the claim and searches the evidence/knowledge base.
2. **Beta Agent** — compares the claim against existing knowledge and detects matches or contradictions.
3. **Decision Agent** — generates the final action.
4. **SQLite Database** — stores verified claims and their verification metadata.
5. **React Frontend** — displays the investigation process and final result.

## Architecture

```text
User Claim
    |
    v
React Frontend
    |
    v
FastAPI Backend
    |
    v
LangGraph Workflow
    |
    +-------------------+
    |                   |
    v                   v
Alpha Agent        Knowledge Base
    |
    v
Beta Agent
    |
    v
Decision Agent
    |
    +--------+----------+
             |
       +-----+-----+
       |     |     |
       v     v     v
    INSERT DISCARD FLAG
       |
       v
   SQLite Database