pygame实现简单推箱子游戏

推箱子游戏中会有一个封闭的围墙，围城一个不规则的多边形区域，人和箱子只能在这个区域内活动。区域内有一个人，几个箱子和目标点，使用方向键控制人的位置推动箱子到目标点即为成功。一次只能推动一个箱子，如果箱子到了死角则无法继续游戏。



sokoban_1.py实现从文件读取游戏地图