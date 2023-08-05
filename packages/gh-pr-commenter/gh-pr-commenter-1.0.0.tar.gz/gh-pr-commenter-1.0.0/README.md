# github-pr-log-commenter

Simple script that posts a comment to a Github PR based on a jinja2 template. This template has two simple variables:

`{{pullRequestAuthor}}`: Will be replaced by the author of the pull request

`{{contents}}`: Will be replaced by the contents of a given file (e.g. a log)

You need to define the `GH_TOKEN` environment variable with at least the repo scope.

# usage:

```
usage: github-pr-commenter.py [-h] repo prnumber template logfile

positional arguments:
  repo        Organization and repository (e.g. xbmc/repo-plugins)
  prnumber    PR number (e.g. 5)
  template    Jinja 2 template file to generate a comment from
  logfile     Log file to parse (e.g. mylog.log)

optional arguments:
  -h, --help  show this help message and exit
```

## Example template

```
## Something was successfull
Hey @{{pullRequestAuthor}},
we found no major flaws with your code. Still you might want to look at this logfile, as we usually suggest some optional improvements.


<details>
  <summary>
    <strong>
     Expand log file
    </strong>
  </summary>

` ` `
{{contents}}
` ` `

```