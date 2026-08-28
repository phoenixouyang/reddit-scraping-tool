# Reddit Scraping Tool

A lightweight Python tool for scraping Reddit posts, comments, and search results directly from subreddits without requiring API authentication.

## Features

- **Get Subreddit Posts**: Fetch posts from any subreddit with customizable sorting (hot, new, top, etc.)
- **Get Post Comments**: Retrieve comments from specific Reddit posts
- **Search Subreddits**: Search for posts within a subreddit using keywords
- **Flexible Output**: Export results to JSON format for further processing
- **Error Handling**: Built-in exception handling for network issues and timeouts

## Requirements

- Python 3.7+
- `requests` library

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install requests
```

## Usage

### Basic Usage

```python
from reddit_scraper import RedditScraper

scraper = RedditScraper()

# Get hot posts from r/gaming
posts = scraper.get_subreddit_posts('gaming', limit=25, sort='hot')

# Search for posts about "AI" in r/gaming
results = scraper.search_subreddit('gaming', 'AI', limit=100)

# Get comments from a specific post
comments = scraper.get_post_comments('gaming', 'post_id_here', limit=100)
```

### Methods

#### `get_subreddit_posts(subreddit, limit=25, sort='hot')`
Fetches posts from a subreddit.

**Parameters:**
- `subreddit` (str): Subreddit name (without r/)
- `limit` (int): Number of posts to retrieve (default: 25)
- `sort` (str): Sort order - 'hot', 'new', 'top', 'rising' (default: 'hot')

**Returns:** List of post dictionaries or None on error

**Example:**
```python
posts = scraper.get_subreddit_posts('python', limit=50, sort='top')
```

#### `get_post_comments(subreddit, post_id, limit=100)`
Fetches comments from a specific post.

**Parameters:**
- `subreddit` (str): Subreddit name
- `post_id` (str): Post ID
- `limit` (int): Number of comments to retrieve (default: 100)

**Returns:** Dictionary with post info and comments list, or None on error

#### `search_subreddit(subreddit, query, limit=25)`
Searches for posts within a subreddit.

**Parameters:**
- `subreddit` (str): Subreddit name
- `query` (str): Search query
- `limit` (int): Number of results (default: 25)

**Returns:** List of matching posts or None on error

## Data Structure

### Post Object
```json
{
  "title": "Post title",
  "author": "username",
  "score": 1234,
  "upvote_ratio": 0.95,
  "num_comments": 42,
  "created_utc": 1234567890,
  "url": "https://...",
  "permalink": "https://reddit.com/r/...",
  "selftext": "Post content",
  "is_self": true,
  "link_flair_text": "Flair",
  "subreddit": "subreddit_name"
}
```

### Comment Object
```json
{
  "author": "username",
  "body": "Comment text",
  "score": 100,
  "created_utc": 1234567890,
  "permalink": "https://reddit.com/r/.../..."
}
```

## Example: Save Posts to File

```python
from reddit_scraper import RedditScraper
import json

scraper = RedditScraper()
posts = scraper.get_subreddit_posts('programming', limit=50)

if posts:
    with open('programming_posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print("Posts saved to programming_posts.json")
```

## Notes

- Reddit may rate-limit requests. Consider adding delays between requests for large-scale scraping
- The scraper uses a user-agent header to identify itself
- Reddit's terms of service should be reviewed before large-scale scraping
- This tool does not require API authentication and works with Reddit's public JSON endpoints

## Disclaimer

This tool is for educational purposes. Users are responsible for ensuring compliance with Reddit's terms of service and applicable laws when scraping web content.
