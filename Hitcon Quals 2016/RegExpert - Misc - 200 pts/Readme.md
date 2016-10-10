# Hitcon Quals 2016 - RegExpert
### Misc - 200 pts

    Do you remember "hard to say" last year?
    I think this one is harder to say...
    
"Simple" channel in appearance, we need to give a regex to match a fixed pattern. We have 5 regex to find.
The three main things to take care of are :
- Ruby language is used. Therefore Regex are sometimes different in their syntax
- We don't have access to options, so no "insensitive" option possible
- Asked Regex are not usual

### 1st Regex :
```
================= [SQL] =================
Please match string that contains "select" as a case insensitive subsequence.
```

Here we need to find every subsequence. Meaning SXeLEcT should match.

First try :
`[sS].*[eE].*[lL].*[eE].*[cC].*[tT]` should be ok. And yes it works until the last test :
`Almost there...But the length limit is 21`...
So here the workaround is a `(?i)` for the insensitive case.

And the solution is `(?i)s.*e.*l.*e.*c.*t`

### 2nd Regex :
```
=============== [a^nb^n] ================
Yes, we know it is a classical example of context free grammer.
````
The "Contenxt free grammer" helps us in our research. Here the goal is to create a pattern aXb where X is the same pattern in recursion and optionnal. This is possible in Ruby with the syntax `\g<1>?` which creates recursion on the 1 capturing group.
So we try the regex `^(a\g<1>?b)$` and it works !

2nd Solution : `^(a\g<1>?b)$`

### 3rd Regex :

```
================= [x^p] =================
A prime is a natural number greater than 1 that has no positive divisors other than 1 and itself.
```
Here I don't have much to say.
To force all elements to be x and avoir empty regex we put `^xx+$` at the end.
`(xx+)\1+` matches non-prime length strings. So we invert it and get the 3rd solution

3rd Solution : `(?!(xx+)\1+$)^xx+$`

### 4th Regex :

```
============= [Palindrome] ==============
Both "QQ" and "TAT" are palindromes, but "PPAP" is not.
```

Here we need to first match a single character, or create a recursive pattern matching the pattern `aXa` where `a` is a random character and `X` the recursion being on the whole pattern. (Because we need the recursion to have a stopping condition which here will be the single character)

So first we match a single character with this `^(\w)$`
Then we add to **OR** pattern with the recursion and it works !

4th Solution : `^(\w?|(\w)\g<1>\k<2>)$`

### 5th Regex :

```
============== [a^nb^nc^n] ==============
Is CFG too easy for you? How about some context SENSITIVE grammer?
```

Here `context SENSITIVE grammer` helps us to find informations on Google.

We first found this Regex : `/\A(?<AB>a\g<AB>b|){0}(?=\g<AB>c)a*(?<BC>b\g<BC>c|){1}\Z/` which we reduced to `^(a\g<1>b|)(?=\g<1>c)a*(b\g<2>c|)$`

This regex works but the length limit is 29. After testings, we didn't find a way to reduce this regex. So we searched for another method. We found the regex `^(?=(a(?-1)?b)c)a+(b(?-1)?c)$` and after a little adaptation to Ruby Language we have the solution

5th Solution : `^(?=(a\g<1>?b)c)a+(b\g<2>?c)$`

**Here we are !**
With all this, we get the well diserved flag : `hitcon{The pumping lemma is a lie, just like the cake}`
