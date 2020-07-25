# Originally from simonw
import pathlib
import re
import datetime
from datetime import datetime

import feedparser

root = pathlib.Path(__file__).parent.resolve()
PYPOOLE_TILS = "https://pypoole.com/rss.xml"

time_fmt = "%a, %d %b %Y %H:%M:%S GM"
# client = GraphqlClient(endpoint="https://api.github.com/graphql")


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!-- {} starts -->.*<!-- {} ends -->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)


def fetch_til_entries():
    entries = feedparser.parse(PYPOOLE_TILS)["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": datetime.strptime(entry["published"], time_fmt).strftime("%Y-%m-%d"),
        }
        for entry in entries
    ]


if __name__ == "__main__":
    readme = root / "README.md"
    project_releases = root / "releases.md"

    readme_contents = readme.open().read()

    tils = fetch_til_entries()
    tils_md = "\n".join(
        ["* [{title}]({url}) - {published}".format(**entry) for entry in tils]
    )
    rewritten = replace_chunk(readme_contents, "tils", tils_md)

    # Once we've updated our blog add it here
    # entries = fetch_blog_entries()[:5]
    # entries_md = "\n".join(
    #     ["* [{title}]({url}) - {published}".format(**entry) for entry in entries]
    # )
    # rewritten = replace_chunk(rewritten, "blog", entries_md)

    readme.open("w").write(rewritten)
