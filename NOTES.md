Scratchpad of notes and thoughts that occurred to me throughout development,
or helpful things to remember

* At present (before it's generated dynamically), the URL for
    the statically-hosted S3 file is `http://pop-culture-graph.s3-website-us-east-1.amazonaws.com`
* To create the stack, call: `aws cloudformation create-stack --stack-name test --template-body file://template.yaml --parameters ParameterKey=paramGithubOAuthToken,ParameterValue=[REDACTED] ParameterKey=paramGithubRepo,ParameterValue=popCultureGraph ParameterKey=paramGithubUser,ParameterValue=scubbo --capabilities CAPABILITY_NAMED_IAM`
* Open question [here](https://stackoverflow.com/questions/53987204/is-it-possible-recommended-to-use-sam-build-in-aws-codebuild) on
    how best to build SAM applications.
* Not necessary in this case (since the website can just call a Route 53 DNS name),
    but I'd be interested to know the best solution for if the static website needed
    to reference a Cloudformation Stack Output (presumably - "it shouldn't, just have it
    call some backend service that references the Stack Output")
* The documentation on how importing works in Python is lacking (or, I can't find it):
** `help();help(import)` gives `The details of the first step, finding and loading modules are described in greater detail in the section on the import system`.
** `help();topics` lists several topics that look potentially helpful: `IMPORTING`, `MODULES`, `PACKAGES`
*** `IMPORTING` contained the same content (at a skim - specifically, it contained the same "The details of the first step..." section) as `help(import)`
*** `MODULES` only contained information for interacting with (already-imported) modules
*** `PACKAGES` containes the same content as `help(import)` and `IMPORTING`

## TODO

* Specific unit-tests for DataFetcher, not just app-level 
* `requests-mock` tests for DataFetcher
* Make the bucket-name in buildspec.yml dynamic `{BUCKET-NAME}`, rather than hard-coded:
    like in [here](https://github.com/scubbo/scubbo-slackbot/blob/master/buildspec.yml#L13)
* Deploy static website *in* a Deploy step, rather than during build
* Framework to test locally (website calling local functions)
* Notification when pipeline fails