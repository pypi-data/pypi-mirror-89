# NoSpam+

An Python Wrapper For NoSpamPlus Api.

# Support

* Channel : @NospamPlus
* Group : @NospamPlusSupport
* Bot : @NospamPlusBot
* Website : nospamplus.tk

# Usage Example

```python
from nospamplus.connect import Connect
mytoken = 'your_token_from_@antispamincbot'
token_connect = Connect(mytoken)
user = token_connect.is_banned(12974624)
print(user.ban_code)
print(user.reason) 
```

# Installing
```shell script
pip install nospamplus
```
or 
```shell script
pip3 install nospamplus
```
