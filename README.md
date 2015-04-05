ngxpurged: purge an nginx cache
===============================

This is a small WSGI daemon to purge the contents of a particular nginx cache 
directory.  It can be used to implement clearing of the entire cache from an 
HTTP request, e.g. during deployments when the deployment user doesn't have 
write access to the nginx cache.

Use it like this:

```
    location /__purgeall {
        if ($request_method != POST) {
            return 405;  # Method not implemented.
        }

        rewrite ^.* /purge/wagtail.io;

        include uwsgi_params;
        uwsgi_pass unix:/run/ngxpurged.sock;

        break;
    }
```

Then to purge the cache:

```
[by-web-3:wagtailsite] ~
{117} wagtailsite> curl -X POST https://wagtail.io/__purgeall
Purged <wagtail.io>, 5 deleted, 0 errors.
```

All the daemon actually does is delete all the files under a particular 
directory, so it could potentially be used to purge any sort of disk-based 
cache, or for other purposes.  You may want to run it under AppArmor or a 
similar MAC system to ensure it doesn't accidentally delete anything it 
shouldn't.

Questions, comments: <ft@le-fay.org>.
