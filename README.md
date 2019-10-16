# Prerequisites

SAM (install from [here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html))

# How to set up PyCharm

1. `git pull`
2. Open in PyCharm
3. Open Preferences, go to `Project:<project name> -> Project interpreter`, click the gear, and "Add"
4. Add a Virtualenv environment, click "Apply" and "OK"
5. In Preferences, go to `Tools -> Python Integrated Tools`, and set the Package Requirements File
6. When prompted (you may need to open a code file), "Install Requirements"

# How to develop

## Main loop

* Make code changes
* Update with `./liveUpdate.sh`
  * If you have changed dependencies, you'll instead need to rebuild with `sam build -u` (`-u` helps because it gets around Python version mismatches. Or you can mangle your PATH - your choice)
* Run locally with `./startLocally.sh`
* TODO - figure out attaching a debugger. I suspect I need the following snippet:

```
import ptvsd

# Enable ptvsd on 0.0.0.0 address and on port 5890 that we'll connect later with our IDE
ptvsd.enable_attach(address=('0.0.0.0', 5890), redirect_output=True)
ptvsd.wait_for_attach()
```

# How to test

`pytest .`
