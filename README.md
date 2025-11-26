# PropelMe
propelme-agent/
  README.md
  requirements.txt
  src/
    __init__.py
    data_models.py          # Contact, UserProfile, Interaction
    scoring.py              # warmth & relevance formulas
    scheduling.py           # weekly planner / badge logic
    tools/
      eventbrite_tool.py    # HTTP or MCP tool wrapper
      linkedin_csv_loader.py
    agents/
      planner_agent.py      # “Concierge” agent
      messaging_agent.py    # DM / comment drafting agent
      evaluator_agent.py    # LLM-as-judge / quality checks
      orchestrator.py       # multi-agent orchestration / A2A
  data/
    sample_contacts.csv
    sample_events.json
    linkedin_example_exports/
  notebooks/
    colab_dev.ipynb         # your working notebook
    kaggle_capstone_demo.ipynb  # exported copy for Kaggle
  mcp/
    eventbrite_server/      # optional MCP server stub later