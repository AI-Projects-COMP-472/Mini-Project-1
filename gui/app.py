"""Simple Tkinter GUI for the Student Support AI assistant."""

from __future__ import annotations

import queue
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from assistant import AssistantConfig, AssistantResponse, SupportAssistant


class StudentSupportApp:
    """Small desktop interface for trying the assistant visually."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Student Support AI")
        self.root.geometry("860x640")
        self.root.minsize(720, 560)
        self.root.configure(bg="#eef3f8")

        self.assistant: SupportAssistant | None = None
        self.result_queue: queue.Queue[tuple[str, object]] = queue.Queue()
        self.placeholder_text = "Type your student support question here..."
        self.placeholder_active = True

        self._build_ui()
        self._set_input_enabled(False)
        self._append_system_message("Loading models and knowledge base. This may take a moment...")
        self._load_assistant_in_background()
        self._poll_queue()

    def _build_ui(self) -> None:
        header = tk.Frame(self.root, bg="#102a43", padx=28, pady=16)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="Student Support AI",
            bg="#102a43",
            fg="white",
            font=("Segoe UI", 20, "bold"),
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="A simple visual demo for semantic search, sentiment analysis, and escalation logic.",
            bg="#102a43",
            fg="#d9e8f5",
            font=("Segoe UI", 10),
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        content = tk.Frame(self.root, bg="#eef3f8", padx=24, pady=16)
        content.pack(fill=tk.BOTH, expand=True)

        chat_label = tk.Label(
            content,
            text="Conversation",
            bg="#eef3f8",
            fg="#243b53",
            font=("Segoe UI", 11, "bold"),
        )
        chat_label.pack(anchor="w", pady=(0, 8))

        self.chat_display = scrolledtext.ScrolledText(
            content,
            height=13,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="white",
            fg="#1f2933",
            insertbackground="#1f2933",
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground="#cbd5e1",
            highlightcolor="#2563eb",
            font=("Segoe UI", 10),
            padx=18,
            pady=12,
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        self.chat_display.tag_configure("system", foreground="#64748b", spacing3=10)
        self.chat_display.tag_configure("user", foreground="#1d4ed8", font=("Segoe UI", 10, "bold"), spacing3=6)
        self.chat_display.tag_configure("assistant", foreground="#172554", spacing3=10)
        self.chat_display.tag_configure("warning", foreground="#b42318", font=("Segoe UI", 10, "bold"))

        input_frame = tk.Frame(content, bg="#eef3f8", pady=10)
        input_frame.pack(fill=tk.X)

        input_label = tk.Label(
            input_frame,
            text="Ask your question",
            bg="#eef3f8",
            fg="#243b53",
            font=("Segoe UI", 11, "bold"),
        )
        input_label.pack(anchor="w", pady=(0, 7))

        entry_row = tk.Frame(input_frame, bg="#eef3f8")
        entry_row.pack(fill=tk.X)

        self.message_entry = tk.Text(
            entry_row,
            height=2,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=2,
            highlightbackground="#cbd5e1",
            highlightcolor="#2563eb",
            bg="white",
            fg="#94a3b8",
            insertbackground="#1f2933",
            padx=14,
            pady=10,
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 12))
        self.message_entry.insert("1.0", self.placeholder_text)
        self.message_entry.bind("<FocusIn>", self._clear_placeholder)
        self.message_entry.bind("<FocusOut>", self._restore_placeholder)
        self.message_entry.bind("<Return>", self._handle_send)

        self.send_button = tk.Button(
            entry_row,
            text="Send",
            command=self._handle_send,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief=tk.FLAT,
            padx=28,
            pady=13,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
        )
        self.send_button.pack(side=tk.RIGHT, fill=tk.Y)

        footer = tk.Frame(self.root, bg="#dbeafe", padx=24, pady=10)
        footer.pack(fill=tk.X)

        self.status_var = tk.StringVar(value="Starting...")
        status = tk.Label(
            footer,
            textvariable=self.status_var,
            bg="#dbeafe",
            fg="#334e68",
            font=("Segoe UI", 9),
            anchor="w",
        )
        status.pack(fill=tk.X)

    def _load_assistant_in_background(self) -> None:
        thread = threading.Thread(target=self._load_assistant, daemon=True)
        thread.start()

    def _load_assistant(self) -> None:
        try:
            config = AssistantConfig(knowledge_base_path=PROJECT_ROOT / "data" / "knowledge_base.csv")
            assistant = SupportAssistant(config)
        except Exception as error:
            self.result_queue.put(("startup_error", error))
        else:
            self.result_queue.put(("startup_complete", assistant))

    def _poll_queue(self) -> None:
        try:
            while True:
                event, payload = self.result_queue.get_nowait()
                if event == "startup_complete":
                    self.assistant = payload
                    self._set_input_enabled(True)
                    self.status_var.set("Ready")
                    self._append_system_message("Ready. Try asking: How do I reset my password?")
                    self.message_entry.focus_set()
                elif event == "startup_error":
                    self.status_var.set("Startup failed")
                    self._append_system_message(f"Startup error: {payload}")
                    messagebox.showerror("Startup error", str(payload))
                elif event == "response":
                    self._set_input_enabled(True)
                    self.status_var.set("Ready")
                    self._append_response(payload)
                    self.message_entry.focus_set()
                elif event == "message_error":
                    self._set_input_enabled(True)
                    self.status_var.set("Ready")
                    self._append_system_message(f"Error: {payload}")
                    self.message_entry.focus_set()
        except queue.Empty:
            pass

        self.root.after(100, self._poll_queue)

    def _handle_send(self, event: tk.Event | None = None) -> None:
        if event is not None:
            event.widget.after(1, lambda: "break")

        if self.assistant is None:
            return "break"

        message = self._get_message_text()
        if not message or self.placeholder_active:
            return "break"

        self._set_message_text("")
        self._append_user_message(message)
        self._set_input_enabled(False)
        self.status_var.set("Thinking...")

        thread = threading.Thread(target=self._process_message, args=(message,), daemon=True)
        thread.start()
        return "break"

    def _process_message(self, message: str) -> None:
        try:
            assert self.assistant is not None
            response = self.assistant.process_message(message)
        except Exception as error:
            self.result_queue.put(("message_error", error))
        else:
            self.result_queue.put(("response", response))

    def _append_user_message(self, message: str) -> None:
        self._write_chat(f"You: {message}\n", "user")

    def _append_response(self, response: AssistantResponse) -> None:
        lines = [
            f"Assistant: {response.answer}",
            f"Sentiment: {response.sentiment_label} ({response.sentiment_score:.2f})",
            f"Match confidence: {response.similarity_score:.2f}",
        ]

        if response.should_escalate:
            lines.append("Recommended escalation: Contact human advisor.")

        self._write_chat("\n".join(lines) + "\n\n", "assistant")

        if response.should_escalate:
            self._write_chat("Escalation recommended for this message.\n\n", "warning")

    def _append_system_message(self, message: str) -> None:
        self._write_chat(f"{message}\n\n", "system")

    def _write_chat(self, text: str, tag: str) -> None:
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, text, tag)
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _set_input_enabled(self, enabled: bool) -> None:
        state = tk.NORMAL if enabled else tk.DISABLED
        self.message_entry.configure(state=state)
        self.send_button.configure(state=state)

    def _get_message_text(self) -> str:
        return self.message_entry.get("1.0", tk.END).strip()

    def _set_message_text(self, text: str) -> None:
        self.message_entry.configure(state=tk.NORMAL)
        self.message_entry.delete("1.0", tk.END)
        if text:
            self.message_entry.insert("1.0", text)
        self.placeholder_active = False

    def _clear_placeholder(self, event: tk.Event | None = None) -> None:
        if self.placeholder_active and self.message_entry.cget("state") == tk.NORMAL:
            self.message_entry.delete("1.0", tk.END)
            self.message_entry.configure(fg="#1f2933")
            self.placeholder_active = False

    def _restore_placeholder(self, event: tk.Event | None = None) -> None:
        if not self._get_message_text():
            self.message_entry.insert("1.0", self.placeholder_text)
            self.message_entry.configure(fg="#94a3b8")
            self.placeholder_active = True


def main() -> None:
    root = tk.Tk()
    StudentSupportApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
