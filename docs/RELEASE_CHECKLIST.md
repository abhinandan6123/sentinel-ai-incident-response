# Release and submission checklist

## Local quality gate
- [ ] Create `.venv`, install requirements, and start the server.
- [ ] `pytest -q` passes.
- [ ] `GET /api/health` works.
- [ ] Run a full analyze → human-confirmed resolve → new analyze workflow.
- [ ] With `DEMO_MODE=false`, verify actual Hindsight retain and recall across separate requests; restart the app and verify the memory remains available.
- [ ] Test missing fields, long inputs, irrelevant memory, Hindsight outage, and LLM outage.
- [ ] Confirm no secret is committed; `.env` is ignored.
- [ ] Review generated recommendations for unsafe or unsupported claims.

## GitHub repository
- [ ] README includes setup, architecture, environment variables, screenshots, and limitations.
- [ ] Add screenshots/GIF and a short demo video link after recording.
- [ ] Add license only if you have chosen one.
- [ ] Add GitHub repository URL to the public social post.

## Official project deliverables
- [ ] Public GitHub repository with clean, documented code.
- [ ] Demo video and live judge demo.
- [ ] Short explanation of how Hindsight memory is used.
- [ ] Each team member's public 800–1,500-word article and social post, per organizer guidance.
- [ ] One public YouTube team video, 2–5 minutes, 1080p minimum.

## Content guide constraints
- [ ] Article title/body do not mention “hackathon”.
- [ ] Social post does not mention “hackathon” or use #Hackathon.
- [ ] Article contains a real code snippet, before/after example, screenshots/diagrams, and an honest limitation.
- [ ] Article is public and linkable; social post links to the project; Hindsight GitHub link is in a comment.
- [ ] Share article on one of the guide's suggested Reddit communities if required by your submission process.

Check the organizer portal for the actual deadline and upload fields; this repository cannot confirm portal-specific submission mechanics.
