# European CyberWeek 2016 Quals - Cyber Aquarium
### Web - 200 pts

[Website link](https://challenge-ecw.fr/chals/web400/)

This website showed a little menu with an administration page protected by an `.htaccess/.htpasswd` system.
First thing to do, check the different pages. We find an interessant URL like this one : `https://challenge-ecw.fr/chals/web400/index.php?file=opening.php`.
We try to change the `file=opening.php` with something else and get a nice blank div in the website. All we need to do is to find a way to include admin protected files. By putting `?file=../admin/index.php` we get an error 500. We know we got the path right, but the file is not readable. We try `?file=../admin/.htpasswd` and bingo ! We get `admin:$apr1$GYisGMCV$jjVb..e11VZBX6WowcpoN0 admin:ECWPasswordWeb`

We can now connect to the admin interface with these credentials and enter the second part of the challenge.

Here the menu is pretty straightforward, there's a page called "Coffre-fort" which means a safe in French. When we click on this page, we are asked a password. No SQL injection available. The page is still given by URL and a wrong page shows nothing which means possible LFI.
The "Coffre-fort" page sends the password in a post request to the `checkFlag.php` page. Here we can't include the wanted page because it does a check on the password. We would like to retrieve the source code.
The first thing to try is the PHP filter : `php://filter/read=convert.base64-encode/resource=checkFlag.php`. It shows nothing, but if we do it on the `strongbox.php` page we get the following error : `Interdit de voir ce fichier, essaye un autre.` (Meaning : Not allowed to read this file, try another one). The first try with `checkFlag.php` must have been blocked by a WAF of something like this. Let's try to bypass it and put caps letters in the request.

We try : `https://challenge-ecw.fr/chals/web400/admin/index.php?file=Php://filter/read=convert.base64-encode/resource=checkFlag.php` and get the page source code base64 encoded.

We base64decode the string and get a piece of code.

```php
if(isset($_POST['flag']))
{
   $f=trim($_POST['flag']);
   if(strlen($f) === 11 &&
      	$f[0] === 'U' &&
      	$f[10] === 'R' &&
      	ord($f[1]) - 5 === 77 &&
      	ord($f[6]) ^ 21 === 84 &&
      	$f[2] === $f[4] &&
      	$f[2] === '_' &&
      	$f[7] === $f[8] &&
	ord($f[3]) ^ ord($f[6]) === 0 &&
	$f[5] === 'H' &&
	ord($f[8]) ^ ord($f[6]) === 25 &&
	ord($f[9]) + 7 === 55)
	{
		echo '<h1>Bravo!</h1><br />
		      <h2>Valide l\'épreuve avec le hash md5 du mot de passe !<br /> Format ECW{md5}</h2>';
	}
	else
	{
		echo '<h1>Accès refusé</h1>';
	}
}
```

We need to reverse the little algorithm to find the right password.
* Password Length : 11
* First Char : "U"
* Last Char : "R"
* 2nd Char : Decimal code 82. It is "R"
* 7th Char : Decimal Code : 84 XOR 21 => 65. It is "A"
* 3rd Char equals the fifth Char
* 3rd Char is "_"
* 8th Char is 9th Char
* 4th Char equals 7th Char (Xor equals zero)
* 6th Char is "H"
* 9th Char XOR 7th Char equals 25. 7th Char is 65, so 9th Char is "X"
* 10th Char : Decimal Value 55-7 which is "0"

This algorithm gives us the password : "UR_A_HAXX0R"

Flag is the md5 value of this.