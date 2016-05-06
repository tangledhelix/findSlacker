A script to find users matching a substring on your Slack site. Easy to plug
into a script that looks for access to shut off when someone leaves the
organization.

```
cp config.json.sample config.json
```

Update `api_token` to contain an API token valid for your Slack site.

Then, to find people matching "john",

```
./findSlacker.py john
```

The username, full name, and email fields are searched.
