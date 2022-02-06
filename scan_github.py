import os
from github import Github
from collections import Counter
import pprint
from dotenv import load_dotenv

load_dotenv()

pp = pprint.PrettyPrinter()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


g = Github(client_id, client_secret)


def language_breakdown(repos):
    return [Counter(r.get_languages()) for r in repos]


def get_languages(user):
    repos = user.get_repos()
    langs = language_breakdown(repos)
    summed = sum(langs, Counter())
    tuples = [(value, key) for key, value in summed.items()]
    tuples.sort(key=(lambda t: t[0]), reverse=True)
    
    tech_stack = [t[1] for t in tuples[0:5]]
    experience = sum(map(lambda t: t[0], tuples))
    return (experience, tech_stack)

def parse_repos(user):
  repos = user.get_repos()
  stars = 0
  for repo in repos:
    stars += repo.stargazers_count
    
  return stars
  


def get_stars(user):
    repos = user.get_starred()
    langs = language_breakdown(repos)

    pp.pprint(sum(langs, Counter()))


def scan_github(username: str):
    user = g.get_user(username)
    experience, tech_stack = get_languages(user)
    starred = parse_repos(user)
    print(experience, tech_stack, starred)
    # get_stars(user)


scan_github("ethanrange")
