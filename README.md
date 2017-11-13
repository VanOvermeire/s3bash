A small experiment. If you add the s3bash.sh file as 's3bash' to, for example, /usr/local/bin,
you can call s3 (almost) as if it was a local system. And do stuff like this:

s3bsh ls | grep some-test | s3bsh rmb

Which will remove any buckets that contains 'some-test'. Which is pretty cool.
