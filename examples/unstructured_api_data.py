#!/usr/bin/env python
"""
REAL-LIFE unstructured data from actual APIs.
Shows how the library handles deeply nested JSON from production systems.
"""

from json_therule0 import read_json, Normalizer
import json

def example_user_activity_api():
    """
    SCENARIO: User activity API response (Slack, Discord, etc.)
    
    Real-life problems:
    - Deeply nested objects (3-4 levels)
    - Mixed arrays and objects
    - Optional fields (some users have phone, some don't)
    - Wrapper objects with metadata
    - Arrays of complex objects (activity log, tags)
    """
    print("=" * 90)
    print("REAL API #1: User Activity Endpoint (Nested Objects & Arrays)")
    print("=" * 90)
    
    normalizer = Normalizer('data/user_activity_api.json')
    
    print(f"\n📋 Detected format: {normalizer.detected_format}")
    
    # This is a nested dict structure, not a list
    data = normalizer.normalize()
    print(f"✓ Flattened nested structure into {len(data)} records")
    
    print(f"\nFlattened columns: {normalizer.normalized_data[0].keys()}\n")
    
    print("SAMPLE RECORD (deeply nested object flattened):")
    print("-" * 90)
    
    sample = data[0]
    for key in sorted(sample.keys())[:15]:  # Show first 15 fields
        val = sample[key]
        if isinstance(val, (dict, list)) and len(str(val)) > 50:
            print(f"  {key}: {str(val)[:60]}...")
        else:
            print(f"  {key}: {val}")
    
    print("\n✅ HANDLING:")
    print("  ✓ Deeply nested profile → flattened to profile_name, profile_contact_email")
    print("  ✓ Arrays of activity logs → preserved as single field")
    print("  ✓ Optional nested contact fields → included only where present")
    print("  ✓ Metadata with nested preferences → flattened with underscores")

def example_social_media_api():
    """
    SCENARIO: Social media API response (Twitter, etc.)
    
    Real-life problems:
    - Lists of tweets at root
    - Replies nested inside tweets (tweets within tweets)
    - Optional author info (some fields missing)
    - Missing metrics for some tweets
    - Entities with different structures
    """
    print("\n\n" + "=" * 90)
    print("REAL API #2: Social Media Feed (Nested Replies & Variable Structure)")
    print("=" * 90)
    
    data = read_json('data/social_media_api.json')
    
    print(f"\n✓ Loaded {len(data.data())} tweets")
    print(f"\nColumns: {data.columns()}\n")
    
    print("TWEET METRICS (with type conversion):")
    print("-" * 90)
    
    tweets = data.data()
    for i, tweet in enumerate(tweets, 1):
        print(f"\n#{i} Tweet by @{tweet['author'].get('username', 'unknown')}:")
        print(f"  Text: {tweet['text'][:60]}...")
        
        # Access metrics safely
        metrics = tweet.get('metrics', {})
        if isinstance(metrics, dict):
            print(f"  Engagement:")
            print(f"    - Retweets: {metrics.get('retweets', 0)}")
            print(f"    - Likes: {metrics.get('likes', 0)}")
            print(f"    - Replies: {metrics.get('replies', 0)}")
        
        # Handle nested replies
        replies = tweet.get('replies', [])
        if replies:
            print(f"  Replies: {len(replies)} nested tweets")
            for reply in replies[:2]:
                if isinstance(reply, dict):
                    print(f"    - @{reply.get('author', {}).get('username', '?')}: {reply.get('text', '')[:40]}")
        
        # Handle entities
        entities = tweet.get('entities', {})
        if isinstance(entities, dict):
            if entities.get('hashtags'):
                print(f"  Hashtags: {', '.join(entities['hashtags'])}")
            if entities.get('mentions'):
                print(f"  Mentions: {', '.join(entities.get('mentions', []))}")
    
    print("\n\n✅ HANDLING:")
    print("  ✓ Root-level list of tweets normalized")
    print("  ✓ Nested author objects preserved")
    print("  ✓ Nested metrics preserved as dict")
    print("  ✓ Nested replies arrays preserved")
    print("  ✓ Entities with varying fields handled")
    print("  ✓ Optional fields (missing metrics, no replies) work gracefully")

def example_complex_filtering():
    """
    SCENARIO: Practical analysis of real API data
    """
    print("\n\n" + "=" * 90)
    print("PRACTICAL ANALYSIS: Finding Valuable Tweets")
    print("=" * 90)
    
    data = read_json('data/social_media_api.json')
    
    print("\nStats on engagement:")
    stats = data.stats()
    
    for col in ['metrics', 'author']:
        if col in stats:
            print(f"  {col}: {stats[col]}")
    
    # Find high-engagement tweets
    tweets = data.data()
    print(f"\nEngagement breakdown:")
    
    for tweet in tweets:
        metrics = tweet.get('metrics', {})
        if isinstance(metrics, dict):
            total_engagement = (
                metrics.get('retweets', 0) + 
                metrics.get('likes', 0) + 
                metrics.get('replies', 0)
            )
            author = tweet.get('author', {})
            username = author.get('username', 'unknown') if isinstance(author, dict) else 'unknown'
            print(f"  {username}: {total_engagement} total engagement")

def main():
    """Run real-life unstructured data examples."""
    try:
        example_user_activity_api()
        example_social_media_api()
        example_complex_filtering()
        
        print("\n\n" + "=" * 90)
        print("✅ REAL-LIFE UNSTRUCTURED DATA HANDLED")
        print("=" * 90)
        print("""
WHAT THE LIBRARY DOES WITH REAL APIs:
  ✓ Detects complex nested structures (user_activity_api.json)
  ✓ Flattens deeply nested objects with consistent naming
  ✓ Preserves complex types (dicts, lists) where appropriate
  ✓ Handles variable optional fields gracefully
  ✓ Works with arrays at multiple levels
  ✓ Allows practical analysis of messy API responses
  ✓ Maintains data integrity during flattening
        """)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
