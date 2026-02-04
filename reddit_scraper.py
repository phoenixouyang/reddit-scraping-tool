#!/usr/bin/env python3

import requests
import json
import time
from typing import List, Dict, Optional


class RedditScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 reddit_scrapper project'
        }
    
    # get posts from a subreddit
    def get_subreddit_posts(self, subreddit: str, limit: int = 25, sort: str = 'hot') -> Optional[List[Dict]]:

        url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            posts = []
            
            # Extract post information from JSON structure
            for child in data['data']['children']:
                post = child['data']
                post_info = {
                    'title': post.get('title'),
                    'author': post.get('author'),
                    'score': post.get('score'),
                    'upvote_ratio': post.get('upvote_ratio'),
                    'num_comments': post.get('num_comments'),
                    'created_utc': post.get('created_utc'),
                    'url': post.get('url'),
                    'permalink': f"https://www.reddit.com{post.get('permalink')}",
                    'selftext': post.get('selftext'),
                    'is_self': post.get('is_self'),
                    'link_flair_text': post.get('link_flair_text'),
                    'subreddit': post.get('subreddit')
                }
                posts.append(post_info)
            
            return posts
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching subreddit posts: {e}")
            return None
    
    # get comments from a specific post by id
    def get_post_comments(self, subreddit: str, post_id: str, limit: int = 100) -> Optional[Dict]:

        url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json?limit={limit}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # First element is the post itself
            post_data = data[0]['data']['children'][0]['data']
            
            # Second element contains comments
            comments_data = data[1]['data']['children']
            
            comments = []
            for comment in comments_data:
                if comment['kind'] == 't1':  # t1 is a comment
                    comment_info = {
                        'author': comment['data'].get('author'),
                        'body': comment['data'].get('body'),
                        'score': comment['data'].get('score'),
                        'created_utc': comment['data'].get('created_utc'),
                        'permalink': f"https://www.reddit.com{comment['data'].get('permalink')}"
                    }
                    comments.append(comment_info)
            
            return {
                'post': {
                    'title': post_data.get('title'),
                    'author': post_data.get('author'),
                    'selftext': post_data.get('selftext')
                },
                'comments': comments
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching post comments: {e}")
            return None
    
    # get posts within a subreddit matching a search query
    def search_subreddit(self, subreddit: str, query: str, limit: int = 25) -> Optional[List[Dict]]:

        url = f"https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=1&limit={limit}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            posts = []
            
            for child in data['data']['children']:
                post = child['data']
                post_info = {
                    'title': post.get('title'),
                    'author': post.get('author'),
                    'score': post.get('score'),
                    'num_comments': post.get('num_comments'),
                    'permalink': f"https://www.reddit.com{post.get('permalink')}"
                }
                posts.append(post_info)
            
            return posts
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching subreddit: {e}")
            return None


def main():
    scraper = RedditScraper()
    
    # Example: Search within a subreddit
    print("\n" + "="*80)
    print("Searching for 'tutorial' in r/python...")
    search_results = scraper.search_subreddit('gaming', ' AI ', limit=100)
    
    # if search_results:
    #     for i, post in enumerate(search_results, 1):
    #         print(f"\n{i}. {post['title']}")
    #         print(f"   Score: {post['score']} | Comments: {post['num_comments']}")
    
    # # Example: Save posts to JSON file
    # print("\n" + "="*80)
    # print("Saving posts to file...")
    # programming_posts = scraper.get_subreddit_posts('programming', limit=10, sort='top')
    
    # if programming_posts:
    #     with open('/home/claude/reddit_posts.json', 'w', encoding='utf-8') as f:
    #         json.dump(programming_posts, f, indent=2, ensure_ascii=False)
    # #     print("Posts saved to reddit_posts.json")

    # results = scraper.get_subreddit_posts('gaming', 100, "new")
    # print(results)

    if search_results:
        with open('./gaming_ai_posts.json', 'w', encoding='utf-8') as f:
            json.dump(search_results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
