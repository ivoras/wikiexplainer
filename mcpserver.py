from wiki import search_wikipedia_md
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("knowledge", stateless_http=True)

@mcp.tool(name="search_knowledge", description="If at all unsure about something, use this tool to search for knowledge. It can search for individual person, product, organization or event names, and for locations and scientific terms. Never use compound sentences or questions as queries.")
def search_knowledge(query: str) -> str:
    return search_wikipedia_md(query)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
