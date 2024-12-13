"""
Script for managing Medium posts based on git changes

Commands:
    publish: Publish or update posts based on git changes between commits
    delete: Delete a post from Medium

Usage:
    1. Create a .env file in the root directory with the following
    MEDIUM_APP_ID=your_medium_app_id
    MEDIUM_APP_SECRET=your_medium_app_secret
    MEDIUM_ACCESS_TOKEN=your_medium_access_token

    2. Install dependencies:
    pip install -r requirements.txt

    3. Run the script:
    # Publish/update changes between commits
    python post_to_medium.py publish --commit-hash HEAD --posts-path ./blog-posts

    # Delete a post
    python post_to_medium.py delete --post-id abc123
"""

import os
import click
import dotenv
import logging
import git
from medium import Client
from typing import Optional, List, Dict
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'medium_posts_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
dotenv.load_dotenv()

@dataclass
class GitChange:
    """Represents a changed file in git"""
    path: str
    status: str  # 'A' for added, 'M' for modified, 'D' for deleted
    post_id: Optional[str] = None  # Medium post ID if exists

class MediumClientError(Exception):
    """Custom exception for Medium client errors"""
    pass

class GitError(Exception):
    """Custom exception for Git operations"""
    pass

class MediumClient:
    def __init__(self):
        try:
            self.client = Client(
                application_id=os.environ["MEDIUM_APP_ID"],
                application_secret=os.environ["MEDIUM_APP_SECRET"]
            )
            self.client.access_token = os.environ["MEDIUM_ACCESS_TOKEN"]
            self.user = self.client.get_current_user()

            # Load post mappings from a local file
            self.post_mappings = self._load_post_mappings()

        except KeyError as e:
            logger.error(f"Missing environment variable: {e}")
            raise MediumClientError("Missing required environment variables")
        except Exception as e:
            logger.error(f"Failed to initialize Medium client: {e}")
            raise MediumClientError(f"Medium client initialization failed: {e}")

    def _load_post_mappings(self) -> Dict[str, str]:
        """Load mapping of local files to Medium post IDs"""
        try:
            if os.path.exists('post_mappings.json'):
                import json
                with open('post_mappings.json', 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.warning(f"Failed to load post mappings: {e}")
            return {}

    def _save_post_mappings(self):
        """Save mapping of local files to Medium post IDs"""
        try:
            import json
            with open('post_mappings.json', 'w') as f:
                json.dump(self.post_mappings, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save post mappings: {e}")

    def create_post(self, title: str, content: str, filepath: str) -> Optional[str]:
        """Create a new post on Medium"""
        try:
            post = self.client.create_post(
                user_id=self.user["id"],
                title=title,
                content=content,
                content_format="markdown",
                publish_status="draft",
            )
            post_url = post.get("url")
            post_id = post.get("id")

            # Save mapping
            if post_id:
                self.post_mappings[filepath] = post_id
                self._save_post_mappings()

            logger.info(f"Successfully created new post: {post_url}")
            return post_url
        except Exception as e:
            logger.error(f"Failed to create post: {e}")
            raise MediumClientError(f"Post creation failed: {e}")

    def update_post(self, post_id: str, title: str, content: str) -> Optional[str]:
        """Update an existing post on Medium"""
        try:
            post = self.client.update_post(
                post_id=post_id,
                title=title,
                content=content,
                content_format="markdown",
            )
            post_url = post.get("url")
            logger.info(f"Successfully updated post: {post_url}")
            return post_url
        except Exception as e:
            logger.error(f"Failed to update post: {e}")
            raise MediumClientError(f"Post update failed: {e}")

    def delete_post(self, post_id: str) -> bool:
        """Delete a post from Medium"""
        try:
            self.client.delete_post(post_id)

            # Remove from mappings
            filepath = next((k for k, v in self.post_mappings.items() if v == post_id), None)
            if filepath:
                del self.post_mappings[filepath]
                self._save_post_mappings()

            logger.info(f"Successfully deleted post: {post_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete post: {e}")
            raise MediumClientError(f"Post deletion failed: {e}")

class GitHandler:
    def __init__(self, repo_path: str = '.'):
        try:
            self.repo = git.Repo(repo_path)
        except Exception as e:
            logger.error(f"Failed to initialize git repo: {e}")
            raise GitError(f"Git initialization failed: {e}")

    def get_changed_files(self, commit_hash: str, posts_path: str) -> List[GitChange]:
        """Get list of changed markdown files between commits"""
        try:
            commit = self.repo.commit(commit_hash)
            prev_commit = commit.parents[0] if commit.parents else None

            if not prev_commit:
                return []

            diff_index = prev_commit.diff(commit)
            changed_files = []

            for diff in diff_index:
                file_path = diff.a_path or diff.b_path
                if not file_path.endswith('.md') or not file_path.startswith(posts_path):
                    continue

                if diff.new_file:
                    status = 'A'
                elif diff.deleted_file:
                    status = 'D'
                else:
                    status = 'M'

                changed_files.append(GitChange(path=file_path, status=status))

            return changed_files
        except Exception as e:
            logger.error(f"Failed to get changed files: {e}")
            raise GitError(f"Git operation failed: {e}")

def process_changes(changes: List[GitChange], medium_client: MediumClient):
    """Process git changes and update Medium accordingly"""
    for change in changes:
        try:
            if change.status in ['A', 'M']:  # Added or Modified
                with open(change.path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    title = os.path.basename(change.path)

                    # Check if post exists
                    post_id = medium_client.post_mappings.get(change.path)
                    if post_id:
                        medium_client.update_post(post_id, title, content)
                    else:
                        medium_client.create_post(title, content, change.path)

            elif change.status == 'D':  # Deleted
                post_id = medium_client.post_mappings.get(change.path)
                if post_id:
                    medium_client.delete_post(post_id)

        except Exception as e:
            logger.error(f"Failed to process change {change.path}: {e}")

@click.group()
def main():
    pass

@main.command()
@click.option(
    '--commit-hash',
    required=True,
    help='Git commit hash to process changes from'
)
@click.option(
    '--posts-path',
    required=True,
    type=click.Path(exists=True),
    help='Path to directory containing blog posts'
)
def publish(commit_hash: str, posts_path: str):
    """Publish or update posts based on git changes"""
    try:
        git_handler = GitHandler()
        medium_client = MediumClient()

        changes = git_handler.get_changed_files(commit_hash, posts_path)
        if not changes:
            click.echo("No relevant changes found")
            return

        process_changes(changes, medium_client)
        click.echo("Successfully processed all changes")

    except (GitError, MediumClientError) as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

@main.command()
@click.option(
    '--post-id',
    required=True,
    help='Medium post ID to delete'
)
def delete(post_id: str):
    """Delete a post from Medium"""
    try:
        medium_client = MediumClient()
        medium_client.delete_post(post_id)
        click.echo(f"Successfully deleted post: {post_id}")
    except MediumClientError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

if __name__ == "__main__":
    main()
