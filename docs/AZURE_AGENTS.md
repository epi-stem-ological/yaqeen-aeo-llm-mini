# Azure AI Foundry Agents + Grounding (Design Note)

This is an **optional** path that plugs in a provider using Azure AI Foundry **Agents** with the **Grounding with Bing Search** tool.

## What you configure in Azure AI Foundry
- Project endpoint (Project → Overview → Project endpoint), e.g.  
  `https://<aihub>.services.ai.azure.com/api/projects/<projectName>`
- Project API key (Project → Manage keys)
- Bing Grounding connection (Management center → Connections → Grounding with Bing Search)
  - You’ll reference its **Connection ID** in the agent tool call
- A deployed chat model (e.g., `gpt-4o-mini`)

## How the provider will work (sketch)
- Create an agent with a system prompt: *“Given a user question, search and return sources with URLs.”*
- Allow the tool: `grounding_with_bing_search`
- For each question:
  - Send a chat turn that triggers the tool.
  - Read `groundingAttributions`/citations and assemble `ProviderResult`:
    - `cited = any(url domain matches target_domain)`
    - `cited_urls = [urls matching domain]`
    - `raw_urls = all URLs returned`
- This keeps the provider API identical to `mock`/`bing`.

> Not required for reviewers; included to show the growth path.
