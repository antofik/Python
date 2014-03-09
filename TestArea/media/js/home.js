//----------------------------- Constants ------------------------------------
var cell_width = 4000;
var cell_height = 3000;
var currentScene;
//----------------------------- Functions ------------------------------------


function random(max){
    return Math.floor((Math.random()*max)+1)
}

function gotoPoint(x, y) {
    initializeButtons();
    var alpha = 2;
    var speed = 1000;
    x = x * cell_width;
    y = y * cell_height;
    $('.layer-speed-1').animate({left: -x + 'px', top: -y + 'px'}, speed);
    $('.layer-speed-2').animate({left: -x*alpha + 'px', top: -y*alpha + 'px'}, speed);
}

function Point(container, x,y){
    this.x = x;
    this.y = y;
    this.Container = container;
    this.Container.css('left', cell_width*this.x);
    this.Container.css('top', cell_height*this.y);
    this.Goto = function(){gotoPoint(this.x, this.y);}
}

function Locations(){
    this.Autemn = new Scene_Autemn();
    this.Winter = new Scene_Winter();
    this.AutemnLake = new Scene_AutemnLake();
    this.AutemnRoad = new Scene_AutemnRoad();
    this.GreenLeaves = new Scene_GreenLeaves();
    this.RedLeaves = new Scene_RedLeaves();
    this.WaterGreenLeaves = new Scene_WaterGreenLeaves();
    this.WhitePinkLeaves = new Scene_WhitePinkLeaves();
    this.WhiteRedLeaves = new Scene_WhiteRedLeaves();
    this.WinterTree = new Scene_WinterTree();
    this.YellowLeaves = new Scene_YellowLeaves();
}

function initializeButtons(){
    $('.btn').unbind('click');
    $('.btn').hide();
    currentScene.initializeButtons();
}

//------------------------------ Scenes ---------------------------------------

function Scene_Autemn(){
    this.Container = $('.scene-autemn');
    this.Point = new Point(this.Container, 0,0);
    this.Goto = function(){currentScene=document.Location.Autemn; this.Point.Goto();};
    this.initialize = function(){
        this.initializeButtons();
        this.generateClouds();
        this.Container.show();
    }
    this.initializeButtons = function(){
        $('.btn-down').show();
        $('.btn-down').click(function(){document.Location.AutemnLake.Goto();});
    }
    this.generateClouds = function() {
        var container = $('.clouds');
        for (var i=0;i<10;i++) this.generateCloud(container, 0);
    }

    this.generateCloud = function(container, offset) {
        var cloudNumber = random(28);
        var id = 'cloud' + random(1000) + "_" + random(1000) + "_" + random(1000);
        var cloudDiv = "<img class='cloud' id='" + id +"' src='/media/images/clouds/" + cloudNumber + ".png'  />";
        var x = random(cell_width);
        var y = random(cell_height);
        container.append(cloudDiv);
        var cloud = $('#' + id);
        cloud.css('left', x + offset);
        cloud.css('top', y);
        var speed = 500+random(1000);
        var length = x + offset + 300;
        var time = Math.floor(10000*length/speed);
        this.runCloud(cloud, time, offset);
    }

    this.runCloud = function(cloud, time, offset){
        var _cloud = this;
        cloud.animate({left: "-300px"}, time, 'linear', function(){
            $(this).css('left', cell_width);
            setTimeout(function(){
                var speed = 500+random(1000);
                var length = cell_width + offset + 300;
                time = Math.floor(10000*length/speed);
                _cloud.runCloud(cloud, time, offset);
            }, 100);
        })
    }

    this.initialize();
}

function Scene_Winter(){
    this.Container = $('.scene-winter');
    this.Point = new Point(this.Container, 1,0);
    this.Goto = function(){currentScene=document.Location.Winter; this.Point.Goto();};
    this.initialize = function(){
        this.initializeButtons();
        this.beginSnowFall();
        this.Container.show();
    }
    this.initializeButtons = function(){
        $('.btn-left').show();
        $('.btn-left').click(function(){document.Location.Autemn.Goto();});
    }
    this.beginSnowFall = function(){
        $('.scene-winter').snowfall({flakeCount : 1000, maxSpeed : 10});
    }

    this.initialize();
}

