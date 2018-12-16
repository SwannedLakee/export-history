# export-history

A simple script that exports my internet history as a webpage. 

The bash script brings the databases into the working directory. This is so that:

* We don't have to close browsers when it runs 
* We definitely aren't messing with the browser databases directly

There is a [blog post](http://joereddington.com/6530/2018/12/12/experimenting-with-public-internet-history./) that talks about the reasons behind this, and there is also a [live example](http://joereddington.com/history.html)

Currently all urls are stripped down to their domain name unless they appear on 'whitelist.txt' 

TODO 
* Allow wildcards in whitelist 
* Add export of a text file of all whitelisted searches (to check everything is fit for publication
