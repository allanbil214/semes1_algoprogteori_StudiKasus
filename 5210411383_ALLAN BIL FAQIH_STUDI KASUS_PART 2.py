import datetime as dt
import sqlite3 as db
import pandas as pd
# import re

conn = db.connect("dbpos.db")
cur = conn.cursor()

def main():
    def squek(): # ini digunakan untuk menambahkan table dan memasukkan beberapa placeholder data ke table
        def createTable():
            cur.execute("""CREATE TABLE IF NOT EXISTS "item" (
                        	"itemID"	INTEGER,
                        	"name"	TEXT NOT NULL,
                        	"price"	INTEGER NOT NULL,
                        	"stock"	INTEGER NOT NULL,
                        	"desc"	TEXT NOT NULL,
                        	PRIMARY KEY("itemID" AUTOINCREMENT)
                        );""")
               
            cur.execute("""CREATE TABLE IF NOT EXISTS "order_header" (
                        	"headerID"	INTEGER,
                        	"order_datetime"	TEXT NOT NULL,
                        	PRIMARY KEY("headerID" AUTOINCREMENT)
                        )""")
             
            cur.execute("""CREATE TABLE IF NOT EXISTS "order_detail" (
                        	"detailID"	INTEGER,
                        	"headerID"	INTEGER NOT NULL,
                        	"itemID"	INTEGER NOT NULL,
                        	"order_price"	INTEGER NOT NULL,
                        	"qty"	INTEGER NOT NULL,
                        	PRIMARY KEY("detailID" AUTOINCREMENT),
                        	FOREIGN KEY("headerID") REFERENCES [order_header] (headerID),
                        	FOREIGN KEY("itemID") REFERENCES [item] (itemID)
                        );""")

            cur.execute("""CREATE TABLE IF NOT EXISTS "payment" (
                        	"payID"	INTEGER,
                        	"headerID"	INTEGER NOT NULL,
                        	"totalCost"	INTEGER NOT NULL,
                        	"totalPaid"	INTEGER NOT NULL,
                        	PRIMARY KEY("payID" AUTOINCREMENT),
                            FOREIGN KEY("headerID") REFERENCES [order_header] (headerID)
                        );""")
            datacount()

        def datacount():
            cur.execute("select count(*) as count from item")
            for r1 in cur.fetchall():
                count1 = r1[0]    
                # print(count1)
            cur.execute("select count(*) as count from order_header")
            for r2 in cur.fetchall():
                count2 = r2[0]   
                # print(count1)
            cur.execute("select count(*) as count from order_detail")
            for r3 in cur.fetchall():
                count3 = r3[0]   
                # print(count1)
            cur.execute("select count(*) as count from payment")
            for r4 in cur.fetchall():
                count4 = r4[0]           
                # print(count1)
            if(count1 == 0 and count2 == 0 and count3 == 0 and count4 == 0):
                exampleData()
            
        def exampleData():
            cur.execute("""insert into item (name, price, stock, desc)
                            values('barang A', '12000', '50', 'barang ini adalah barang A'),
                            ('barang B', '15000', '50', 'barang ini adalah barang B'),
                            ('barang C', '9000', '50', 'barang ini adalah barang C'),
                            ('barang D', '22000', '50', 'barang ini adalah barang D'),
                            ('barang E', '5000', '50', 'barang ini adalah barang E')
                        """)
                        
            cur.execute("""insert into order_header (order_datetime)
                            values('2021-12-28 06:23:43.145283'),
                            ('2021-12-28 06:23:43.145283'),
                            ('2021-12-28 06:23:43.145283'),
                            ('2021-12-28 06:23:43.145283'),
                            ('2021-12-28 06:23:43.145283')
                        """)

            cur.execute("""insert into order_detail(headerID, itemID, order_price, qty)
                            values('1', '1', '12000', '3'),
                            ('1', '5', '5000', '4')
                        """)

            cur.execute("""insert into order_detail(headerID, itemID, order_price, qty)
                            values('2', '1', '12000', '4'),
                            ('2', '2', '15000', '2')
                        """)
                        
            cur.execute("""insert into order_detail(headerID, itemID, order_price, qty)
                            values('3', '1', '12000', '2'),
                            ('3', '2', '15000', '1'),
                            ('3', '5', '5000', '15')
                        """)
            
            cur.execute("""insert into order_detail(headerID, itemID, order_price, qty)
                            values('4', '1', '12000', '5')
                        """)
                        
            cur.execute("""insert into order_detail(headerID, itemID, order_price, qty)
                            values('5', '1', '12000', '3'),
                            ('5', '3', '9000', '5'),
                            ('5', '4', '22000', '2')
                        """)
                               
            cur.execute("""insert into payment(headerID, totalCost, totalPaid)
                            values('1', '56000', '60000'),
                            ('2', '78000', '80000'),
                            ('3', '114000', '120000'),
                            ('4', '60000', '60000'),
                            ('5', '125000', '150000')
                        """)
            conn.commit()

        createTable()
        
    def mainFunc():
        print('=============================================================================')
        print('[i] Order Item')
        print('=============================================================================')

        def formOrder():
            tempBarang = {} #{"nama": nama, "qty": qty, "price": price, "stock": stock, "id": id}
                           
            def showItem(z): #mendisplay item menggunakan panda
                print("\n[i] Daftar Barang\n")
                df = pd.read_sql_query("""select itemID as 'Id',
                                        name as 'Nama Barang', 
                                        price as 'Harga', 
                                        stock as 'Stok', 
                                        desc as 'Deskripsi' from item""", conn)
                print(df.to_string(index=False))
                # print(df)   
                ordering(z)
                
            def ordering(boole):     
                booly = False
                price = 0
                stock = 0
                iid = 0
                inpItem = input("[=] Ketikkan nama atau nomor barang : ")
                if(boole == True): #addition atau subtraction
                    inpQty = input("[=] Ketikkan kuantitas barang : ")
                else:
                    inpQty = input("[=] Kurangi kuantitas barang : ")
                
                #simple check inputan
                if(inpItem == "" or inpQty == ""):
                    return loop_daloop()
                elif(inpItem.isdigit()):
                    cur.execute("select * from item where itemID=?", (inpItem,))
                    row = cur.fetchone()
                    # print(row)
                    # print("nganu0")
                    if row == None:
                        # print("nganu1")
                        print("\n[i] Tidak ada barang yang bernomor " + inpItem)
                        return loop_daloop()
                    else:
                        # print("nganu2")
                        iid = row[0]
                        inpItem = row[1]
                        price = row[2]
                        stock = row[3]
                else:
                    cur.execute("select * from item where name like ?", (inpItem,))
                    row = cur.fetchone()
                    # print("nganu3")
                    if row == None:
                        print("\n[i] Tidak ada barang yang bernama " + inpItem)
                        return loop_daloop()
                    else:
                        iid = row[0]
                        inpItem = row[1]
                        price = row[2]
                        stock = row[3]
                                
                #lalu jika sama maka item yg ada di dict akan ditambahkan qty-nya saja
                #kalo tidak sama maka dict-nya ditambah item
                if(bool(tempBarang) == False): #ngecek apakah dict-nya kosong atau tidak
                    idx = 0
                    tempBarang[idx] = {"nama": inpItem , "qty": int(inpQty), 
                                       "price": price, "stock": stock, "id": iid}

                else: #jika tidak kosong baru dicek apakah ada item yg sama atau tidak
                    for r in range(len(tempBarang)): #ngecek apakah ada item yg sama
                        tmp = tempBarang[r]
                        if(tmp["nama"] == inpItem):
                            item = r
                            booly = True
                    idx = len(tempBarang)
                    if(booly == True): #cek apakah akan disubtract or add
                        getQty = tempBarang[item]
                        if(boole == True):
                            tempBarang[item].update({"qty": int(inpQty) + getQty["qty"]})
                        else:
                            tempBarang[item].update({"qty": getQty["qty"] - int(inpQty)})
                            if(getQty["qty"] <= 0):
                                del tempBarang[item]
                    else:
                        if(boole == True):
                            tempBarang[idx] = {"nama": inpItem , "qty": int(inpQty), 
                                               "price": price, "stock": stock, "id": iid}
                        else:
                            print("\n[!] Inputan ada yang salah!")
                            return loop_daloop()

                loop_daloop()
     
            def loop_daloop(): #loop pengen nambah item atau masuk ke payment
                print("\n[i] Tekan [Enter] untuk memasukkan barang kembali")
                print("[i] Ketik [1] lalu [Enter] untuk mengurangi quantity")
                print("[i] Ketik [2] lalu [Enter] untuk masuk ke menu pembayaran")
                usure = input("[=] Pilih : ")

                if(usure == "2"):
                    if(len(tempBarang) > 0):
                        payment()
                    else:
                        return loop_daloop()
                elif(usure == ""):
                    showTemp()
                    showItem(True)
                elif(usure == "1"):
                    showTemp()
                    showItem(False)
                else:
                    print("[i] Salah input!")
                    return loop_daloop()

            def showTemp(): #display dict barang yg ingin dibeli
                showTemp.thotty = 0 #total cost
                print('\n=============================================================================')
                print("[i] Barang yang telah dimasukkan adalah :")
                print('=============================================================================\n')
                print("DAFTAR BELANJA")
                print("======================================================")
                print("Nama Barang\t | \t \t", "QTY", " | Harga\t", "|  Jumlah Harga")
                print("======================================================")
                for i in tempBarang:
                    vGet = tempBarang[i]
                    amount = vGet["price"] * vGet["qty"]   
                    print(vGet["nama"], "\t\t\t  ", 
                          vGet["qty"], "  ",
                          vGet["price"],"\t\t",
                          amount)
                    showTemp.thotty += amount
                print("======================================================")
                print("Total \t\t\t\t\t\t\t\t\tRp.",showTemp.thotty)
                print("======================================================")
       
            def insertOrder(): #create data ke dalam order_header dan order_detailnya   
                todayDate = str(dt.datetime.now())
                cur.execute("insert into order_header(order_datetime) values(?)", (todayDate,))    
                conn.commit()
                cur.execute("SELECT MAX(headerID) as 'new' from Order_Header")
                for hid in cur.fetchone():
                    for tempe in range(len(tempBarang)):
                        tahu = tempBarang[tempe]
                        cur.execute("""insert into order_detail(headerID, itemID, order_price, qty) 
                                    values(?, ?, ?, ?)""", (hid, tahu["id"], tahu["price"], tahu["qty"]),)
                        conn.commit()
                        stockMin = tahu["stock"] - tahu["qty"] #update stock di table item
                        cur.execute("update item set stock=? where itemID=?", (stockMin, tahu["id"]),)
                        conn.commit()
                        # print("[i] Data berhasil masuk.")        
            
            def insertPay(): #insert payment ke db dan menampilakn receipt
                inpPay = input("[=] Masukkan uang yang customer berikan : ")
                if(inpPay == ""):
                    return insertPay()
                elif(inpPay.isdigit()):
                    def runQ(): #running query untuk insert ke payment
                        cur.execute("SELECT MAX(headerID) as 'new' from Order_Header")
                        for hid in cur.fetchone():
                            cur.execute("""insert into payment(headerID, totalcost, totalpaid) 
                                         values(?,?,?)""", (hid, showTemp.thotty, inpPay,))
                    if(int(inpPay) == showTemp.thotty):
                        print("[i] Terima Kasih telah membeli di toko kami, receipt anda akan diprint")
                        showTemp()
                        afterPay(True, False, inpPay)
                        runQ()
                        conn.commit()
                    elif(int(inpPay) > showTemp.thotty):
                        print("[i] Terima Kasih telah membeli di toko kami, receipt anda akan diprint")
                        showTemp()
                        afterPay(True, True, inpPay)
                        runQ()
                        conn.commit()
                    elif(int(inpPay) < showTemp.thotty):
                        print("[!] Uang customer tidak mencukupi!")
                        return insertPay()
                    else:
                        print("[!] Inputan ada yang salah!")
                        return insertPay()                
                else:
                    return insertPay()
                    
            def afterPay(booly, booly2, paid): # addon untuk receiptnya
                if(booly == True and booly2 == False):
                    print("======================================================")
                    print("Uang Anda \t\t\t\t\t\t\t\tRp.",paid)
                    print("======================================================")
                elif(booly == True and booly2 == True):
                    print("======================================================")
                    print("Uang Anda \t\t\t\t\t\t\t\tRp.",paid)
                    print("Kembalian \t\t\t\t\t\t\t\tRp.", int(paid) - showTemp.thotty)
                    print("======================================================")
                    
            def payment():
                showTemp()
                insertOrder()
                insertPay()
                def retry():
                    inpAgain = input("[=] Exit? Y/N : ")
                    if(inpAgain == "N" or inpAgain =="n"):
                        showItem(True)
                    elif(inpAgain == "Y" or inpAgain =="y"):
                        print("[i] Good Bye!")
                    else:
                        return retry()
                retry()
                # print("ini payment placeholder")
            showItem(True)
            
        formOrder()

    squek()
    mainFunc()

main()
conn.close