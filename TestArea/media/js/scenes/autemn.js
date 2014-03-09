function Scene_Home(){
    this.Point = new Point(0,0);
    this.Point1 = new Point(0,1000);
    this.Point2 = new Point(2000,1000);
    this.Point3 = new Point(1000,0);
    this.Point4 = new Point(1000,1600);
    this.Goto = function(){this.Point.Goto();}
    this.Goto1 = function(){this.Point1.Goto();}
    this.Goto2 = function(){this.Point2.Goto();}
    this.Goto3 = function(){this.Point3.Goto();}
    this.Goto4 = function(){this.Point4.Goto();}
    function initialize(){
        initializeButtons();
        generateClouds();
    }
    function initializeButtons(){
        $('.btn-left').click(function(){document.Location.Home.Goto1();});
        $('.btn-right').click(function(){document.Location.Home.Goto2();});
        $('.btn-top').click(function(){document.Location.Home.Goto3();});
        $('.btn-bottom').click(function(){document.Location.Home.Goto4();});
        $('.btn-to-winter').click(function(){document.Location.Winter.Goto();});
    }
    function generateClouds() {
        var container = $('.clouds');
        for (var i=0;i<100;i++) generateCloud(container, 0);
    }

    function generateCloud(container, offset) {
        var cloudNumber = random(28);
        var id = 'cloud' + random(1000) + "_" + random(1000) + "_" + random(1000);
        var cloudDiv = "<img class='cloud' id='" + id +"' src='/media/images/clouds/" + cloudNumber + ".png'  />"
        var x = random(6000) - 500;
        var y = random(4000) - 500;
        container.append(cloudDiv);
        var cloud = $('#' + id);
        cloud.css('left', x + offset);
        cloud.css('top', y);
        var speed = 500+random(1000);
        var length = x + offset + 300;
        var time = Math.floor(10000*length/speed);
        //runCloud(cloud, time, offset);
    }

    function runCloud(cloud, time, offset){
        cloud.animate({left: "-300px"}, time, 'linear', function(){
            $(this).css('left', 6000);
            setTimeout(function(){
                var speed = 500+random(1000);
                var length = 6000 + offset + 300;
                time = Math.floor(10000*length/speed);
                runCloud(cloud, time, offset);
            }, 100);
        })
    }

    initialize();
}