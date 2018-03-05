# SA-rsearch
Sample custom search commands for Splunk to allow limited and controlled access to restricted indexes and lookups.

## Warnings
The code in this app provides a mechanism for bypassing access controls in Splunk. 

* If you are inexperienced with Splunk or if you cannot understand exactly what every line of the included code is doing, you should not install this app. 
* You should carefully analyze this code and perform a risk assessment before installing this app on a production system. 

**Beware that this app stores Splunk usernames and passwords in plain text in a configuration file in the filesystem of the Splunk search head.** This is generally considered a bad practice. If this violates your policies, standards, or compliance mandates, you should not install this app.


*No guarantees are made about the efficacy of this app. Use at your own risk.*


## Installation
```
$ cd $SPLUNK_HOME/etc/apps
$ git clone https://github.com/daveherrald/SA-rsearch.git
$ $SPLUNK_HOME/bin/splunk restart
```

## Configuration
Edit $SPLUNK_HOME/etc/aps/SA-rsearch/rsearch.config to configure a strong password.
```
[rsearch]
USER = privileged_splunk_user
PASS = <put a strong password here, and ditch the angle brackets>
HOST = 127.0.0.1
PORT = 8089
```

## Use
