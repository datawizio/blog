# blog
Datawiz Python courses

## Підготовка
Для економії часу щоб не налаштовувати оточення можна використати [docker](https://docs.docker.com/desktop/install/mac-install/):
0. Відрийте термінал і перейдіть у папку із проектом (`cd /path/to/blog`);
1. Збілдити image:
```
docker build -t blog:0.0.1 .
```
2. Запустити container:
```
docker run -it --rm \
  --name blog \
  -v "$(pwd)/static:/home/dw/blog/static" \
  -v "$(pwd)/templates:/home/dw/blog/templates" \
  -p "8001:8001" \
  blog:0.0.1
```
якщо порт 8001 зайнятий то його можна замінити на ішний:
```
docker run -it --rm \
  --name blog \
  -v "$(pwd)/static:/home/dw/blog/static" \
  -v "$(pwd)/templates:/home/dw/blog/templates" \
  -p "YOUR_PORT:8001" \
  blog:0.0.1
```
де `YOUR_PORT` будь-який вільний порт.