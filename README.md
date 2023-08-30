<div align="center">

# Personal AI Assistant
_AI Assistant bot with Bing AI ( using [EdgeGPT](https://github.com/acheong08/EdgeGPT) API )_


</div>

# Features
- [x] Multi Language Support 
- [x] Image Download ( Gif & JPG)
- [x] Voice Recognition Enables 
- [x] Can allow every one to use
- [x] Allow you set your own cookie at runtime
- [x] Allow you set a bot name to you
- [X] Export conversation to Text File 
- [x] Hot update the EdgeGPT dependence
- [ ] Image Generation Using EdgeGPt

# Setup
## Requirements
* python 3.8+
* A Microsoft Account with early access to [http://bing.com/chat](http://bing.com/chat)
* Good practical skills and a clear mind!

<details>
  <summary>

### Checking bing AI access (Required)
PS: Everyone can access Bing AI for chat now, even anonymous users.

  </summary>
</details>


<details>
  <summary>

### Getting authentication (Mandatory)

  </summary>

- Install the cookie editor extension for [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/) or [Edge](https://microsoftedge.microsoft.com/addons/detail/cookieeditor/neaplmfkghagebokkhpjpoebhdledlfi)
- Go to [`bing.com`](https://bing.com/) & SignIN Or SignUp ( Mandatory )
- Open the extension
- Click "Export" on the bottom right, then "Export as JSON" (This saves your cookies to clipboard)
- Paste your cookies into a file `cookie.json`

</details>

## Install requirements
```shell
pip install -r requirements.txt
```

## Set environment variables ( OPTIONAL)

Then edit `config.py` file and set `bot_name`, `master`, `VoiceType` etc..(Check Configuration File for more )

# Run
```shell
python main.py
```



That's ALL Your Personal AI Assistant is ready to use !!!
