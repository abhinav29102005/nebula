"""
intelligence/reflection.py – Episodic Memory and RAG Reflection
===============================================================
Enables the agent to query its past trajectories and generate
a "Lesson Learned" to guide future plans.
"""

from __future__ import annotations

import json
from typing import Dict, Any, List
from config.logging_config import get_logger

logger = get_logger("intelligence.reflection")

class ReflectionEngine:
    def __init__(self, db_manager):
        self.db = db_manager

    async def reflect_on_task(self, session_id: str, prompt: str, plan: str, actions: List[Dict[str, Any]], outcome: str) -> None:
        """Saves a completed trajectory to the episodic memory database."""
        try:
            logger.info(f"Saving trajectory to episodic memory for task: {prompt[:30]}...")
            await self.db.add_trajectory(session_id, prompt, plan, actions, outcome)
        except Exception as e:
            logger.error(f"Failed to save trajectory: {e}")

    async def retrieve_lessons(self, current_prompt: str, limit: int = 3) -> str:
        """Retrieves lessons from recent trajectories."""
        # Note: In a full RAG system, this would use semantic search (Weaviate).
        # For now, it retrieves the most recent trajectories that might be relevant.
        try:
            trajectories = await self.db.get_recent_trajectories(limit=limit)
            if not trajectories:
                return "No past lessons available."

            lessons = []
            for t in trajectories:
                lessons.append(f"Past Task: {t['prompt']}\nOutcome: {t['outcome']}\nActions Taken: {len(t['actions'])}")
            
            return "\n\n".join(lessons)
        except Exception as e:
            logger.error(f"Failed to retrieve lessons: {e}")
            return "Failed to retrieve past lessons."
