# service-image

## Colorization Model
[Richard Zhang](https://github.com/richzhang/colorization)

![](http://richzhang.github.io/colorization/resources/images/teaser3.jpg)

## Frontend
Vue.js + Bootstrap

[ReadMe](frontend/README.md)

##Backend

flask

## Docker image

```shell
docker build -t service-item:latest .
docker run -d -p 8080:8080 service-item:latest
```