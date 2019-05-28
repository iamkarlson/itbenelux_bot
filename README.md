# itbenelux_bot
Functions:

* Warm welcome messages
* Support participants when they are in difficult life situations


## Notes

### Sync code from AWS to repo

```
curl (aws lambda get-function --function-name "itbenelux_bot"|ConvertFrom-Json).Code.Location -o sources.zip; 7z x -y sources.zip; rm sources.zip; g add .; g commit ;g push
```

### Publish from local code

Useful guide:
[Publishing Your Skill Code to Lambda via the Command Line Interface](https://developer.amazon.com/blogs/alexa/post/Tx1UE9W1NQ0GYII/publishing-your-skill-code-to-lambda-via-the-command-line-interface)

#### Windows batch file:
```
del index.zip 
cd lambda 
7z a -r ..\index.zip *
cd .. 
aws lambda update-function-code --function-name itbenelux_bot --zip-file fileb://index.zip
```

Find a ready to go batch file in this repo called *publish.bat*