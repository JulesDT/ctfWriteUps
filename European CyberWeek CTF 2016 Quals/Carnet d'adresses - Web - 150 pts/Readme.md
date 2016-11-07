# European CyberWeek 2016 Quals - Carnet d'adresses
### Web - 150 pts

Very obvious XEE here. But sadly, we have to guess the flag file to read it. Reading the source code of the index page gives us no informations about where is the flag. No config.php file.

In the end all we have to do is :

```xml
<!DOCTYPE foo [
<!ENTITY xxe SYSTEM "flag.txt" >
]>
```

and then add `&xxe;` in a visible field of the example XML given, and the flag will appear.