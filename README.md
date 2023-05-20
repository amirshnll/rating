# Rating

this is a code challenge. (technical task)

## Package Used list

```
Django==4.2
djangorestframework==3.14.0
django-environ==0.10.0
django-cors-headers==3.13.0
djangorestframework-recursive==0.1.2
djangorestframework-simplejwt==5.2.0
decorator==5.1.1
gunicorn==20.1.0
```

## env variables

```
SECRET_KEY=abcdefghijklmnopqrstuvwxyz
MINIMUM_PER_PURCHASE=10
DEBUG=true
ADMIN_ENABLED=true
AUTH_PREFIX=Bearer
AUTH_HEADER_TYPES=Bearer
```

## Test

1. test all

```
python manage.py test
```

2. user authentication

```
python manage.py test user.tests.UserTestCases.test_UserAuth
```

3.  blog post

```
python manage.py test blog.tests.BlogTestCases.test_BlogPost
```

4. rate blog post

```
python manage.py test rate.tests.RateTestCases.test_Rate
```

## Run

1. build project

```
docker-compose build
```

2. start project

```
docker-compose up -d
```

3. check health

```
curl http://localhost:8000/api/v1/healthcheck/
```

## endpoint documentation (postman)

[Rate.postman_collection.json](postman/Rate.postman_collection.json)
