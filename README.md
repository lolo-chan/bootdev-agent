This is the codebase for the AI Agent project course on boot.dev.

Few things to note:
1. The main() function inside main.py currently does not handle exiting the loop properly. If the number of LLM calls exceeds 20 without a single tool call, it should exit the program gracefully.
2. More features are to be added. I plan on turning this into a much more capable AI assistant. New features are to be researched and developed.
3. Also try switching from Gemini to Claude, using Anthropic's own SDK.
4. Eventually give the Agent capabilities similar to Claude Code or Codex.