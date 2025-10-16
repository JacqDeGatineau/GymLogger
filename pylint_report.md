# Pylint-raportti
Pylintin raportti sovelluksesta:

    ************* Module app
    app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    app.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:45:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:50:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:54:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:87:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:91:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:97:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:112:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:119:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:124:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:132:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:152:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:162:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:179:8: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
    app.py:184:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:189:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:203:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:218:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:228:0: C0116: Missing function or method docstring (missing-function-docstring)
    app.py:239:0: C0116: Missing function or method docstring (missing-function-docstring)
    ************* Module config
    config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    ************* Module db
    db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
    db.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
    db.py:11:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
    db.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
    db.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
    db.py:21:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
    ************* Module gym
    gym.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    gym.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:36:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:46:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:55:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
    gym.py:60:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:66:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:71:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:75:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:80:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:87:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:94:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:101:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:106:0: C0116: Missing function or method docstring (missing-function-docstring)
    ************* Module update_exercises
    update_exercises.py:1:0: C0114: Missing module docstring (missing-module-docstring)

    ------------------------------------------------------------------
    Your code has been rated at 8.17/10 (previous run: 8.10/10, +0.08)

Seuraavaksi perustelemme, miksi tiettyjä asioita ei ole korjattu.

## Docstring-ilmoitukset

Suurin osa ilmoituksista on seuraavanlaisia:

    gym.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    gym.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
    gym.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)

Tämä on tietoinen valinta. Docstring-kommentteja ei tietoisesti käytetä sovelluksessa.

## Enumerate range(len()) -sijasta

    app.py:179:8: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)

Tässä kyseisessä tapauksessa tekijän mielestä range(len()) -on selkeämpi, sillä näin kutsuttaessa näin montaa parametria funktiolle, enumerate -muoto olisi sekavampi

## Vaarallinen oletusarvo

    db.py:11:0: W0102: Dangerous default value [] as argument (dangerous-default-value)

Tämä varoitus tulee esim. tässä tapauksessa:

    def execute(sql, params=[]):
    with get_connection() as con:
        result = con.execute(sql, params)
        con.commit()
        g.last_insert_id = result.lastrowid
    return result

Koodi ei muuta listaoliota, joten vaaraa ei ole.

## Tarpeeton else

    gym.py:55:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)

Koodin toki voi kirjoittaa joskus tiivimmin ilman else-haaraa, mutta kehittäjän näkemyksen mukaan joissain tapauksissa se tekee koodista selkeämmän ja helposti luettavamman.