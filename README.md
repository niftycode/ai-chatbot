# ai-chatbot

This chatbot is using the OpenAI API to fetch **Python** related answers.

The program is inspired by an article from [heise.de](https://www.heise.de/ratgeber/Python-Eigene-KI-Programmierhilfe-entwickeln-9330993.html). In contrast to the code in the article, the new API (> 1.0.0) is used here.

Information on how to use the new API can be found on Github:

[v1.0.0 Migration Guide #742](https://github.com/openai/openai-python/discussions/742)

In the [heise.de](https://www.heise.de/ratgeber/Python-Eigene-KI-Programmierhilfe-entwickeln-9330993.html) code, the API key is hard coded. In the code used here, however, it is stored in a **binary file**. By default the key is located in

    > ~/Documents/API/openai-api-file.bin

This deviates from the suggestion shown [on Github](https://github.com/openai/openai-python/discussions/742)
. Because `os.environ` is used there:

    from openai import OpenAI

    client = OpenAI(
      api_key=os.environ['OPENAI_API_KEY'],
    )

**Tip**: You can create a binary file in Python using this code:

    # initialize string
    api_key = "API_KEY"

    # open file as a binary file
    f = open('openai-api-file', 'wb')

    # convert string to bytes
    strBytes = api_key.encode()

    # write byte string to binary file
    f.write(strBytes)

    f.close()

## Operating System

* macOS
* Linux
* Windows (not tested, but should work too)

## Requirements

* Python >= 3.12
* openai >= 1.0.0
* OpenAI Api Key

## Additional Notes

This repository contains a spec file that allows you to create an executable with [PyInstaller](https://pyinstaller.org/en/stable/). The prerequisite is that the PyInstaller package was installed with `pip`:

```Bash
pip3 install pyinstaller
```

