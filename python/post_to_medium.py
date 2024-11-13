"""
Script for posting to Medium

Commands:
    git-commit: Post a blog from a git commit message. The message should
    contain the word "PUBLISH" followed by the blog name.

Usage:
    1. Create a .env file in the root directory with the following
    MEDIUM_APP_ID=your_medium_app_id
    MEDIUM_APP_SECRET=your_medium_app_secret
    MEDIUM_ACCESS_TOKEN=your_medium_access_token

    2. Install python dependencies into your .venv directory
    pip install -r requirements.txt

    3. Activate the virtual environment
    source .venv/bin/activate

    4. Run the script
    python post_to_medium.py git-commit
        --commit-msg "commit message PUBLISH post_file_name.md" /
        --blog-path "path/to/blog"
"""


import os
import click
import dotenv
from medium import Client
from typing import Optional
from pathlib import Path

dotenv.load()

ENV = os.environ


def post_to_medium(heading: str, body: str) -> Optional[str]:
    client = Client(
        application_id=ENV["MEDIUM_APP_ID"],
        application_secret=ENV["MEDIUM_APP_SECRET"]
    )
    client.access_token = ENV["MEDIUM_ACCESS_TOKEN"]

    user = client.get_current_user()
    post = client.create_post(
        user_id=user["id"],
        title=heading,
        content=body,
        content_format="markdown",
        publish_status="draft",
    )

    print(f"New post at {post['url']}")
    return post.get("url")

@click.group()
def main():
    pass


@main.command(
    name="git-commit",
    help="Git commit message to post to Medium",
)
@click.option(
    "commit_msg",
    "--commit-msg",
    type=str
)
@click.option(
    "posts_path",
    "--posts-path",
    type=click.Path()
)
def post_from_git_commit(
    commit_msg: str,
    posts_path: Path,
):
    posts_dir_files = os.listdir(posts_path)

    if "PUBLISH" in commit_msg.upper():
        commit_file_name = commit_msg.upper().split("PUBLISH")[1].strip()[:-1]
        for filename in posts_dir_files:
            if commit_file_name == filename.strip():
                post_path = os.path.join(posts_path, filename)
                with open(post_path, "r") as file:
                    body = file.read()
                post_to_medium(filename, body)


if __name__ == "__main__":
    main()
