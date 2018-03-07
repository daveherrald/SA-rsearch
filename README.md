# SA-rsearch
Sample custom search commands for Splunk to allow limited and controlled access to restricted indexes and lookups.

## Warnings
The code in this app provides a mechanism for bypassing access controls in Splunk. 

* If you are inexperienced with Splunk or if you cannot understand exactly what every line of the included code is doing, you should not install this app. 
* You should carefully analyze this code and perform a risk assessment before installing this app on a production system. 

This app uses the [Python keyring module](https://pypi.python.org/pypi/keyring) with a [file based encrypted keyring](https://github.com/jaraco/keyrings.alt/blob/master/keyrings/alt/file.py#L71) backend to store privileged Splunk credentials. **Beware, the app requires you to store the encrypted keyring password in a plain text file. Use file level access controls to secure the file.** If this violates your policies, standards, or compliance mandates, you should not install this app.

*No guarantees are made about the efficacy of this app. Use at your own risk.*


## Installation
```
$ cd $SPLUNK_HOME/etc/apps
$ git clone https://github.com/daveherrald/SA-rsearch.git
$ $SPLUNK_HOME/bin/splunk restart
```


## Configuration
### Create/Update/Delete Splunk Privileged Accounts

```
# cd $SPLUNK_HOME/etc/apps/SA-rsearch/bin
```

Use the `keyring-cli` command to seed and manage the password store.

```
# $SPLUNK_HOME/bin/splunk cmd python keyring-cli

Usage: keyring-cli [get|set|del] SERVICE USERNAME

Options:
  -h, --help            show this help message and exit
  -p KEYRING_PATH, --keyring-path=KEYRING_PATH
                        Path to the keyring backend
  -b KEYRING_BACKEND, --keyring-backend=KEYRING_BACKEND
                        Name of the keyring backend
  --list-backends       List keyring backends and exit

```

To store the Splunk user `shaskell` in the `prod` service run the following command. If this is the first time you're adding a user, you will be prompted input a password to secure the keyring. **Don't lose this password or you will need to delete and re-create the keyring. You will need to use this password in the next section**

```
# $SPLUNK_HOME/bin/splunk cmd python keyring-cli set prod shaskell

Password for 'shaskell' in 'prod': 
Please set a password for your new keyring: 
Please confirm the password: 
```

Use the **set** command on an existing **SERVICE** and **USERNAME** combo to update the password.

### Store Keyring Password
You must store the keyring password in `$SPLUNK_HOME/etc/apps/SA-rsearch/bin/python_keyring/.secret` for the custom search commands to access encrypted passwords in the keyring.

Replace `mykeyringpassword` with the password you set for the keyring in the previous step. Make sure it's wrapped in single quotes. Be sure to lock the file down to the user running splunkd (typically root) and set to mode 600.

```
# echo 'mykeyringpassword' > $SPLUNK_HOME/etc/apps/SA-rsearch/bin/python_keyring/.secret
# chmod 600 $SPLUNK_HOME/etc/apps/SA-rsearch/bin/python_keyring/.secret
```

### rsearch config file
Edit $SPLUNK_HOME/etc/apps/SA-rsearch/bin/rsearch.config and modify to suit your environment. Set the full path to your Splunk install for the `XDG_*` keys.

```
[rsearch]
USER = shaskell
SERVICE = prod
HOST = 127.0.0.1
PORT = 8089
XDG_CONFIG_HOME = /opt/splunk/etc/apps/SA-rsearch/bin
XDG_DATA_HOME = /opt/splunk/etc/apps/SA-rsearch/bin/
XDG_SECRET_HOME = /opt/splunk/etc/apps/SA-rsearch/bin
```

Log into Splunk and create the Splunk user. Make sure the username and password match what is specified in the config file above. The user should be granted only the privileged_reader role. 

NOTE: the privileged_reader role is defined by this app when it is installed.

### Keyring File Reference
**Encrypted Keyring** - `$SPLUNK_HOME/etc/apps/SA-rsearch/bin/python_keyring/crypted_pass.cfg`

**Keyring Defaults** - `$SPLUNK_HOME/etc/apps/SA-rsearch/bin/python_keyring/keyringrc.cfg`

**Keyring Secret** - `$SPLUNK_HOME/etc/apps/SA-rsearch/bin/python_keyring/.secret`

## Try it out
For these sceanrios, create a simple Splunk user called 'luser' with the role of 'user'. This user will mimic a non-privileged user who you want to be able to access a restricted resource. NOTE: This is a different user than the one specified above.

### Scenario 1 - Read a restricted lookup table
In this scenario, we will allow the unprivileged user access to **only certain rows** of a restricted lookup table called employeedata.csv (included with this app). 

employeedata.csv contains the following sensitive records:

```
user,salary,employee_rating
mallory,100000,4
bob,75000,3
alice,200000,5
luser,20000,2
```

Log in as the unprivileged user(luser) and attempt to read the lookup. Splunk will report 'No results found...' as expected.

![](https://github.com/daveherrald/SA-rsearch/raw/master/images/failed-inputlookup.png "Logo Title Text 1")

Now, as the same unprivileged user(luser), run the custom search command called rinputlookup, and observe the restricted results.

![](https://github.com/daveherrald/SA-rsearch/raw/master/images/rinputlookup.png "Logo Title Text 1")

## Customize

Edit the search in the file $SPLUNK_HOME/etc/apps/SA-rsearch/bin/rinputlookup.py. The search appears as follows:

```
    user = self._metadata.searchinfo.username
    searchquery = """
    | inputlookup employeeinfo.csv | search user={}
    """.format(user)
```

## Yep it's kludgey!
We know! Again, use at your own risk.
