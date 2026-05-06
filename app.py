import socket
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopkorean.db'
db = SQLAlchemy(app)

# Модель товара
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    sostav = db.Column(db.String(100))
    barcode = db.Column(db.String(100))
    typelabel = db.Column(db.Integer)
    formatfield = db.Column(db.Boolean, default=True, nullable=False)

  #  price = db.Column(db.Float)

# Создание базы и 15 тестовых товаров
with app.app_context():
    db.create_all()
    # if not Product.query.first():
        # for i in range(1, 16):
        #     db.session.add(Product(name=f"Товар №{i}", price=100.0 + i*10))
        # db.session.commit()
    # Проверяем, пустая ли база, прежде чем добавлять данные
    if not db.session.get(Product, 1):
        test_product = Product(
            id=1,
            name="ЛУК ЖАРЕННЫЙ",
            sostav=(f"Состав: лук,пальмовое масло,пшеничная мука, соль "
                f"Изготовитель: Цзянсу пищевая компания Хайленд, Китай. Импортер «ООО Промпоствка-М»"
                f"Адрес: Москва, Орджоникидзе 11 стр 43 "
                f"Расфасовка: ИП Воронец О.Н. "
                f"Адрес: Оренбург, Карагандинская 25/1 "
                f"Энерг.ценность: 276Ккал. "
                f"Пищевая ценность: Белки:6г, Жиры:43г, Угл:41г "
                f"Срок годности: 30 сут при t не выше 25С "
                f"Дата и время вскрытия и фасовки:"
                ),
            barcode="2001000000616",
            typelabel=1,
            formatfield=False
        )
        db.session.add(test_product)
        test_product = Product(
            id=2,
            name="Сыр плавленый",
            sostav=(f"Состав: Сыры, масло сливочное, молоко сухое обезжиренное, эмульгаторы (Е331,339), соль, лимонная кислота, пищевые красители (Е160а,Е160С), белок молочный, вода, растительный жир"
                    f"Изготовитель:ООО «Хохланд Руссланд», г.о Раменский , п Раменской агрохимстанции д16."
                    f"Расфасовка: ИП Воронец О.Н.г Оренбург, ул Карагандинская 25/1"
                    f"Масса нетто: 13гр; Срок годности 5 суток при температуре +2С-+6С"
                    f"Пищевая и энергетическая ценность: Б-19г; Ж-27г; У-5г. 343Ккал/1422 кДж"
                    f"Дата и время вскрытия и фасовки:"
                    ),
            barcode="2001000000623",
            typelabel=2,
            formatfield=False
        )
        db.session.add(test_product)
        test_product = Product(
            id=3,
            name="Сосиска сливочные",
            sostav=(
                f"Состав: свинина,говядина,филе куриное,вода питьевая, сливки,нитритно посолочная смесь,соль,пищевые пшеничные волокна,регулятор кислотности,декстроза, уселитель вкуса и аромата(глутамат натрия),антиокислитель(аскорбиновая кислота),перец черный, мускатный орех,кардамон,перец белый,загустители(каррагинан из водорослей гуаровая и ксантановые камеди,эмульгатор (эфиры глицерина и лимонной и жирных кислот),краситель(кармин).На предприятии используются яйца,соя,молоко,глютен,горчица и продукты их преработки"
                f"Изготовитель: ООО «Мясокомбинат «ЖеЛеН» ,Ореббургская область ,г Орск, с Ударник, ул Школьная 11 "
                f"Фасовщик: ИП Воронец О.Н., г.Оренбург, ул Карагандинская 25/1 "
                f"Масса нетто 66г; Срок годности 5 суток при температуре +2С-+6С "
                f"Пищевая и энергетическая ценность на 100гр : Б-10гр; Ж-20г; Ккал-220/921 кДЖ"
                f"Дата, время вскрытия и фасовки:"
            ),
            barcode="2001000000630",
            typelabel=2,
            formatfield=False
        )
        db.session.add(test_product)
        test_product = Product(
            id=4,
            name="Креветка жареная",
            sostav=(
                f"Состав: креветка, масло растительное, вино белое сухое, соль, перец черный, чеснок"
                f"Изготовитель: ИП Воронец О.Н. г.Оренбург ,ул Карагандинская 25/1"
                f"Масса нетто -30гр; Срок годности 5 суток при температуре хранения +2С-+6С"
                f"Пищевая и энергетическая ценность на 100гр продукта: Б-18,5; Ж- 8,0; У-1.2; 155Ккал/650 кДж"
                f"Дата и время приготовления и упаковки:"
            ),
            barcode="2001000000647",
            typelabel=2,
            formatfield=False
        )
        db.session.add(test_product)
        test_product = Product(
            id=5,
            name="Имбирь маринованный розовый ",
            sostav=(
                f"Состав: имбирь,вода,соль, уксусная ктслота, консервант сорбат калия,уселитель вкуса глутамат натрия, подсластитель аспартам, сахарин, пищевой краситель красный."
                f"Изготовитель: Китай, Цзинань «Золотой урожай». Импортер ИП Раденко Р.Г., Московская область, г Истра, ул Фадеева 11-5"
                f"Расфасовка: ИП Воронец О.Н. г.Оренбург. ул Карагандинская 25/1"
                f"Масса нетто: 15гр Срок годности 5 суток . Хранить при температуре +2С-+6С"
                f"Пищевая и энергетическая ценность на 100гр. Б- 1.8; Ж-8; У- 1,3 17.6 Ккал/ 76 кДж"
                f"Дата, время вскрытия и фасовки:"
            ),
            barcode="2001000000654",
            typelabel=2,
            formatfield=False
        )
        db.session.add(test_product)
        test_product = Product(
            id=6,
            name="Яйцо куриное вареное очищенное ",
            sostav=(
                f"Состав: яйцо куринное"
                f"Изготовитель ИП Воронец О.Н. г.Оренбург, ул Карагандинская 25/1"
                f"Масса нетто 50гр, Срок годности -5 суток при температуре +2С - +6С"
                f"Пищевая и энергетическая ценность на 100гр продукта: Б-12.7; Ж-11.5; У- 0.7г 157-Ккал/ 657 кДж"
                f"Дата и время приготовления: "
            ),
            barcode="2001000000661",
            typelabel=2,
            formatfield=False
        )
        db.session.add(test_product)

        test_product = Product(
            id=7,
            name="Бекон копчено-вареный",
            sostav=(
                f"Состав: свинина, вода, посолочная смесь, соль пищевая,фиксатор окраски У250,регуляторы кислотности Е451,Е331,Е262,молочный белок,стабилизаторы Е452,Е450,загустители Е407,Е412,уселитель вкуса и аромата Е621, ароматизатор(свинина) ,агент влагоудерживающий Е325."
                f"Изготовитель:ООО» Мясокомбинат ЭКО» Московская область, г Дмитров , ул Дорожная 59"
                f"Расфасовка: ИП ВоронецО.Н. ,г Оренбург , ул Карагандинская 25/1"
                f"Масса нетто: 30г. Срок годности 5 суток. Хранить при температуре +2С-+6С"
                f"Пищевая и энергетическая ценность на 100гр: Б-8гр, Ж-55г 527Ккал/ 2171 кДж."
                f"Дата,время вскрытия и фасовки:"
            ),
            barcode="2001000000678",
            typelabel=2,
            formatfield=False
        )
        db.session.add(test_product)

        test_product = Product(
            id=8,
            name="Курица жареная",
            sostav=(
                f"Состав: мясо курицы, перец черный, паприка сладкая, кориандр молотый, зира молотая, тимьян, чеснок сухой, соль, вода"
                f"Масса нетто: 40 гр. Срок годности при температуре +2С- +6С – 5 суток. "
                f"Пищевая и энергетическая  ценность на 100гр. Б- 25.4; Ж – 7; У-0,4. 206Ккал/862 кДж"
                f"Изготовлено и упаковано: "
            ),
            barcode="2001000000685",
            typelabel=2,
            formatfield=False
        )
        db.session.add(test_product)
        test_product = Product(
            id=9,
            name="Свинина жареная",
            sostav=(
                f"Состав: мясо свинина, соль, перец черный, перец душистый, перец чили, паприка сладкая, кориандр молотый, зира молотая, тимьян, чеснок сухой,вода"
                f"Изготовитель: ИП Воронец О.Н. г.Оренбург, ул Карагандинская 25/1"
                f"Масса нетто: 40гр.Срок годности при температуре +2С - +6С – 5 суток"
                f"Пищевая и энергетическая ценность на 100гр.Б-17гр, Ж-22 У-0;  266 Ккал/1113 кДж"
                f"Изготовлено и упаковано: "
            ),
            barcode="2001000000692",
            typelabel=2,
            formatfield=False
        )
        db.session.add(test_product)
        test_product = Product(
            id=10,
            name="Кукуруза консервированная",
            sostav=(
                f"Состав: кукуруза в зернах,вода питьевая,сахар,соль."
                f"Изготовитель: Джиянг Джонг Фуд Ко. ,Китай. Импортер ООО «КП Импорт». Московская область, Мытищинский район. Д Коргашено ул Центральная 62А."
                f"Расфасовка: ИП Воронец О.Н. г Оренбург ул Карагандинская 25/1"
                f"Масса нетто: 30гр. Срок годности при температуре +2 С-+6С  - 5 суток"
                f"Пищевая и энергетическая ценность на 100гр : Б- 28.7; Ж- 0.6; У-9,9.  57,8 Ккал/242 кДЖ"
                f"Дата и время вскрытия и фасовки: datatime"
            ),
            barcode="2001000000708",
            typelabel=2,
            formatfield=False
        )
        db.session.add(test_product)
        test_product = Product(
            id=11,
            name="Дайкон маринованный",
            sostav=(
                f"Состав: редис,вода, соль,регуляторы кислотности:ледяная уксусная кислота, лимонная кислота, Консерванты:сорбат калия и пиросульфат натрия,одсластитель:аспартам,сукралоза, сахарин натрия и ацесульфам калия,краситель Е102. "
                f"Импортер ООО «Фактор-ФУД г Москва,г.Муниципальный округ Текстильщики, ул Артюхиной 66"
                f"Расфасовка: ИП Воронец О.Н. г Оренбург ул Карагандинская 25/1"
                f"Масса нетто:15гр. Срок годности 5 суток. Хранить при температуре +2С-+6С"
                f"Пищевая и энергетическая ценность на 100г: Б-0; иЖ- 0.,У-3.9., ккал-15/кДж 66"
                f"Дата и время вскрытия и фасовки:"
            ),
            barcode="2001000000715",
            typelabel=1,
            formatfield=False
        )
        db.session.add(test_product)
        test_product = Product(
            id=12,
            name="Крабовое мясо (эмитация) ",
            sostav=(
                f"Состав: фарш рыбный минтай,сардинелла,вода,крахмал кукурузный,масло растительное,белок соевый,соль,сахар,глутамат натрия,красители(кармины,экстракт паприки. Содержат аллергены (рыба,яйца,глютен)"
                f"Изготовитель: ООО» Вичи-Русь»,Россия,Калининградская обл,г Советск,ул Маяковского 3Б"
                f"Упаковано: ИП Воронец О.Н. г Оренбург,ул Карагандинская 25/1"
                f"Масса нетто:40гр"
                f"Срок годности : 5 суток ; Хранить при температуре +2С-+6С.Пищевая  ценность: Б-5.14г,Ж-0.6г, У-20.6 Ккал-108г"
                f"Дата и время вскрытия и фасовки:"
            ),
            barcode="2001000000722",
            typelabel=2,
            formatfield=False
        )
        db.session.add(test_product)
        test_product = Product(
            id=13,
            name="Кунжут жареный (семена) ",
            sostav=(
                f"Состав: кунжут белый, кунжут черный  "
                f"Фасовка: ИП Воронец О.Н. г.Оренбург, ул Карагандинская 25/1"
                f"Масса нетто: 3г Срок годности 12 месяцев"
                f"Пищевая ценность (на 100 г): белки — 19 г, жиры — 49 г, углеводы — 12 г. Энергетическая ценность: 565 ккал / 2365 кДж."
                f"Дата и время вскрытия и упаковки:"
            ),
            barcode="2001000000739",
            typelabel=1,
            formatfield=False
        )
        db.session.add(test_product)
        test_product = Product(
            id=14,
            name="Зеленый лук",
            sostav=(
                f"Состав: лук зеленый свежий"
                f"Изготовитель: ИП Воронец О.Н. г.Оренбург, ул Карагандинская 25/1"
                f"Масса нетто: 10 г"
                f"Масса нетто: 3г Срок годности 12 месяцев"
                f"Срок годности: 5 суток  при температуре от +2 °С до +6 °С Пищевая ценность и энергетическая ценность в 100г: белки — 1,3 г; жиры — 0,1 г; углеводы — 3,2 г. 20 ккал / 85 кДж"
                f"Дата и время упаковки:"
            ),
            barcode="2001000000746",
            typelabel=2,
            formatfield=False
        )
        db.session.add(test_product)
        test_product = Product(
            id=15,
            name="Грибы Эноки",
            sostav=(
                f"Страна происхождения Китай. Импортер ООО «Дракон» Москва ул Академика Варга д8к1.Поставщик ООО «Есть грибы» Москва г.муниципальный округ Очаково-Матвеевское, ул Никулевская д 33,стр1,помещ 67."
                f"Расфасовка: ИП Воронец О.Н. г.Оренбург, ул Карагандинская 25/1"
                f"Масса нетто: 20г. Срок годности – 5 суток при температуре +2С -+6С."
                f"Пищевая и энергетическая ценность: Б-2.7; Ж-0.3,У -3,1 Ккал-37"
                f"Дата и время вскрытия и фасовки:"
            ),
            barcode="2001000000753",
            typelabel=2,
            formatfield=False
        )
        db.session.add(test_product)
    db.session.commit()


