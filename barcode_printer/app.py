from flask import *
from barcode_print import *
import io
import psycopg2
import pypyodbc as odbc
path = 'C:/Users/myagmardorj/Git/lesson3/barcode_printer/'
odoodatabases = {'34': {'user': 'readonly_c34','password': 'readonly_c34_password','server': '10.34.1.220','port': 5432,'database':'CARREFOURS34_LIVE'},
                '13': {'user': 'postgres','password': 'postgres','server': '10.13.1.220','port': 5432,'database':'CARREFOURS13_LIVE'},
                '88': {'user': 'readonly_c88','password': 'readonly_c88_password','server': '10.88.1.220','port': 5432,'database':'CARREFOURS88_LIVE'},
                '21': {'user': 'readonly_c21','password': 'readonly_c21_password','server': '10.21.1.220','port': 5432,'database':'CARREFOURS21_LIVE'},
                '01': {'user': 'readonly_c01','password': 'readonly_c01_password','server': '10.1.1.220',  'port': 5432,'database':'STORE01_LIVE'},
                '12': {'user': 'readonly_c42','password': 'readonly_c42_password','server': '10.12.1.220',  'port': 5432,'database':'STORE42_LIVE'},
                '06': {'user': 'readonly_c06','password': 'readonly_c06_password','server': '10.6.1.220',  'port': 5432,'database':'STORE06_LIVE'},
                '17': {'user': 'readonly_c17','password': 'readonly_c17_password','server': '10.17.1.220',  'port': 5432,'database':'STORE17_LIVE'},
                '38': {'user': 'readonly_c38','password': 'readonly_c38_password','server': '10.38.1.220',  'port': 5432,'database':'STORE38_LIVE'},
                '25': {'user': 'readonly_c25','password': 'readonly_c25_password','server': '10.25.1.220',  'port': 5432,'database':'STORE25_LIVE'},
                '26': {'user': 'readonly_c26','password': 'readonly_c26_password','server': '10.26.1.220',  'port': 5432,'database':'STORE26_LIVE'},
                '16': {'user': 'readonly_c16','password': 'readonly_c16_password','server': '10.16.1.220',  'port': 5432,'database':'STORE16_LIVE'},
                '22': {'user': 'readonly_c22','password': 'readonly_c22_password','server': '10.22.1.220',  'port': 5432,'database':'STORE22_LIVE'},
                '08': {'user': 'readonly_c08','password': 'readonly_c08_password','server': '10.8.1.220',  'port': 5432,'database':'STORE08_LIVE'},
                '39': {'user': 'readonly_c39','password': 'readonly_c39_password','server': '10.39.1.220',  'port': 5432,'database':'STORE39_LIVE'},
                '32': {'user': 'itid','password': 'it#2016','server': '10.32.1.220',  'port': 5432,'database':'STORE32_LIVE'},
                '61': {'user': 'itid','password': 'it#2016','server': '10.61.1.220',  'port': 5432,'database':'STORE61_LIVE'},
                '62': {'user': 'itid','password': 'it#2016','server': '10.62.1.220',  'port': 5432,'database':'STORE62_LIVE'},
                '33': {'user': 'itid','password': 'it#2016','server': '10.33.1.220',  'port': 5432,'database':'STORE33_LIVE'},
                '20': {'user': 'itid','password': 'it#2016','server': '10.20.1.220',  'port': 5432,'database':'DC'},
                '00': {'user': 'itid','password': 'it#2016','server': '10.0.99.220',  'port': 5432,'database':'CENTRAL_PREGOLIVE'}
}
def postg_return_value(conn,query):
    global stringa;
    cursor = conn.cursor()
    cursor.execute(query)

    data = cursor.fetchall()
    #print(len(data))
    #for row in data:
        #print(row)
        #stringa = row;
    conn.close()
    return data

query_get_barcodes = "SELECT * FROM product_product where barcode = '"
query_get_template = "select name,list_price from product_template where id = '"
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():

    return render_template('about.html')

@app.route('/button_clicked', methods=['POST'])
def button_clicked():
    global product_template_table
    user_input = request.form.get('user_input')
    baraaner = request.form.get('second_input')
    expire = request.form.get('fourthinput')

    logo = request.form.get('dropdown')
    button_type = request.form.get('button_type')
    ishavedate = request.form.get('dropdown2')
    print('date ',ishavedate)
    papersize = request.form.get('dropdown3')
    

    if logo == "sansar":
        isSansar = 1
    else:
        isSansar = 0

    if ishavedate == "yes":
        ishavedate = 1
    else:
        ishavedate = 0
    if papersize =="4030":
        width_mm = 60   
        height_mm = 45
    elif papersize == "6040":
        width_mm = 90   
        height_mm = 60
    if button_type == "button1":
        barcode_usr = request.form.get('user_input')
        
        output_file = "output_with_text.png"
        
        text_content = product_template_table[0][0]
        barcode_text = "Код: "+str(barcode_usr)
        barcode = str(barcode_usr)
        price = "Үнэ: "+str(product_template_table[0][1])

        image = generate_white_png_with_text(width_mm, height_mm, output_file, text_content,barcode,barcode_text,price,ishavedate,isSansar,expire)
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)

        # Return the PNG image as a response with appropriate headers
        return send_file(img_byte_array, as_attachment=True, download_name='sample_image.png', mimetype='image/png')
    elif button_type == "button2":
        barcode_usr = request.form.get('user_input')
        itemname_usr = request.form.get('second_input')
        thirtinput_usr = request.form.get('thirtinput')
        salbar_usr=request.form.get('dropdown1')
        type=request.form.get('dropdown')
        expire = request.form.get('fourthinput')
        
        conp = psycopg2.connect(database=odoodatabases[salbar_usr[6:]]['database'], user=odoodatabases[salbar_usr[6:]]['user'], password=odoodatabases[salbar_usr[6:]]['password'], host=odoodatabases[salbar_usr[6:]]['server'], port= odoodatabases[salbar_usr[6:]]['port'])
        product_product_table = postg_return_value(conp,query_get_barcodes+barcode_usr+"'")
        print(product_product_table[0][0])
        conp = psycopg2.connect(database=odoodatabases[salbar_usr[6:]]['database'], user=odoodatabases[salbar_usr[6:]]['user'], password=odoodatabases[salbar_usr[6:]]['password'], host=odoodatabases[salbar_usr[6:]]['server'], port= odoodatabases[salbar_usr[6:]]['port'])
        product_template_table = postg_return_value(conp,query_get_template+str(product_product_table[0][0])+"'")
        print(product_template_table)

        defaultvalue = product_template_table[0][0]   # барааны нэр 
        defaultprice = int(product_template_table[0][1])
        return render_template('about.html',item_name=defaultvalue,price=defaultprice,barcode=barcode_usr,selected_option=type,selected_salbar=salbar_usr,selected_option2=ishavedate,selected_option3=papersize,expireday=expire)


if __name__ == '__main__':
    app.run(debug=True)
