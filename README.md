# extractor
Deep feature extractor demo.

# minimum usage
```
$ docker build -t extractor .
$ docker run --rm -it -p 8080:5000 extractor
```

And then, access http://127.0.0.1:8080/

NOTE: docker build takes about 10 minutes for downloading weights.
