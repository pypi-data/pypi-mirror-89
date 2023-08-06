ipybd 是一款由 `Python` 语言开发的中文生物多样性数据清洗、统计与分析框架。当前 `ipybd` 主要聚焦于构建众源数据集与生物多样性数据库之间的通道。在此之前，国内生物多样性数据的提取、转换、装载（ETL）等处理尚不成体系，不同数据源、不同数据集，不同数据清理者所采用的数据处理方式往往会有很大的差异。因此即便使用相同的处理工具，相应数据的处理方式也很难被复用到不同的数据处理工作之中。这导致数据链路中的采集者、接收者、利用者都需要为数据的标准化付出巨大的精力和时间。经验上这一工作至少会占据 70% 的链路时间。`ipybd` 则实现了一个**通用**的生物多样性数据提取、转换、装载框架，它可以显著提升数据平台（如 CVH/NSII）、数据接收机构（如标本馆）、数据利用者（如科研工作者）对不同来源、不同格式、不同品质、不同规范的数据集进行统一的清洗转换与整合利用的能力，从而大幅降低数据处理的门槛和成本，提高数据分析前的数据处理效率和品质。

作为一个框架，`ipybd` 不仅定义了一套生物多样性数据处理的流程和语义，还为开发者提供了一些重要的数据处理方法，这包括：

1. **数据装载**： 目前支持从Excel/CSV/TEXT/Pandas.DataFrame 以及关系型数据库（比如Mysql）导入数据；

