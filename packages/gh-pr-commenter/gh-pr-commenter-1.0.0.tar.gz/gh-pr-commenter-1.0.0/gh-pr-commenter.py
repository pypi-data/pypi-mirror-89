#!/usr/bin/env python3
import os
import sys
import argparse
from github import Github
from jinja2 import Template


def get_pr(repo, prnumber):
    g = Github(os.environ['GH_TOKEN'])
    repo = g.get_repo(repo)
    return repo.get_pull(prnumber)


def generate_comment(pr, template_file, logfile):
    with open(template_file, 'r') as f:
        template = Template(f.read())

    with open(logfile, 'r') as f:
        log = f.read()

    return template.render(
        pullRequestAuthor=pr.user.name,
        contents=log)


def post_comment(pr, comment):
    pr.create_issue_comment(comment)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('repo',
                        help='Organization and repository (e.g. xbmc/repo-plugins)',
                        type=str)

    parser.add_argument('prnumber',
                        help='PR number (e.g. 5)',
                        type=int)

    parser.add_argument('template',
                        help='Jinja 2 template file to generate a comment from',
                        type=str)

    parser.add_argument('logfile',
                        help='Log file to parse (e.g. mylog.log)',
                        type=str)

    args = parser.parse_args()

    # Check for github token in the environment (GH_TOKEN environment variable)
    gh_token = os.environ.get('GH_TOKEN', False)
    if not gh_token:
        sys.exit('Error: GH_TOKEN environment variable not found!')

    # Check template file and log file actually exist
    if not os.path.exists(args.template):
        sys.exit('Error: Provided template file {} was not found!'.format(args.template))

    if not os.path.exists(args.logfile):
        sys.exit('Error: Provided log file {} was not found!'.format(args.template))

    pr = get_pr(args.repo, args.prnumber)
    comment = generate_comment(pr, args.template, args.logfile)
    post_comment(pr, comment)
