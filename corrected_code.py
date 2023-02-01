import datetime
import traceback
import json
from sqlite3 import connect

import requests

time_now='"'+str(datetime.datetime.now())[:19]+'"'
print(time_now)
for target in [-2, -3]:
    try:
        ok = True
        line = str(target)
        response = requests.get(f"https://dummy.server/products/example?id={line}")
        response_content = response.content
        # changed to append mode, file operation changed to 'with'
        with open("tmp.txt", "wb") as file:
            file.write(response_content)

        print("data downloaded from server " + str(len(response_content)))
        with open("tmp.txt", "rb") as file:
            product = json.loads(file)
    except BaseException:
        print("issue with server/data format")
        ok=False

    else:

        if product["type"] != "bundle":
            try:
                print("product loaded")
                sql = connect("database.sqlite")
                for x in product["details"]["supply"]:
                    for y in x["stock_data"]:
                        if y["stock_id"] == 1: productSupply = y["quantity"]

                    cursor = sql.cursor()
                    # simplified load do sqllite db
                    sql_code="INSERT INTO product_stocks (time, product_id, variant_id, stock_id, supply) VALUES (?,?,?,?,?)"
                    values = (time_now, str(product["id"]), str(x["variant_id"]), str(1), str(productSupply))
                    cursor.execute(sql_code,values)
                    sql.commit()
            except BaseException:
                print("issue with product load")
                ok=False

        if product["type"] == "bundle":
            try:
                print("bundle loaded")
                products = []
                for p in product["bundle_items"]:
                    products.append(p["id"])
                print("products " + str(len(products)))
                id = product["id"]
                all = []
                open('tmp2.txt', 'w').close()
                for p in products:
                    r = requests.get(f"https://dummy.server/products/example?id={str(p)}")
                    respContent = r.content
                    # second temp file (content removed before) used for this part not to interfere with the first file
                    with open("tmp2.txt", "ab") as file2:
                        file2.write(respContent)

                    with open("tmp2.txt", "r") as file2:
                        product = json.loads(file2)

                    supply = 0
                    for s in product["details"]["supply"]:
                        print(s)
                        for stoc in s["stock_data"]:
                            if int(stoc["stock_id"]) == 1:
                                supply += int(stoc["quantity"])
                    all.append(supply)
                productSupply = min(all)
                baza_d = connect("database.sqlite")
                cursor = baza_d.cursor()

                sql_code = "INSERT INTO product_stocks (time, product_id, variant_id, stock_id, supply) VALUES (?,?,?,?,?)"
                values = (time_now, str(id), "NULL", str(1), str(productSupply))
                cursor.execute(sql_code, values)
                baza_d.commit()
            except BaseException:
                print('Issue with Bundle load'),
                ok=False

    finally:
        if ok:
            print("ok")
        else:
            print("error")
            print(traceback.format_exc())

