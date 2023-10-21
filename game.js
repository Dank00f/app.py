window.onload = function() {
    var canvas = document.getElementById("gameCanvas");
    var ctx = canvas.getContext("2d");

    var sprites = {};

    function loadImages() {
        var imgUrls = {
            'wall': 'static/box.png',
            'empty': 'static/grass.png',
            'player': 'static/img.png'
        };

        var loaded = 0;
        var total = Object.keys(imgUrls).length;

        for (var key in imgUrls) {
            var img = new Image();
            img.onload = function() {
                loaded++;
                if (loaded === total) {
                    startGame();
                }
            };
            img.src = imgUrls[key];
            sprites[key] = img;
        }
    }

    function startGame() {
        var game = new PygameGame();
        game.start();
    }

    function PygameGame() {
        var self = this;

        var tileWidth = 50;
        var tileHeight = 50;
        var tiles = [];
        var player = null;
        var running = true;
        var fps = 60;
        var clock = null;
        var i = 0;

        function Tile(type, x, y) {
            this.type = type;
            this.x = x;
            this.y = y;
        }

        function Player(x, y) {
            this.x = x;
            this.y = y;
        }

        function loadLevel() {
            var level = [
                "....................",
                ".########..........#",
                ".#.................#",
                ".#.................#",
                ".#.......#.........#",
                ".##############..###",
                "...................."
            ];

            for (var y = 0; y < level.length; y++) {
                for (var x = 0; x < level[y].length; x++) {
                    var type = level[y][x];
                    var tile = new Tile(type, x, y);
                    tiles.push(tile);
                    if (type === '@') {
                        player = new Player(x, y);
                    }
                }
            }
        }

        function update() {
            // Обновите игровую логику здесь
            // Например, обработка движений игрока, проверка столкновений и т. д.
        }

        function draw() {
            // Отрисуйте игру здесь
            // Например, отрисовка фона, плиток и игрока
            // Используйте ctx.drawImage и sprites для отображения изображений
        }

        this.start = function() {
            loadLevel();
            clock = setInterval(function() {
                update();
                draw();
            }, 1000 / fps);
        };

        this.stop = function() {
            clearInterval(clock);
            running = false;
        };
    }

    loadImages();
};