@app.route('/')
@app.route('/product/<int:p_id>')
def index(p_id=1):
    # 1. Считаем сколько всего товаров в базе данных
    max_id = db.session.query(db.func.count(Product.id)).scalar()

    # 2. Ограничиваем p_id, чтобы не выйти за пределы (от 1 до max_id)
    if max_id == 0:
        return "База данных пуста"
    # Ограничиваем id диапазоном от 1 до 15
    p_id = max(1, min(p_id, max_id))
    product = Product.query.get(p_id)
    return render_template('index.html', product=product,max_id=max_id)

@app.route('/print', methods=['POST'])
def print_route():
    try:
        p_id = int(request.form.get('product_id'))
        qty = request.form.get('quantity', 1)

        print_tspl_label(p_id, qty)

        # Здесь логика печати
        # return f"Отправлено на печать: {p_name}, количество: {qty} шт."
        # return "OK", 200  # Отправляем статус 200 (Успешно) без перезагрузки
        return jsonify({"status": "success", "message": "Печать запущена"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



def split_fixed(text, width):
    """Нарезает текст строго по ширине, игнорируя пробелы (режет слова)"""
    return [text[i:i + width] for i in range(0, len(text), width)]


def print_tspl_label(product_id, count=1, port=9100):

    # 1. Данные товара (позже здесь будет запрос к БД по product_id)
    print(f"Попытка печати товара с ID: {product_id}")  # Добавьте это
    product = Product.query.get(product_id)
    if not product:
        print("ОШИБКА: Товар не найден в БД!")
        return False

    # product = Product.query.get(product_id)
    p_name = product.name
    p_sostav = product.sostav or ""  # Если состава нет, будет пустая строка
    barcode = product.barcode or "0000000000000"


    if product.typelabel == 1:
        size = "SIZE 43 mm, 25 mm"
        barcode_h = 80
        ipaddress = "192.168.1.154"
        width = 33
    else:
        size = "SIZE 58 mm, 40 mm"
        barcode_h = 240
        ipaddress = "192.168.1.154"
        width = 48


    # 2. Формирование списка команд
    commands = []
    commands.append(size)
    commands.append("DIRECTION 1")
    commands.append("CLS")
    commands.append("CODEPAGE 1251")

    # Заголовок (Шрифт "2" — крупнее)
    commands.append(f'TEXT 20,2,"2",0,1,1,"{p_name}"')

    # Нарезка и вывод основного текста (Шрифт "1" — мелкий)

    y = 25

    if product.formatfield:

        # ЛОГИКА 1: Построчный вывод (разбиваем по \n)
        lines = p_sostav.split('\n')
        for line in lines:
            line = line.strip()  # убираем лишние пробелы по краям
            if line:  # печатаем только непустые строки
                commands.append(f'TEXT 20,{y},"1",0,1,1,"{line}"')
                y += 12
    else:
        # ЛОГИКА 2: Автоматическая нарезка (ваш старый метод)
        lines = split_fixed(p_sostav, width)
        for line in lines:
            commands.append(f'TEXT 20,{y},"1",0,1,1,"{line}"')
            y += 12
    print(f"ID: {product_id}")  # Добавьте это
    # 4. Финальные данные
    commands.append(f'BARCODE 40,{barcode_h},"EAN 13",20,10,0,2,2,"{barcode}"')

    current_date = datetime.now().strftime("%d.%m.%Y %H:%M")

    # # Получаем текущую дату
    # today = datetime.now()
    # # Прибавляем 1 день
    # tomorrow = today + timedelta(days=1)
    # tomorrow_date = tomorrow.strftime("%d.%m.%Y")
    # commands.append(f'TEXT 20,{barcode_h-20},"1",0,1,1,"Дата фасовки: {current_date}"')
    commands.append(f'TEXT 20,{barcode_h - 20},"1",0,1,1,"{current_date}"')
    # Печать нужного количества копий
    commands.append(f"PRINT 1,{count}")


    # 3. Сборка в одну строку
    tspl_commands = "\r\n".join(commands) + "\r\n"
    print(tspl_commands)
    # 4. Отправка на принтер
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((ipaddress, port))
            s.sendall(tspl_commands.encode('cp1251'))
            print(f"Успешно отправлено на {ip_address}")
            return True
    except Exception as e:
        print(f"Ошибка при печати: {e}")
        return False



# Страница списка всех товаров (Админка)
@app.route('/admin')
def admin_index():
    products = Product.query.all()
    return render_template('admin.html', products=products)


# Добавление товара
@app.route('/admin/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    sostav = request.form.get('sostav')
    barcode = request.form.get('barcode')
    barcode = request.form.get('barcode')

    formatfield = True if request.form.get('formatfield') else False

    #  price = request.form.get('price', 0)

    new_product = Product(name=name, sostav=sostav, barcode=barcode,formatfield = formatfield)
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('admin_index'))


# Редактирование товара (получение данных для формы)
@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.sostav = request.form.get('sostav')
        product.barcode = request.form.get('barcode')
        product.barcode = request.form.get('barcode')
        product.formatfield = True if request.form.get('formatfield') else False
     #   product.price = float(request.form.get('price'))
        db.session.commit()
        return redirect(url_for('admin_index'))
    return render_template('edit.html', product=product)


# Удаление товара
@app.route('/admin/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin_index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4444, debug=True)
