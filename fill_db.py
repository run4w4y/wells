from oil_db import *

db = MainDB('oil')
LayerProperties('Argillite', '#E52B50', 'Аргиллит')
LayerProperties('Breccia', '#FFBF00', 'Брекчиа')
LayerProperties('Chalk', '#9966CC', 'Мел')
LayerProperties('Chert' ,'#FBCEB1' ,'Шерт')
LayerProperties('Coal', '#7FFFD4', 'Уголь')
LayerProperties('Conglomerate', '#007FFF', 'Конгломерат')
LayerProperties('Dolomite', '#0095B6', 'Доломит')
LayerProperties('Limestone', '#800020', 'Известняк')
LayerProperties('Marl', '#DE3163', 'Мергель')
LayerProperties('Mudstone', '#F7E7CE', 'Глинистый сланец')
LayerProperties('Sandstone', '#7FFF00', 'Песчаник')
LayerProperties('Shale', '#C8A2C8', 'Сланец')
LayerProperties('Tufa', '#BFFF00', 'Туф')
LayerProperties('Wackestone', '#FFFF00', 'Ваккит')
WellType('Oil')
WellType('Gas')
WellType('Oil-Gas')