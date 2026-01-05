import requests
import html2text


def search_wikipedia_md(query: str) -> str:
    """
    Search Wikipedia for the given query and return the markdown of the first found page.
    The search API is the one documented here: https://www.mediawiki.org/wiki/API:Opensearch
    It follows redirects and returns the markdown of the final page.
    """
    # Step 1: Use OpenSearch API to find the first page title
    opensearch_url = "https://en.wikipedia.org/w/api.php"
    opensearch_params = {
        "action": "opensearch",
        "search": query,
        "limit": 1,
        "format": "json"
    }
    headers = {
        "User-Agent": "WikiExplainer/1.0 (https://github.com/ivoras/wikiexplainer)"
    }

    response = requests.get(opensearch_url, params=opensearch_params, headers=headers)
    response.raise_for_status()
    opensearch_data = response.json()

    # OpenSearch returns: [query, [titles], [descriptions], [urls]]
    if not opensearch_data[1] or len(opensearch_data[1]) == 0:
        raise ValueError(f"No Wikipedia page found for query: {query}")

    page_title = opensearch_data[1][0]

    # Step 2: Get HTML using the parse API (automatically follows redirects)
    parse_url = "https://en.wikipedia.org/w/api.php"
    parse_params = {
        "action": "parse",
        "page": page_title,
        "format": "json",
        "redirects": "1"  # Follow redirects
    }

    response = requests.get(parse_url, params=parse_params, headers=headers)
    response.raise_for_status()
    parse_data = response.json()

    # Check for errors in the API response
    if "error" in parse_data:
        raise ValueError(f"Error retrieving page: {parse_data['error'].get('info', 'Unknown error')}")

    # Extract HTML from the parse response
    html_content = parse_data.get("parse", {}).get("text", {}).get("*", "")

    if not html_content:
        raise ValueError(f"Could not retrieve page content for: {page_title}")

    # Step 3: Convert HTML to markdown using html2text
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    markdown = h.handle(html_content)

    return markdown


if __name__ == "__main__":
    print(search_wikipedia_md("medena"))