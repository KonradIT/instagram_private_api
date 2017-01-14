# FAQ

## 1. What does error code XXX mean?

- **400**: Bad request. Please check the parameters specified.
- **403**: The method requires authentication (web client) or the request has been denied by IG.
- **404**: The entity requested is not found (web client) or the endpoint does not exists.
- **429**: Too many requests. You're making too many calls.

IG may also return other 4XX or 5XX codes.
 
## 2. "Your version of Instagram is out of date. Please upgrade your app to log in to Instagram."

Instagram is rejecting the app version that the lib is using. 

If discarding the cached auth and relogging in does not work, you may need to (1) update the lib, or (2) extract the latest signature key and version from the latest Instagram APK or from https://github.com/mgp25/Instagram-API/blob/master/src/Constants.php.

With the new sig key and app version, you can modify the client like so

```python
new_app_version = '10.3.2'
new_sig_key = '5ad7d6f013666cc93c88fc8af940348bd067b68f0dce3c85122a923f4f74b251'
new_key_ver = '4'           # does not freq change
new_ig_capa = '3ToAAA=='    # does not freq change

api = Client(
    user_name, password,
    app_version=new_app_version,
    signature_key=new_sig_key,
    key_version= new_key_ver,
    ig_capabilities=new_ig_capa)
```    