# How to create translations

## Extract strings
```bash
pybabel extract -F babel.cfg -o messages.pot .
```

## Create translations files
```bash
pybabel init -i messages.pot -d translations -l ru
pybabel init -i messages.pot -d translations -l en
...
```

### Update translations files
```bash
pybabel update -i messages.pot -d translations
```

## Edit translations files
```bash
nano translations/en/LC_MESSAGES/messages.po
nano translations/ru/LC_MESSAGES/messages.po
```

## Compile translations files
```bash
pybabel compile -d translations
```

## Done!