2. **物种学名**：可以在线批量获取 [POWO](http://www.plantsoftheworldonline.org/), [IPNI](https://www.ipni.org/), [中国生物物种名录](http://www.sp2000.org.cn/)上相应物种的最新分类阶元、分类处理、物种图片、发表文献、相关异名等信息；

3. **日期与时间**：可以对各类手工转录的日期和时间，进行严格的校验和转换，并可根据需要输出不同样式；

4. **经纬度**：可以对各类手工转录的经纬度，进行严格的校验和转换；

5. **行政区划**：可以对各种自然语言表达的中文县级及其以上的行政区划进行高品质的匹配、校正和转换；

6. **点选值**：能够自定义各种字段的可选值和转换关系，并根据转换关系，自动完成值的规范化；

7. **数值和数值区间**：可以对各类数值或数值区间，进行自动化的清洗、校正和转换；

8. **拆分与合并**：`ipybd` 不仅可以对数据列进行各种合并和拆分，还可以将单列、多列或整个表格的数据列映射为各类 Python `dict`/`list` 对象或者 JSON `Object` 和 `Array`，从而为各种数据分析和互联网平台的数据交换工作提供灵活的格式转换支持。

9. **DarwinCore 数据模型**：提供了完善的各类中文字段名到标准的 DarwinCore 字段名的自动映射支持和半自动映射引导，同时 ipybd 还提供了相应的 DarwinCore 数据模型类，能够将绝大多数不同结构不同数值格式的生物多样性数据表重塑为统一规范的数据表，因此可以极大的简化不同数据集的标准化聚合工作。

10. **自定义数据模型**：除了 DarwinCore， 用户还可以通过 `Enum` 类在 `ipybd` 定义的语义下对上述各种能力进行自由拼接和组合，快速定制出个性化的数据模型，以应对不同需求的众源数据处理。

11. **标签打印**：能够生成传统标签样式和带有条形码/二维码样式的纸质标签文档以供打印（后续还会提供标签模版自定义功能）。

12. **`Pandas`**： Pandas 是整个 `Python` 数据分析生态中的核心库，`ipybd`基底数据结构完全基于 `Pandas.DataFrame` ，因此可以直接使用 `Pandas` 生态完善的数据统计分析功能。

13. **数据输出**：经过处理的数据，可以输出为Excel/CSV文件或者直接更新至相应的数据库之中。

    

[toc]



## 一、安装方法

通过 pip 在线安装 ipybd：

```python
pip install ipybd
```
或者将程序包 Clone 到本地后，在终端内进入 ipybd 目录，然后运行：

```python
pip install .
```



##二、主要的数据处理方法

### 1. BioName

BioName 类可接受单个学名字符串、`tuple`、`list`或`Pandas.Series` 类型的学名字符串序列实例化对象：

```python
from ipybd import BioName

poa = BioName(["Poaceae", "Poa", "Poa annua", "Poa annua Schltdl. & Cham.", "Poa annua L.", None])
```
参与实例化的学名可以包含命名人（命名人的写法可随意），也可以不包含命名人（但包含命名人可以提高匹配精度），学名格式可以比较规范，也可以是不太规范的人工转录学名（但不能简写属名或种名）。

BioName 实例主要通过 `get`方法配合关键字从 [powo](http://www.plantsoftheworldonline.org/)、[ipni](www.ipni.org)、[中国生物物种名录](www.sp2000.org.cn) 获取相关学名的分类阶元、分类处理、物种图片、发表文献、相关异名等数据 。下面以获取上文 `poa` 实例对象在`powo`平台上的科属地位为例：

```python
poa.get('powoName')

Out:
[
  ('Poaceae', 'Barnhart', 'Poaceae'),
 	('Poa', 'L.', 'Poaceae'),
 	('Poa annua', 'L.', 'Poaceae'),
 	('Poa annua', 'Schltdl. & Cham.', 'Poaceae'),
 	('Poa annua', 'L.', 'Poaceae'),
 	(None, None, None)
]

```
默认返回的结果是以元组为元素的 `list` 对象，`list`对象中的各检索结果与检索词的位置一一对应，对于没有检索结果的值，则以`None`值补充并与其他各检索结果对齐，以方便直接将返回结果转换成表格的行列；若希望以 `dict`对象返回，在请求时则可以通过`typ`参数指定：

```python
poa.get('powoName', typ=dict)  

Out:
{
  'Poaceae': ('Poaceae', 'Barnhart', 'Poaceae'),
 	'Poa': ('Poa', 'L.', 'Poaceae'),
 	'Poa annua': ('Poa annua', 'L.', 'Poaceae'),
 	'Poa annua Schltdl. & Cham.': ('Poa annua', 'Schltdl. & Cham.', 'Poaceae'),
 	'Poa annua L.': ('Poa annua', 'L.', 'Poaceae')
}
```

除了上述示例中的`powoName`参数，目前`BioName`的`get`关键字总共有 9 个，以适应不同需求：

+ `'powoName'`: 获取 powo 平台相应学名的科属地位、学名简写和命名人信息；

+ `'powoImages'`: 获取 powo 平台相应学名的物种图片地址，每个物种返回三张图片地址；

+ `'powoAccepted'`: 获取 powo 平台相应学名的接受名；

+ `'ipniName'`: 获取 ipni 平台相应学名的科属地位、学名简写和命名人信息；

+ `'ipniReference'`: 获取 ipni 平台相应学名的发表文献信息；

+ `'colName'`: 获取相应学名在中国生物物种名录中的科属地位、学名简写和命名人信息；

+ `'colTaxonTree'`: 获取相应学名在中国生物物种名录中的完整的分类学阶元信息；

+ `'colSynonyms'`: 获取相应学名在中国生物物种名录中的异名信息;

+ `'stdName'`: 优先获取中国生物物种名录的名称信息，如果无法获得，则获取`ipni`的信息。 

使用时，只需将上例`get`方法中的相应关键字替换为所需关键字即可。

### 2. FormatDataSet

`FormatDataSet` 类是 ipybd 进行数据处理的核心类。它提供了对生物多样性相关的各类数据表进行各种表结构重构和值格式化处理的基本方法。普通用户也可以直接调用它以更加自主的方式处理个性化的数据集或者开发自己的脚本和程序。

#### 2.1 数据的装载

目前 FormatDataSet 可接受一个 Excel、CSV、TXT、Pandas.DataFrame、RDBMS 数据库对象进行实例化：基于 Excel 、CSV 、TXT 数据表实例化，可以直接传递相应文件的路径给 `FormatDataSet`：

```python
collections = FormatDataSet(r"~/Documents/record2019-09-10.xlsx") 
```

`FormatDataSet` 默认采用 UTF-8 编码文件，如果传递 CSV 文件出现`UnicodeDecodeError`错误，可以尝试显式指定相应的编码方式，一般都可以得到解决（Python 可选用的标准编码[戳这里](https://docs.python.org/3/library/codecs.html#standard-encodings)）。

```python
# 这里显式的指定了 csv 文件的编码方式为 gbk
collections = FormatDataSet(r"~/Documents/record2019-09-10.cvs", encoding='gbk') 
```

如果已经有一个 DataFrame 对象，也可以直接传递给 `FormatDataSet`：

```pythoon
collections = FormatDataSet(DataFrame)
```

基于本地或线上的关系型数据库创建 `FormatDataSet` 实例，需要先创建数据库连接。在 python 生态中有很多数据库连接器，比如 mysqlclient、pymysql、mysql-connector 等等，下方示例使用的是 sqlalchemy 建立 mysql 数据库连接，个人可以根据喜好自行选择相应的连接库创建连接器。

```python
# 首先导入相应的连接库
from sqlalchemy import create_engine

# 通过账户、密码、地址、端口等创建连接器
# 这里演示了与我本地 mysql 中 ScientificName 数据库建立连接
conn = create_engine('mysql+pymysql://root:mypassward@localhost:3306/ScientificName')

# 然后建立检索数据库的 sql 语句，用于筛选出需要的数据
# 这里的sql语句演示了从 ScientificName 数据库中调取 10 条 theplantlist 学名数据
sql = "select * from theplantlist limit 10;"

# 将 sql 语句和建立好的连接器传递给 ipybd.FormatDataSet
tpl = FormatDataSet(sql, conn)

# 执行完毕后，数据会以 DataFrame 结构保存 tpl 实例的 df 对象
# 然后就可以在本地内存中对这些数据进行各种操作了
# 比如查看数据中的学名 id 、family、genus 和拉丁名信息
tpl.df[['_id', 'family', 'genus', 'latin']] 

Out:
                        _id          family        genus                 latin
0  59367c08ec325b77e9124490     Achariaceae                          Chilmoria
1  59367c08ec325b77e9124491                                        Achariaceae
2  59367c08ec325b77e9124492     Achariaceae    Chilmoria     Chilmoria odorata
3  59367c08ec325b77e9124494  Alseuosmiaceae                         Alseuosmia
4  59367c09ec325b77e9124495                                     Alseuosmiaceae
5  59367c09ec325b77e9124496  Alseuosmiaceae   Alseuosmia    Alseuosmia banksii
6  59367c09ec325b77e9124498   Allisoniaceae                        Calycularia
7  59367c09ec325b77e9124499                                      Allisoniaceae
8  59367c09ec325b77e912449a   Allisoniaceae  Calycularia  Calycularia compacta
9  59367c09ec325b77e912449c     Acanthaceae                        Acanthodium
```

#### 2.2 学名处理

`FormatDataSet` 类基于 `BioName` 实例封装了一些学名处理方法，以便用户能够更便捷的对数据表中的名称进行处理。比如对于上述 `collections` 实例，若相关数据表中的学名并非单列，而是按照 `"属名"`、`"种名"`、`"种下单元"`、`"命名人"`四列分列存储，单纯使用 `BioName` 类需要用户先自行合并相应数据列才可以执行在线查询。而 `FormatDataSet` 实例则可以直接进行学名的查询和匹配：

```python
# 这里以获取 ipni 平台的信息为例
# 调用 get_ipni_name 时，可直接将多个列名按序传递给方法
collections.get_ipni_name("属名", "种名", "种下单元", "命名人")

Out:
[
	('Clematis', 'L.', 'Ranunculaceae'),
 	('Crepis', 'L.', 'Asteraceae'),
 	('Krascheninnikovia ceratoides', '(L.) Gueldenst.', 'Chenopodiaceae'),
	('Apiaceae', 'Lindl.', 'Apiaceae'),
 	('Boerhavia', 'L.', 'Nyctaginaceae'),
 	('Aster', 'L.', 'Asteraceae'),
 	('Agropyron cristatum', '(L.) P.Beauv.', 'Poaceae'),
 	('Orostachys', 'Fisch.', 'Crassulaceae'),
 	('Ephedra', 'L.', 'Ephedraceae'),
 	('Elymus', 'Mitchell', 'Poaceae'),
 	('Aster', 'L.', 'Asteraceae'),
 	('Nitraria tangutorum', 'Bobrov', 'Zygophyllaceae'),
 	(None, None, None),
 	('Carissa', 'L.', 'Apocynaceae'),
 	('Pedicularis', 'L.', 'Scrophulariaceae'),
 	('Centaurea', 'L.', 'Asteraceae'),
 	...
 ]
```

如上所示，不同数据表的学名表示方式时常会有差异，而通过诸如`get_ipni_name`方法这样的 `FormatDataSet` 实例方法可以大幅提高数据处理的便捷性和灵活性。目前 `FormatDataSet` 实例共支持以下几种学名处理方法：

+ `get_powp_name`: 获取 powo 平台相应学名的科属地位、学名简写和命名人信息；

+ `get_powo_images`: 获取 powo 平台相应学名的物种图片地址，每个物种返回三张图片地址；

+ `get_powo_accepted`: 获取 powo 平台相应学名的接受名；

+ `get_ipni_name`: 获取 ipni 平台相应学名的科属地位、学名简写和命名人信息；

+ `get_ipni_reference`: 获取 ipni 平台相应学名的发表文献信息；

+ `get_col_name`: 获取相应学名在中国生物物种名录中的科属地位、学名简写和命名人信息；

+ `get_col_taxontree`: 获取相应学名在中国生物物种名录中的完整的分类学阶元信息；

+ `get_col_Synonyms`: 获取相应学名在中国生物物种名录中的异名信息。

如果在使用这些方法时，并不希望程序直接返回结果，而是想直接将查询结果写入`collections`数据表，请求时可以将`concat`参数设置为`True`:

```python
collections.get_ipni_name("属名", "种名", "种下单元", "命名人", concat=True)
```

如果需要将整合后的数据表存储为文件，可以调用`collections`的`save_data`方法：

```python
collections.save_data(r"~/Documents/new_record.xlsx")
```

#### 2.3 中文行政区划清洗和转换

同物种学名一样，数据表中的中文行政区划也有可能是多列或单列。`FormatTale`提供了类似的方法对其进行批量清洗和转换。

```python
# FormatDataSet 实例可以通过 df 属性获得数据表的 DataFrame
# 下行代码输出了 collections 前 30 行记录的行政区划：
collections.df[["国别", "行政区"]].head(30)                                                                                                                                                                                           

Out:
     国别        行政区
0    中国        NaN
1    中国       大理南涧
2    中国  河北，承德，栾平县
3    中国       广东白云
4    中国    云南省云南楚雄
5    中国  甘肃省Anning
6   NaN         白云
7    中国     河北，承德县
8    中国      云南省大理
9    中国       台湾新竹
10   中国       内蒙白云
11   中国         海南
12  NaN         河南
13   中国         河北
14   中国       云南楚雄
15   中国      新竹市东区
16   中国  云南 Anning
17   中国   台湾新竹市,东区
18   中国        祥云县
19   中国         云县
20   中国         东昌
21   中国        东昌府
22   中国       江西东乡
23   中国        东乡族
24   中国      in 德钦
25   中国     安徽省怀远县
26   中国     黑龙江伊春市
27   中国         云龙
28   中国       四川南川
29   中国         龙江

```

可以发现 `collections` 实例的数据表中，每条记录的行政区划都是按照`"国别"`和`"行政区"`两个字段进行归类的，其中`"国别"`列的值相对规范，只有若干记录中会有些空值；而`"行政区"`列的值则非常的脏，主要问题表现为：

1. 行政区使用简称，比如大理南涧；
2. 行政等级信息缺失，比如“祥云县”缺少省级和市级行政区名称；
3. 名称缺少等级标识，比如“云龙”，不知是区还是县；
4. 格式和分隔符不统一，比如有用中文逗号作为分隔符，也有用空格，还有没有分隔符的；
5. 行政区中混有英文和拼音，比如“云南 Aning”。

类似这样的行政区数据大多转录自手写的纸质标签记录，尤其是那些年代比较久远的生物多样性原始数据集，这样简略的记录其实是广泛存在的，纯粹依靠人工逐条处理这些历史数据，其实是一件极为低效和不可靠的模式。而利用人工和 `ipybd`相结合的方式，可以大幅提高这类工作的效率和品质。

目前 `FormatDataSet` 实例的`format_admindiv`方法可以自动进行县级及其以上等级的中文行政区名称的清洗和转换：

```python
# 使用方式类似于学名处理方法，将覆盖国省市县行政区名的相关字段按序传递给方法即可
# 如果想要将清洗的结果直接替换 collections.df 数据表中的相应列
# 可以将这里的 inplace 保持默认，或设置为 True
collections.format_admindiv("国别", "行政区", inplace=False)

Out: 
   country province     city   county
0      !中国     None     None     None
1       中国      云南省  大理白族自治州  南涧彝族自治县
2       中国      河北省      承德市      平泉县
3       中国      广东省      广州市      白云区
4       中国      云南省  楚雄彝族自治州     None
5       中国      甘肃省     None     None
6      !中国      广东省      广州市      白云区
7       中国      河北省      承德市      承德县
8       中国      云南省  大理白族自治州     None
9       中国       台湾      新竹市     None
10      中国   内蒙古自治区      包头市   白云鄂博矿区
11     !中国      海南省     None     None
12      中国      河南省     None     None
13     !中国      河北省     None     None
14      中国      云南省  楚雄彝族自治州     None
15      中国       台湾      新竹市       东区
16      中国      云南省     None     None
17      中国       台湾      新竹市       东区
18      中国      云南省  大理白族自治州      祥云县
19      中国      云南省      临沧市       云县
20      中国      吉林省      通化市      东昌区
21      中国      山东省      聊城市     东昌府区
22      中国      江西省      抚州市      东乡县
23      中国      甘肃省  临夏回族自治州   东乡族自治县
24      中国      云南省  迪庆藏族自治州      德钦县
25      中国      安徽省      蚌埠市      怀远县
26      中国     黑龙江省      伊春市     None
27      中国      江苏省      徐州市      云龙区
28     !中国      四川省     None     None
29      中国     黑龙江省    齐齐哈尔市      龙江县

```

通过上述处理结果，可以发现`format_admindiv` 即便在应对简略的自然文本记录时，仍然可以将其中绝大多数的文本转换为正确规范的行政区等级。实际上随着数据完整性的提高，行政区文本的转换精度也会随之提高，在目前常用的数据规范下 `format_admindiv`的转换结果通常是可以被直接使用的。而对于信息比较简略的数据，`format_admindiv` 的优先参与也可以大幅降低后期人工核查的工作量，从而大大提高数据核查的质量和效率。

对于有疑议的转换，绝大多数情况下，`format_admindiv` 会将相应转换结果以英文"!"标注，但在一些特殊情况下仍然有可能会出现潜在的转换错误，这些情况包括：

1. 已经裁撤的行政区，比如第 28 行的 “四川南川”，程序只会匹配出“中国,四川省”，且不会做标注；
2. 拼音或英文行政区划，比如第 16 行的 “云南 Anning”，程序只会匹配到“中国,云南”且不会做标注；
3. 本身就有错误的行政区划，比如第 3 行的 “河北，承德，栾平县”，程序有一定的可能会返回错误的匹配并不做标识；
4. 难以通过字面文本确实的行政区，比如上述第 27 行的“云龙”，程序会随机返回一个同名的行政区且不会做标识；

上述问题在当前数据集之中并不广泛，但在历史数据集之中可能有一定的存量，使用中需要予以注意。

#### 2.4 日期、时间的清洗和转换

```python
collections.df['Time'].head(20) 

Out: 
0         2       X  1973
1             9  IX  1973
2           24 Aug., 2000
3                    1982
4              VIII  1982
5     2012-12-31 00:00:00
6                 60.6.30
7                   10995
8               1983.9.13
9                 4X'1994
10             VIII' 1963
11               4-6-1982
12    2013-03-30 12:30:09
13               19820431
14                 82.9.8
15               VI  1978
16                   9.12
17                2007.06
18             2007.07.13
19            12 IV' 1987
Name: Time, dtype: object
```
转换为国内目前广泛采用的 8 位整数型日期的：

```python
# 使用时直接传递所要清洗的日期列的列名给 foramt_datetime 方法
# 此外 style 参数可指定清洗后输出的日期格式，可传递的值目前有 "num"/"date"/"datetime"/"utc"，默认为 “datetime”样式
# mark 参数可指定是否返回带有!标记的错误日期，如果为 False，错误日期返回 None
# inplace 参数指定是否直接将转换后的列替代原数据表中的列
collections.format_datetime("Time", style='num', mark=True, inplace=False)

Out:
         Time
0    19731002
1    19730909
2    20000824
3    19820000
4    19820800
5    20121231
6    19600630
7      !10995
8    19830913
9    19941004
10   19630800
11   19820604
12   20130330
13  !19820431
14   19820908
15   19780600
16      !9.12
17   20070600
18   20070713
19   19870412
```

对于错误的日期，如果 `mark` 参数为 `True` ，会使用英文 “!” 标注返回。

转换为日期时间格式：

```python
collections.format_datetime("Time", style='datetime', mark=True, inplace=False)

Out:
                   Time
0    1973-10-2 00:00:00
1     1973-9-9 00:00:00
2    2000-8-24 00:00:00
3   1982-01-01 00:00:02
4    1982-8-01 00:00:01
5   2012-12-31 00:00:00
6    1960-6-30 00:00:00
7                !10995
8    1983-9-13 00:00:00
9    1994-10-4 00:00:00
10   1963-8-01 00:00:01
11    1982-6-4 00:00:00
12  2013-03-30 12:30:09
13            !19820431
14    1982-9-8 00:00:00
15   1978-6-01 00:00:01
16                !9.12
17   2007-6-01 00:00:01
18   2007-7-13 00:00:00
19   1987-4-12 00:00:00

```

如果原始数据没有时间，则补充"00:00:00"；如果原始数据没有day，则默认以每月 1 号 00:00:01 表示；如果原始数据缺失月份，则默认以该年 1 月 1 日 00:00:02 表示。这种转换方式可以将所有有效的日期和时间转换为规范可统计的时期时间文本。

转换为日期格式：

郗建勋. (1982). *55* (2020 ed.). 昆明: 中国科学院昆明植物研究所标本馆.

郗建勋.55* (2020 ed.). str: 昆明:中国科学院昆明植物研究所标本馆.

```python
collections.format_datetime("Time", style='date', mark=True, inplace=False)

Out:
          Time
0    1973-10-2
1     1973-9-9
2    2000-8-24
3   1982-01-01
4    1982-8-01
5   2012-12-31
6    1960-6-31
7       !10995
8    1983-9-13
9    1994-10-4
10   1963-8-01
11    1982-6-4
12   2013-3-30
13   !19820431
14    1982-9-8
15   1978-6-01
16       !9.12
17   2007-6-01
18   2007-7-13
19   1987-4-12
```

转换为 UTC 时间：

```python
# 默认为东八区时间，可以通过 timezone 参数手动指定，指定样式类似“+07:00”
collections.format_datetime("Time", style='utc', mark=True, inplace=False)

Out:
                         Time
0   1973-10-02T00:00:00+08:00
1   1973-09-09T00:00:00+08:00
2   2000-08-24T00:00:00+08:00
3   1982-01-01T00:00:02+08:00
4   1982-08-01T00:00:01+08:00
5   2012-12-31T00:00:00+08:00
6   1960-06-30T00:00:00+08:00
7                      !10995
8   1983-09-13T00:00:00+08:00
9   1994-10-04T00:00:00+08:00
10  1963-08-01T00:00:01+08:00
11  1982-06-04T00:00:00+08:00
12  2013-03-30T12:30:09+08:00
13                  !19820431
14  1982-09-08T00:00:00+08:00
15  1978-06-01T00:00:01+08:00
16                      !9.12
17  2007-06-01T00:00:01+08:00
18  2007-07-13T00:00:00+08:00
19  1987-04-12T00:00:00+08:00
```

UTC 世界协调时在处理和分析跨时区生物多样性数据时，具有明显优势。同时 UTC 时间支持`JSON Schema`时间样式，非常利于 web 平台间的数据交换。

#### 2.5 经纬度清洗和转换

经纬度数据是物种分布信息最为关键的信息，`FormatDataSet`实例为此提供了严格可靠的数据清洗方法 `format_latlon`，该方法既能最大限度的执行数据的自动清洗和转换，又能实现百分之百的数据纠错：

```python
collections.df['GPS'].head(20)     

Out[10]: 
0                N:28 34'478E:99 49 129"
1                       N:27 55'E:99 36'
2              N:38 34'481"E:099 50'054"
3     N: 24°35'51.22"; E: 100°04 '52.96"
4             N 31°04′206″, E 96°58′476″
5             N:26°14.636′，E:101°25.765′
6             24°53′01.78N,100°20′48.47E
7      N: 26°21'16.08", E: 103°01'43.76"
8               28 34'481",E:099 50'054"
9                         28 34'E:99 49'
10               27 20'356"N,100'04'776"
11                                   NaN
12                                   NaN
13                                   NaN
14               N:42.2354°, E:123.6607°
15                   N: 28 20', E:99 04'
16               41˚56'00"N, 123˚40'40"E
17      10˚37'08.83" N, 104˚01'53.97" E 
18                   S:64°41′, W: 62°37′
19                 48 45.9"N, 142 17.3'E
Name: GPS, dtype: object

```
调用`format_latlon`方法时需要将经纬度涉及的一列或两列的列名传递给该方法，`format_latlon`会自动纠正错位的经度和纬度，表格中经纬度的书写可以是十进制格式、度分格式、度分秒格式，或者以上几种的混合，数字之间的分隔符也没有统一的要求。

```python
collections.format_latlon("GPS", inplace=False)

Out:
   decimalLatitude decimalLongitude
0          28.5746          99.8188
1          27.9167             99.6
2          38.5747          99.8342
3          24.5976          100.081
4          31.0701          96.9746
5          26.2439          101.429
6          24.8838          100.347
7          26.3545          103.029
8              !28              !34
9              !28              !34
10             !27              !20
11            None             None
12            None             None
13            None             None
14         42.2354          123.661
15         28.3333          99.0667
16         41.9333          123.678
17         10.6191          104.032
18        -64.6833         -62.6167
19          48.765          142.288
```

#### 2.6 数值及数值区间的清洗和转换

`format_number` 函数可以对各种文本样式的数列或数值区间列进行处理，并以纯粹的整数或浮点数为元素返回 `list` 结果或者直接生成全新的数据列。

```python
# 首先预览一下海拔数据的情况
collections.df['altitude'].head(20) 

Out: 
0            NaN
1          大约10m
2      大概400-600
3            NaN
4          3800米
5         3800 m
6      1400～1800
7      1200-1300
8           1000
9           1250
10           700
11           700
12          1200
13           620
14       400+600
15       400-600
16       400～600
17       400-600
18       400-600
19       400—600
Name: 海拔, dtype: object
```
通过数据预览，可以发现 `collections` 实例的海拔属性是一个数值区间，而且区间间隔符号也不统一，有些数值还带有计量单位或者其他文本字符。`format_number` 方法在处理单个数列时，只需传递该列列名即可。但在处理数值区间时，就需要接受两个实际可调用的表格字段名，因此我们首先需要将 `collections` 的 `altitude` 属性拆分位两列，拆分数据列可以调用 `split_column` 方法：

```python
# split_column 方法会在下文详解
# 这里将 altitude 按照 '-' 符号拆分为 minimumElevation 和 maximumElevation 两个新列
collections.split_column("altitude", "-", new_headers["minimumElevation","maximumElevation"]) 
  
# 可以发现单纯的列拆分并不能将所有的区间值分开
# 但是它可以为进一步使用 fromat_number 方法提供基础
  Out: 
           minimumElevation         maximumElevation
0                       NaN                     None
1                     大约10m                     None
2                     大概400                      600
3                       NaN                     None
4                     3800米                     None
5                    3800 m                     None
6                 1400～1800                     None
7                      1200                     1300
8                      1000                     None
9                      1250                     None
10                      700                     None
11                      700                     None
12                     1200                     None
13                      620                     None
14                  400+600                     None
15                      400                      600
16                  400～600                     None
17                      400                      600
18                      400                      600
19                  400—600                     None

```

将拆分出的两个新列传递给 `format_number` 方法，进行数值清洗：

```python
# 调用 format_number 方法清洗数据列
# 同时指定清洗结果为整形，也可以根据需要将其指定为 float
# 该方法默认会将清洗结果直接替换 df 属性中的相应数据列
# 如果不希望直接替换被处理的数据列，可以在调用时设置 inplace=False
# 此外对于非法数值，该方法默认会在返回结果中删除该值，并以空值填充
# 如果希望标记和保留非法数值，可以在调用时设置 mark=True
collections.format_number("minimumElevation", "maximumElevation", typ=int)

# 预览处理结果，可以发现原先的数值区间已经准确的进行了拆分
# 原先的单个数值，则会默认补充为同值区间，以保证拆分结果的一致性
collections.df[["minimumElevation", "maximumElevation"]].head(20)  

Out: 
            minimumElevation          maximumElevation
0                       <NA>                      <NA>
1                         10                        10
2                        400                       600
3                       <NA>                      <NA>
4                       3800                      3800
5                       3800                      3800
6                       1400                      1800
7                       1200                      1300
8                       1000                      1000
9                       1250                      1250
10                       700                       700
11                       700                       700
12                      1200                      1200
13                       620                       620
14                       400                       600
15                       400                       600
16                       400                       600
17                       400                       600
18                       400                       600
19                       400                       600

```



#### 2.7 重复值标注

`FormatDataSet` 提供了类似 Excel 的行值判重功能，该功能可以通过 `mark_repeat` 方法实现。

```python
collections.df[["标本号", "国别", "Time"]]

Out: 
        标本号  国别        Time
0    016589  中国        1978
1    016589  中国        1978
2    016589  中国    1983.5.8
3    019387  中国    1983.5.8
4    016108  中国  1982.08.24
..      ...  ..         ...
507  016675  中国  1983.11.29
508  016676  中国  1983.12.12
509  016677  中国  1983.12.18
510  016678  中国  1975.03.04
511  016965  中国  1984.11.29

[512 rows x 3 columns]

```
通过预览，可以发现 `collections` 有些字段的值是有重复的，`mark_repeat` 支持分别以单列和多列为依据进行重复值标记，比如：

```python
# 以标本号作为判重依据
collections.mark_repeat("标本号")                                                                                                                                                                  
# 查看标记结果
collections.df[["标本号", "国别", "Time"]]                                                                                                                                                         
Out[14]: 
         标本号  国别        Time
0    !016589  中国        1978
1    !016589  中国        1978
2    !016589  中国    1983.5.8
3     019387  中国    1983.5.8
4     016108  中国  1982.08.24
..       ...  ..         ...
507   016675  中国  1983.11.29
508   016676  中国  1983.12.12
509   016677  中国  1983.12.18
510   016678  中国  1975.03.04
511   016965  中国  1984.11.29

[512 rows x 3 columns]

```

如上所示：凡是重复的标本号都会以英文 "!" 标注。如果想要以多个列值为依据进行重复值标记，可以在调用`mark_repeat`时提供多个真实可调用的列名即可：

```python
# 以标本号、国别、Time 三个字段联合判重
collections.mark_repeat("标本号", "国别", "Time")                                                                                                                                                  

# 查看标记结果
collections.df[["标本号", "国别", "Time"]]                                                                                                                                                         
Out: 
         标本号  国别        Time
0    !016589  中国        1978
1    !016589  中国        1978
2     016589  中国    1983.5.8
3     019387  中国    1983.5.8
4     016108  中国  1982.08.24
..       ...  ..         ...
507   016675  中国  1983.11.29
508   016676  中国  1983.12.12
509   016677  中国  1983.12.18
510   016678  中国  1975.03.04
511   016965  中国  1984.11.29

[512 rows x 3 columns]

```

通过多个列名进行重复值标记，程序只会标注那些相应字段均重复的数据。

#### 2.8 数据列的分割

`split_column`方法可以对文本数据列进行分拆操作，该方法与常用的文本列分割方法有些不同：`split_column` 的方法一次性可以接受多个不同分隔符进行分拆操作，但每个分隔符只能作用于一次拆分，比如 下方 `collections` 的`cite1` 字段是一个引文内容，各引文成分之间分别使用了","和":"进行了分割。

```python
collections.df["cite1"].head(10)                                                                                                                                                                   
Out: 
0           Linnaeus, 1758,Syst. Nat.,ed. 10,1:159
1      Sharpe,1894,Cat. Bds. Brit. Mus. 23:250,252
2                 Buturlin, 1916, OpH. Becth.7:224
3           Jerdon et Blyth, 1864, Bds. Ind. 3:648
4                         Riley, 1925, Auk 42: 423
5    Boddaert,17348,Tabl. Pl. enlum. Hist. Nat.:54
6         Swinhoe,1871,Proc. Zool. Soc. London:401
7                  Hartert,1917, Nov. Zool. 24:272
8         Swinhoe,1871,Proc. Zool. Soc. London:401
9                                              NaN
Name: cite1, dtype: object

```

如果想要将其拆分为作者、年代、杂志卷期、页码四列数据，就需要根据数据情况传递两个","分割符和一个":"分割符给`split_column`方法。

```python
collections.split_column("cite1", (",",",",":"), new_headers=["author", "year", "from", "page"])                                                                                                   

collections.df[["author", "year", "from", "page"]].head(10)                                                                                                                                        
Out: 
            author   year                         from     page
0         Linnaeus   1758          Syst. Nat.,ed. 10,1      159
1           Sharpe   1894      Cat. Bds. Brit. Mus. 23  250,252
2         Buturlin   1916                 OpH. Becth.7      224
3  Jerdon et Blyth   1864                  Bds. Ind. 3      648
4            Riley   1925                       Auk 42      423
5         Boddaert  17348  Tabl. Pl. enlum. Hist. Nat.       54
6          Swinhoe   1871      Proc. Zool. Soc. London      401
7          Hartert   1917                Nov. Zool. 24      272
8          Swinhoe   1871      Proc. Zool. Soc. London      401
9              NaN   None                         None     None

```

其中`split_column`方法第一个参数为需要拆分的列名。第二个参数为拆分所依据的分隔符，可以是字符（只根据该字符拆分一次），也可以是字符组成的元组（每个字符按序拆分一次）。第三个参数用于设置拆分后新列的列名，如果缺省，则返回 `list` 数据而不改变实例 `df` 属性的数据列；如果给予，则会直接改写`df`属性相应的数据列。上面示例子就是将原 `collections.df` 中 `cite`数据列改为了`author`，`year`, `from`,  `page` 四列。

`split_column` 方法同时支持中西文拆分，使用时可以将分隔符设为单个"$"符号或多个该符号组成的元组：

```python
collections.df["鉴定"].head(10)                                                                                                                                                                     
Out: 
0                                          青海二色香青
1                  白苞蒿Artemisia lactiflora Walld.
2                     马蛋果Gynocardia odorata Roxb.
3                  高山大风子Hydnocarpus alpinus Wight
4    海南大风子Hydnocarpus hainanensis (Merr.) Sleumer
5                   针叶韭Allium aciphyllum J. M. Xu
6                           llium caeruleum Pall.
7              滇南黄杨Buxus austroyunnanensis Hatus.
8                      雀舌黄杨uxus bodinieri H. Lév.
9                                             NaN
Name: 鉴定, dtype: object

```

拆分结果：

```python
collections.split_column("鉴定", "$", new_headers=["中文名", "拉丁名"])

collections.df[["中文名", "拉丁名"]].head(10)
Out: 
                     中文名                                      拉丁名
0                 青海二色香青                                         
1                    白苞蒿              Artemisia lactiflora Walld.
2                    马蛋果                 Gynocardia odorata Roxb.
3                  高山大风子                Hydnocarpus alpinus Wight
4                  海南大风子  Hydnocarpus hainanensis (Merr.) Sleumer
5                    针叶韭               Allium aciphyllum J. M. Xu
6  llium caeruleum Pall.                                         
7                   滇南黄杨           Buxus austroyunnanensis Hatus.
8                   雀舌黄杨                   uxus bodinieri H. Lév.
9                    NaN                                     None

```



#### 2.9 数据列的合并

`merge_columns` 方法支持多列按序拼接合并，合并分隔符可以是同样的字符：

```python
# 统一使用 : 号拼接上述被拆分的引文内容
# 调用 merge_columns 方法如果不传递 new_header 参数
# 则默认返回 list 类型的拼接结果，但不改变 df 属性的值
collections.merge_columns(["author", "year", "from", "page"], ":") 

['Linnaeus: 1758:Syst. Nat.,ed. 10,1:159',
 'Sharpe:1894:Cat. Bds. Brit. Mus. 23:250,252',
 'Buturlin: 1916: OpH. Becth.7:224',
 'Jerdon et Blyth: 1864: Bds. Ind. 3:648',
 'Riley: 1925: Auk 42: 423',
 'Boddaert:17348:Tabl. Pl. enlum. Hist. Nat.:54',
 'Swinhoe:1871:Proc. Zool. Soc. London:401',
 'Hartert:1917: Nov. Zool. 24:272',
 'Swinhoe:1871:Proc. Zool. Soc. London:401',
 None]
```

也可以使用不同的字符拼接各列：

```python
collections.merge_columns(["author", "year", "from", "page"], (",", "; ", ":"))

Out:
['Linnaeus, 1758; Syst. Nat.,ed. 10,1:159',
 'Sharpe,1894; Cat. Bds. Brit. Mus. 23:250,252',
 'Buturlin, 1916;  OpH. Becth.7:224',
 'Jerdon et Blyth, 1864;  Bds. Ind. 3:648',
 'Riley, 1925;  Auk 42: 423',
 'Boddaert,17348; Tabl. Pl. enlum. Hist. Nat.:54',
 'Swinhoe,1871; Proc. Zool. Soc. London:401',
 'Hartert,1917;  Nov. Zool. 24:272',
 'Swinhoe,1871; Proc. Zool. Soc. London:401',
 None]

```

如果调用 `merge_columns` 时指定了 `new_header` 属性，则返回 None ，同时会将处理结果直接合并到实例的 df 属性中，并删除参与合并的列：

```python
# 指定 new_header 后，方法执行后返回 None
collections.merge_columns(["author", "year", "from", "page"], (",", "; ", ":") ,new_header="cite")                                                                                                 

# df 属性中新增了合并的 cite 数据列，同时 author, year, from, page 列会被删除
collections.df['cite'].head(10)                                                                                                                                                                              
Out: 
0           Linnaeus, 1758; Syst. Nat.,ed. 10,1:159
1      Sharpe,1894; Cat. Bds. Brit. Mus. 23:250,252
2                 Buturlin, 1916;  OpH. Becth.7:224
3           Jerdon et Blyth, 1864;  Bds. Ind. 3:648
4                         Riley, 1925;  Auk 42: 423
5    Boddaert,17348; Tabl. Pl. enlum. Hist. Nat.:54
6         Swinhoe,1871; Proc. Zool. Soc. London:401
7                  Hartert,1917;  Nov. Zool. 24:272
8         Swinhoe,1871; Proc. Zool. Soc. London:401
9                                              None
Name: cite, dtype: object


```

`merge_columns` 方法不仅可以对数据列进行按序拼接，还可以将不同数据列组合为带 title 的换行文本，或者组装为 Python 的 `Dict` 和 `list`， JSON 的 `Object` 和 `Array` 对象。使用方法也很简单，只需在传递参数时，将分隔符参数按需设置为 "r"、"d"、"l"、"o"、"a" 中的某一个，即可将拼接结果转换为相应的形式。这里仍以上述已分列的引文数据为例：

```python
# 合并为带title的换行文本
collections.merge_columns(["author", "year", "from", "page"], "r")

# 组合结果带有字段 Title，且每个组合都以换行符\n 分开，这种形式非常适合需要带title的打印文本输出
Out:
['author：Linnaeus\nyear： 1758\nfrom：Syst. Nat.,ed. 10,1\npage：159',
 'author：Sharpe\nyear：1894\nfrom：Cat. Bds. Brit. Mus. 23\npage：250,252',
 'author：Buturlin\nyear： 1916\nfrom： OpH. Becth.7\npage：224',
 'author：Jerdon et Blyth\nyear： 1864\nfrom： Bds. Ind. 3\npage：648',
 'author：Riley\nyear： 1925\nfrom： Auk 42\npage： 423',
 'author：Boddaert\nyear：17348\nfrom：Tabl. Pl. enlum. Hist. Nat.\npage：54',
 'author：Swinhoe\nyear：1871\nfrom：Proc. Zool. Soc. London\npage：401',
 'author：Hartert\nyear：1917\nfrom： Nov. Zool. 24\npage：272',
 'author：Swinhoe\nyear：1871\nfrom：Proc. Zool. Soc. London\npage：401',
 None]



# 将每一组合并为 python 的 dict 对象 
collections.merge_columns(["author", "year", "from", "page"], "d")      

Out: 
[{'author': 'Linnaeus',
  'year': ' 1758',
  'from': 'Syst. Nat.,ed. 10,1',
  'page': '159'},
 {'author': 'Sharpe',
  'year': '1894',
  'from': 'Cat. Bds. Brit. Mus. 23',
  'page': '250,252'},
 {'author': 'Buturlin',
  'year': ' 1916',
  'from': ' OpH. Becth.7',
  'page': '224'},
 {'author': 'Jerdon et Blyth',
  'year': ' 1864',
  'from': ' Bds. Ind. 3',
  'page': '648'},
 {'author': 'Riley', 'year': ' 1925', 'from': ' Auk 42', 'page': ' 423'},
 {'author': 'Boddaert',
  'year': '17348',
  'from': 'Tabl. Pl. enlum. Hist. Nat.',
  'page': '54'},
 {'author': 'Swinhoe',
  'year': '1871',
  'from': 'Proc. Zool. Soc. London',
  'page': '401'},
 {'author': 'Hartert',
  'year': '1917',
  'from': ' Nov. Zool. 24',
  'page': '272'},
 {'author': 'Swinhoe',
  'year': '1871',
  'from': 'Proc. Zool. Soc. London',
  'page': '401'},
 None]



# 合并为 Python 的 list 对象
collections.merge_columns(["author", "year", "from", "page"], "l")

Out: 
[['Linnaeus', ' 1758', 'Syst. Nat.,ed. 10,1', '159'],
 ['Sharpe', '1894', 'Cat. Bds. Brit. Mus. 23', '250,252'],
 ['Buturlin', ' 1916', ' OpH. Becth.7', '224'],
 ['Jerdon et Blyth', ' 1864', ' Bds. Ind. 3', '648'],
 ['Riley', ' 1925', ' Auk 42', ' 423'],
 ['Boddaert', '17348', 'Tabl. Pl. enlum. Hist. Nat.', '54'],
 ['Swinhoe', '1871', 'Proc. Zool. Soc. London', '401'],
 ['Hartert', '1917', ' Nov. Zool. 24', '272'],
 ['Swinhoe', '1871', 'Proc. Zool. Soc. London', '401'],
 None]



# 合并为 Json 的 Object 对象
collections.merge_columns(["author", "year", "from", "page"], "o")

Out: 
['{"author": "Linnaeus", "year": " 1758", "from": "Syst. Nat.,ed. 10,1", "page": "159"}',
 '{"author": "Sharpe", "year": "1894", "from": "Cat. Bds. Brit. Mus. 23", "page": "250,252"}',
 '{"author": "Buturlin", "year": " 1916", "from": " OpH. Becth.7", "page": "224"}',
 '{"author": "Jerdon et Blyth", "year": " 1864", "from": " Bds. Ind. 3", "page": "648"}',
 '{"author": "Riley", "year": " 1925", "from": " Auk 42", "page": " 423"}',
 '{"author": "Boddaert", "year": "17348", "from": "Tabl. Pl. enlum. Hist. Nat.", "page": "54"}',
 '{"author": "Swinhoe", "year": "1871", "from": "Proc. Zool. Soc. London", "page": "401"}',
 '{"author": "Hartert", "year": "1917", "from": " Nov. Zool. 24", "page": "272"}',
 '{"author": "Swinhoe", "year": "1871", "from": "Proc. Zool. Soc. London", "page": "401"}',
 None]



# 合并为 JSON 的 Array 对象
collections.merge_columns(["author", "year", "from", "page"], "a")

Out: 
['["Linnaeus", " 1758", "Syst. Nat.,ed. 10,1", "159"]',
 '["Sharpe", "1894", "Cat. Bds. Brit. Mus. 23", "250,252"]',
 '["Buturlin", " 1916", " OpH. Becth.7", "224"]',
 '["Jerdon et Blyth", " 1864", " Bds. Ind. 3", "648"]',
 '["Riley", " 1925", " Auk 42", " 423"]',
 '["Boddaert", "17348", "Tabl. Pl. enlum. Hist. Nat.", "54"]',
 '["Swinhoe", "1871", "Proc. Zool. Soc. London", "401"]',
 '["Hartert", "1917", " Nov. Zool. 24", "272"]',
 '["Swinhoe", "1871", "Proc. Zool. Soc. London", "401"]',
 None]

```



### 三、数据模型定义

#### 3.1 特定数据集的结构重塑

```python
from ipybd import imodel                                                                                                                                                
from enum import Enum                                                                                                                                                   

@imodel 
class MyCollection(Enum): 
    记录人 = '$采集人' 
    记录编号 = '$采集号' 
    省_市 = {'$省市':','}
    行政区划 = ('$省市', '$区县', '，') 
    学名 = ('$属', '$种', '$种下等级', ' ') 

```



```python
cvh = MyCollection(r"/Users/.../cvh.xlsx") 

cvh.df.head()                                                                                                                                                          
Out: 
            记录人                    记录编号      记录时间    省     市                          学名
0    王雷,朱雅娟,黄振英  Beijing-huang-dls-0026  20070922   北京   北京市    Ostericum grosseserratum
1           NaN              YDDXSC-022  20071028  云南省   临沧市  Boenninghausenia albiflora
2  欧阳红才,穆勤学,奎文康              YDDXSC-022  20071028  NaN  None  Boenninghausenia albiflora
3   吴福川,查学州,余祥洪                     NaN  20070512  湖南省  张家界市       Broussonetia kazinoki
4   吴福川,查学州,余祥洪              SCSB-07009  20070512  湖南省  张家界市       Broussonetia kazinoki

```

#### 3.2 多源数据集的结构重塑

```python
from enum import Enum
from ipybd import imodel

@imodel  
class MyCollection(Enum):  
    记录人 = '$recordedBy'  
    记录编号 = '$recordNumber'  
    采集日期 = '$eventDate' 
    省_市 = {('$province', '$city'): ','} 
    学名 = ['$scientificName',  ('$genus', '$specificEpithet', '$taxonRank', '$infraspecificEpithet', ' ')] 
    
```



```python
cvh = MyCollection(r"/Users/.../cvh.xlsx", fields_mapping=True) 

cvh.df.head()

Out:
            记录人                    记录编号      记录时间          行政区划                          学名
0    王雷,朱雅娟,黄振英  Beijing-huang-dls-0026  20070922   北京，北京市，门头沟区    Ostericum grosseserratum
1           NaN              YDDXSC-022  20071028   云南省，临沧市，永德县  Boenninghausenia albiflora
2  欧阳红才,穆勤学,奎文康              YDDXSC-022  20071028           永德县  Boenninghausenia albiflora
3   吴福川,查学州,余祥洪                     NaN  20070512  湖南省，张家界市，永定区       Broussonetia kazinoki
4   吴福川,查学州,余祥洪              SCSB-07009  20070512  湖南省，张家界市，永定区       Broussonetia kazinoki

```

#### 3.2 数据值的清洗与转换

### 四、DarwinCore 模型

#### 4.1 Occurrence

#### 4.2 CVH

#### 4.3 NSII

#### 4.4 NOI

#### 4.5 KingdoniaPlant

###

### 五、标签打印

### 六、基于 Pandas 的数据统计与分析生态



### 七、特别声明

1. Ipybd 遵从 GNU General Public License v3.0 许可    
2. 本软件由 NSII 资助，© 徐洲锋，中国科学院昆明植物研究所
