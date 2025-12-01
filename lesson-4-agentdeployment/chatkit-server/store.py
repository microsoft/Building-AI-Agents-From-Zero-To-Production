"""
SQLite-based storage for ChatKit threads and messages.

This module implements the ChatKit Store protocol using SQLite for persistence.
It handles thread management and message storage for the ChatKit server.
"""

import json
import logging
import sqlite3
import uuid
from datetime import datetime
from typing import Any

from chatkit.types import (
    CreateThreadRequest,
    LoadThreadItemsResponse,
    LoadThreadsResponse,
    ListItemsCursor,
    ThreadItem,
    ThreadMetadata,
    UserMessageItem,
    AssistantMessageItem,
    TextContent,
)

logger = logging.getLogger(__name__)


class SQLiteStore:
    """SQLite-based storage implementing ChatKit Store protocol."""

    def __init__(self, db_path: str = "chatkit_onboarding.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Threads table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS threads (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    metadata TEXT
                )
            """)
            
            # Thread items (messages) table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS thread_items (
                    id TEXT PRIMARY KEY,
                    thread_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE
                )
            """)
            
            # Create indexes for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_thread_items_thread_id 
                ON thread_items(thread_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_thread_items_created_at 
                ON thread_items(thread_id, created_at)
            """)
            
            conn.commit()
        logger.info(f"Database initialized at {self.db_path}")

    async def create_thread(
        self, request: CreateThreadRequest, context: dict[str, Any]
    ) -> ThreadMetadata:
        """Create a new conversation thread."""
        thread_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        title = request.title if request.title else "New Conversation"
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO threads (id, title, created_at, updated_at, metadata) VALUES (?, ?, ?, ?, ?)",
                (thread_id, title, now, now, json.dumps({}))
            )
            conn.commit()
        
        logger.info(f"Created thread: {thread_id}")
        return ThreadMetadata(
            id=thread_id,
            title=title,
            created_at=datetime.fromisoformat(now),
        )

    async def save_thread(
        self, thread: ThreadMetadata, context: dict[str, Any]
    ) -> ThreadMetadata:
        """Save or update a thread."""
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE threads SET title = ?, updated_at = ? WHERE id = ?",
                (thread.title, now, thread.id)
            )
            conn.commit()
        
        return thread

    async def load_thread(
        self, thread_id: str, context: dict[str, Any]
    ) -> ThreadMetadata | None:
        """Load a thread by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, title, created_at, updated_at FROM threads WHERE id = ?",
                (thread_id,)
            )
            row = cursor.fetchone()
        
        if row is None:
            return None
        
        return ThreadMetadata(
            id=row[0],
            title=row[1],
            created_at=datetime.fromisoformat(row[2]),
        )

    async def load_threads(
        self, 
        after: str | None, 
        limit: int, 
        context: dict[str, Any]
    ) -> LoadThreadsResponse:
        """Load all threads with pagination."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if after:
                cursor.execute(
                    """SELECT id, title, created_at FROM threads 
                       WHERE created_at < (SELECT created_at FROM threads WHERE id = ?)
                       ORDER BY created_at DESC LIMIT ?""",
                    (after, limit + 1)
                )
            else:
                cursor.execute(
                    "SELECT id, title, created_at FROM threads ORDER BY created_at DESC LIMIT ?",
                    (limit + 1,)
                )
            
            rows = cursor.fetchall()
        
        has_more = len(rows) > limit
        threads = [
            ThreadMetadata(
                id=row[0],
                title=row[1],
                created_at=datetime.fromisoformat(row[2]),
            )
            for row in rows[:limit]
        ]
        
        next_cursor = threads[-1].id if has_more and threads else None
        
        return LoadThreadsResponse(
            data=threads,
            cursor=ListItemsCursor(next_cursor=next_cursor) if next_cursor else ListItemsCursor(),
        )

    async def delete_thread(self, thread_id: str, context: dict[str, Any]) -> None:
        """Delete a thread and all its messages."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM thread_items WHERE thread_id = ?", (thread_id,))
            cursor.execute("DELETE FROM threads WHERE id = ?", (thread_id,))
            conn.commit()
        
        logger.info(f"Deleted thread: {thread_id}")

    async def save_thread_item(
        self, 
        thread_id: str, 
        item: ThreadItem, 
        context: dict[str, Any]
    ) -> ThreadItem:
        """Save a message to a thread."""
        now = datetime.now().isoformat()
        
        # Determine role and content
        role = "user" if isinstance(item, UserMessageItem) else "assistant"
        content_text = ""
        if item.content:
            for content_part in item.content:
                if hasattr(content_part, "text"):
                    content_text = content_part.text
                    break
        
        item_id = item.id if item.id else str(uuid.uuid4())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT OR REPLACE INTO thread_items 
                   (id, thread_id, role, content, created_at) VALUES (?, ?, ?, ?, ?)""",
                (item_id, thread_id, role, content_text, now)
            )
            # Update thread's updated_at timestamp
            cursor.execute(
                "UPDATE threads SET updated_at = ? WHERE id = ?",
                (now, thread_id)
            )
            conn.commit()
        
        return item

    async def load_thread_items(
        self,
        thread_id: str,
        after: str | None,
        limit: int,
        order: str,
        context: dict[str, Any],
    ) -> LoadThreadItemsResponse:
        """Load messages from a thread."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            order_direction = "ASC" if order == "asc" else "DESC"
            
            if after:
                cursor.execute(
                    f"""SELECT id, role, content, created_at FROM thread_items 
                        WHERE thread_id = ? AND created_at > 
                            (SELECT created_at FROM thread_items WHERE id = ?)
                        ORDER BY created_at {order_direction} LIMIT ?""",
                    (thread_id, after, limit + 1)
                )
            else:
                cursor.execute(
                    f"""SELECT id, role, content, created_at FROM thread_items 
                        WHERE thread_id = ? ORDER BY created_at {order_direction} LIMIT ?""",
                    (thread_id, limit + 1)
                )
            
            rows = cursor.fetchall()
        
        has_more = len(rows) > limit
        items: list[ThreadItem] = []
        
        for row in rows[:limit]:
            item_id, role, content, created_at = row
            content_obj = [TextContent(type="text", text=content)]
            created_dt = datetime.fromisoformat(created_at)
            
            if role == "user":
                items.append(UserMessageItem(
                    id=item_id,
                    thread_id=thread_id,
                    created_at=created_dt,
                    content=content_obj,
                ))
            else:
                items.append(AssistantMessageItem(
                    id=item_id,
                    thread_id=thread_id,
                    created_at=created_dt,
                    content=content_obj,
                ))
        
        next_cursor = items[-1].id if has_more and items else None
        
        return LoadThreadItemsResponse(
            data=items,
            cursor=ListItemsCursor(next_cursor=next_cursor) if next_cursor else ListItemsCursor(),
        )

    async def delete_thread_item(
        self, thread_id: str, item_id: str, context: dict[str, Any]
    ) -> None:
        """Delete a specific message from a thread."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM thread_items WHERE id = ? AND thread_id = ?",
                (item_id, thread_id)
            )
            conn.commit()
        
        logger.info(f"Deleted item {item_id} from thread {thread_id}")
