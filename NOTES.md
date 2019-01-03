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
* I'm really lacking a neat way of referencing a common root (such that a test runs with the same relative working dir
    whether run from PyCharm or from `pytest .`). A variable like `package-root` would be useful (probably exists, I just
    haven't looked it up yet)

## TODO

* Specific unit-tests for DataFetcher, not just app-level 
* `requests-mock` tests for DataFetcher
* Make the bucket-name in buildspec.yml dynamic `{BUCKET-NAME}`, rather than hard-coded:
    like in [here](https://github.com/scubbo/scubbo-slackbot/blob/master/buildspec.yml#L13)
* Deploy static website *in* a Deploy step, rather than during build
* Framework to test locally (website calling local functions)
* Notification when pipeline fails
* Rewrite from line 313-onwards of main.js, which handles responses from clicking nodes in spread mode. Update to match
    the current data-format (and/or update the data-format to be more helpful - might be nice to make the responses
    statelessly-consumable, without requiring the client to track that!)
* Do not duplicate existing linked-nodes (probably requires passing a list of "nodes to suppress" into the functions)
* franchises_for_actor for Alison Brie (1555340) is returning empty
    ditto Zoe Saldana
* Many incorrect character-name parsings (e.g. `)` as a character name of Charlie Day)
    Also Will Arnett has two "Riviera" entries
* Clicking a node N_1 that's already connected to a node N_2 will reset the chunkNum of N_2
* When pruning, also remove all leaves
* Clicking spread one one node, then on another one quickly afterwards (before completion) leads to the resulting three
    nodes being "linked" to nothing