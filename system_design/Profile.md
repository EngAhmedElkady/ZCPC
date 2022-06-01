# Profile
## summary

### profile has the following
- username (required)
- name   (not required (flag)
- email  (required)
- image 
- bio
- codeforces (required)
- university (required)
- github     
- telegram   (required)
- linkedin


# usage
## register
### link: http://0.0.0.0:8000/account/register/
### post:
~~~
{
    "username": "ahmed",
    "email": "ahmedelkady@gmail.com",
    "codeforces": "ahmed_elkady",
    "telegram": "https://t.me/elkady_ps",
    "password":"ahmed_elkady123"
}
~~~
### return 
~~~
{
    "user": {
        "id": 8,
        "username": "ahmed",
        "name": null,
        "email": "ahmedelkady@gmail.com",
        "bio": null,
        "university": null,
        "image": null,
        "codeforces": "ahmed_elkady",
        "linkedin": null,
        "github": null,
        "telegram": "https://t.me/elkady_ps"
    },
    "token": "b07f035692c86f84babc21abf48e00c832ef4b7f399d917bbfd3c16d7c10da1f"
}
~~~
## login
### link: http://0.0.0.0:8000/account/login/
### post:
~~~
{
    "email": "ahmedelkady@gmail.com",
    "password":"ahmed_elkady123"
}
~~~
return
~~~
{
    "user": {
        "id": 8,
        "username": "ahmed",
        "name": null,
        "email": "ahmedelkady@gmail.com",
        "bio": null,
        "university": null,
        "image": null,
        "codeforces": "ahmed_elkady",
        "linkedin": null,
        "github": null,
        "telegram": "https://t.me/elkady_ps"
    },
    "token": "d9e4816a8354bd63cb6b9b5dda3d89fbfe28d96cab2da7f99468c399ab4dbba7"
}
~~~
## logout
### link: http://0.0.0.0:8000/account/logout/
### Post: take a token only
~~~
Token d9e4816a8354bd63cb6b9b5dda3d89fbfe28d96cab2da7f99468c399ab4dbba7
~~~

## reset password
### link: http://0.0.0.0:8000/account/password_reset/
### Post:
~~~
{
    "email": "ahmedelkady@gmail.com"
}
~~~
return 
~~~
May 22, 2022 - 08:35:05
Django version 3.2.12, using settings 'config.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Password Reset for Some website title
From: noreply@somehost.local
To: ahmedelkady@gmail.com
Date: Sun, 22 May 2022 08:35:25 -0000
Message-ID: <165320852566.7.7158934524215821422@a59817410e51>
/account/password_reset/?token=524f22be3df010485926994cfb8c58
-------------------------------------------------------------------------------
web_1  | [22/May/2022 08:35:25] "POST /account/password_reset/ HTTP/1.1" 200 15
~~~

## password confirm
### linke: http://0.0.0.0:8000/account/password_reset/confirm/
### Post
~~~
{
    "token":"524f22be3df010485926994cfb8c58",
    "password":"ahmed_new_password"
}
~~~
return 
~~~
{
    "status": "OK"
}
~~~

## change password
### link: http://0.0.0.0:8000/account/change-password/
### put
~~~

~~~