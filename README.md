# ansible_human_log.py
Ansible Human Log

This makes the ansible errors be shown in a way humans can understand, with idented jsons and multi line strings converted to something nice.

After a lot of research, tweaking and merging, this is the ansible human_log I always dreamed of.

I hope I did not forget to add anybody's name in the credits.

Marcos Diez [ marcos AT unitron DOT com DOT br ]

usage:

- create a file called ansible.cfg with at least the following content:

```
[defaults]
callback_plugins = callback
```

- create the folder 'callback'
- copy the file human_log.py to this callback folder
- enjoy


https://github.com/marcosdiez