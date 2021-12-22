Setup untuk API POST
----------------------------

    Prequisite:
        - Install dependency PyJWT (https://pypi.org/project/PyJWT/)
        - Instal Modul rest_api 
        - Install POSTMAN untuk Testing
        - add dbfilter in odoo.conf = nama_db yang digunakan (ex: TEST) // jika satu host multiple db
        
        
### Test On POSTMAN

- Login ( untuk mendapatkan token akses ke API POST)
  - Add New Environments
     - url ==> contoh =  http://10.64.20.27:8069/
     - username ( username untuk login ke odoo )
     - password ( psswd dari username odoo)
     - token ( value kosongin saja )
  - POST Login
      - Bash URL  ==> {{url}}/api/v1/login/ 
      - Headers ==> Key = Content-Type || Value = application/json
      - Request Body 
       ```
          {
            "username":"{{username}}", 
            "password": "{{password}}"
          }
           ```
- POST INVOICE
  - Bash URL ==>  {{url}}/api/v1/post/invoice/
  - Headers ==> 
       - Key = Content-Type || Value = application/json
       - Key = Authorization || Value = Bearer {{token}}
  - Request Body

   ```
      {
            "data": {
                "invoice_date": "2020-08-15",
                "customer_name": "admin", #mandatory boleh customer_name/customer_id
                "bo_code": "INV00391", #mandatory
                "type": "out_invoice", #mandatory & nilainya tetap "outinvoice"
                "invoice_line_ids": [
                    [
                        0,
                        0,
                        {
                            "product_name": "VIP Onsite Package", #mandatory boleh product_id/product_code/product_name 
                            "quantity": 1, #mandatory
                            "price_unit": 2000000, #mandatory
                            "discount": 10 #tentatif
                        }
                    ]
                ]
            }
        }
    ```
- POST Sale Order
  - Bash URL ==>  {{url}}/api/v1/post/sale-order/
  - Headers ==> 
       - Key = Content-Type || Value = application/json
       - Key = Authorization || Value = Bearer {{token}}
  - Request Body

   ```
        {
            "data": {
                "date_order": "2020-09-09",
                "customer_name": "Medika Plaza",#mandatory boleh customer_name/customer_id
                "bo_code": "12345", #mandatory
                "co_name": "Pak Haji", #mandatory 
                "order_line": [
                    [
                        0,
                        0,
                        {
                            "product_name": "Swab Test H+1", #mandatory
                            "product_uom_qty": 1, #mandatory
                            "discount": 10 #tentatif
                        }
                    ]
                ]
            }
        }
    ```

