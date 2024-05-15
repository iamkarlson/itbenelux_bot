import requests

API_BASE_URL = "https://hacker-news.firebaseio.com/v0"

class HackerNewsAction:
    def __init__(self):
        pass

    def get_json(self, url):
        resp = requests.get(url)
        return resp.json()

    def get_top_story_id(self):
        url = f"{API_BASE_URL}/topstories.json"
        top_stories = self.get_json(url)
        return top_stories[0]  # Get the first top story id

    def get_story_details(self, story_id):
        url = f"{API_BASE_URL}/item/{story_id}.json"
        return self.get_json(url)

    def get_hn_top_story_link(self):
        print("Getting top story from HN")
        top_story_id = self.get_top_story_id()
        story_details = self.get_story_details(top_story_id)
        url = story_details.get("url")
        title = story_details.get("title")
        print(f"url: {url}")
        print(f"title: {title}")
        return title, url


if __name__ == "__main__":
    hn_action = HackerNewsAction()
    hn_action.get_hn_top_story_link()