function Scene_AutemnLake(){
    this.Container = $('.scene-autemn-lake');
    this.Point = new Point(this.Container, 0,1);
    this.Goto = function(){currentScene=document.Location.AutemnLake; this.Point.Goto();};
    this.initialize = function(){
        this.initializeButtons();
        this.Container.show();
    }
    this.initializeButtons = function(){
        $('.btn-right').show();
        $('.btn-right').click(function(){document.Location.AutemnRoad.Goto();});
    }

    this.initialize();
}

function Scene_AutemnRoad(){
    this.Container = $('.scene-autemn-road');
    this.Point = new Point(this.Container, 1,1);
    this.Goto = function(){currentScene=this; this.Point.Goto();};
    this.initialize = function(){
        this.initializeButtons();
        this.Container.show();
    }
    this.initializeButtons = function(){
        $('.btn-up').show();
        $('.btn-up').click(function(){document.Location.GreenLeaves.Goto();});
    }

    this.initialize();
}

function Scene_GreenLeaves(){
    this.Container = $('.scene-green-leaves');
    this.Point = new Point(this.Container, 2,0);
    this.Goto = function(){currentScene=this; this.Point.Goto();};
    this.initialize = function(){
        this.initializeButtons();
        this.Container.show();
    }
    this.initializeButtons = function(){
        $('.btn-down').show();
        $('.btn-down').click(function(){document.Location.RedLeaves.Goto();});
    }

    this.initialize();
}

function Scene_RedLeaves(){
    this.Container = $('.scene-red-leaves');
    this.Point = new Point(this.Container, 2,1);
    this.Goto = function(){currentScene=this; this.Point.Goto();};
    this.initialize = function(){
        this.initializeButtons();
        this.Container.show();
    }
    this.initializeButtons = function(){
        $('.btn-down').show();
        $('.btn-down').click(function(){document.Location.WaterGreenLeaves.Goto();});
    }

    this.initialize();
}

function Scene_WaterGreenLeaves(){
    this.Container = $('.scene-water-green-leaves');
    this.Point = new Point(this.Container, 2,2);
    this.Goto = function(){currentScene=this; this.Point.Goto();};
    this.initialize = function(){
        this.initializeButtons();
        this.Container.show();
    }
    this.initializeButtons = function(){
        $('.btn-left').show();
        $('.btn-left').click(function(){document.Location.WhitePinkLeaves.Goto();});
    }

    this.initialize();
}

function Scene_WhitePinkLeaves(){
    this.Container = $('.scene-white-pink-leaves');
    this.Point = new Point(this.Container, 1,2);
    this.Goto = function(){currentScene=this; this.Point.Goto();};
    this.initialize = function(){
        this.initializeButtons();
        this.Container.show();
    }
    this.initializeButtons = function(){
        $('.btn-left').show();
        $('.btn-left').click(function(){document.Location.WhiteRedLeaves.Goto();});
    }

    this.initialize();
}

function Scene_WhiteRedLeaves(){
    this.Container = $('.scene-white-red-leaves');
    this.Point = new Point(this.Container, 0,2);
    this.Goto = function(){currentScene=this; this.Point.Goto();};
    this.initialize = function(){
        this.initializeButtons();
        this.Container.show();
    }
    this.initializeButtons = function(){
        $('.btn-up').show();
        $('.btn-up').click(function(){document.Location.WinterTree.Goto();});
    }

    this.initialize();
}

function Scene_WinterTree(){
    this.Container = $('.scene-winter-tree');
    this.Point = new Point(this.Container, 3,1);
    this.Goto = function(){currentScene=this; this.Point.Goto();};
    this.initialize = function(){
        this.initializeButtons();
        this.Container.show();
    }
    this.initializeButtons = function(){
        $('.btn-down').show();
        $('.btn-down').click(function(){document.Location.YellowLeaves.Goto();});
    }

    this.initialize();
}

function Scene_YellowLeaves(){
    this.Container = $('.scene-yellow-leaves');
    this.Point = new Point(this.Container, 3,2);
    this.Goto = function(){currentScene=this; this.Point.Goto();};
    this.initialize = function(){
        this.initializeButtons();
        this.Container.show();
    }
    this.initializeButtons = function(){
        $('.btn-up').show();
        $('.btn-up').click(function(){document.Location.Winter.Goto();});
    }

    this.initialize();
}

function main(){
   document.Location = new Locations();
   document.Location.Autemn.Goto();
}

$(main);

