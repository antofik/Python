$C = @

class BlackAndWhite extends $C.Scene
  cell: new $C.Cell(0,0)
  container: $('.scene-black-and-white')
  position: true

  ############################# Locations ###############################################################

  AsProgram: new $C.Location(-1000,-600)
  LocationSite: new $C.Location(1000,0)
  LocationShop: new $C.Location(0,700)
  LocationImpossible: new $C.Location(1000,700)
  LocationPortfolio: new $C.Location(4000,0)

  enter: ->
    @cell.goto(@AsProgram)
    @mouseMove()

  ############################# Mouse move ##############################################################

  mouseMove: ->
    @container.mousemove((e)->
      alpha = 0.01
      x = e.pageX - $(@).offset().left
      y = e.pageY - $(@).offset().top
    )

  ############################# Canvas ##################################################################

  generateClouds: ->
    holder = $('.clouds', @container)
    for i in [1...3]
      new MovingItem(holder, -1200, -200, $C.Screen.cell_width, 1000)
    for i in [1...10]
      new MovingItem(holder, -1200, -200, $C.Screen.cell_width, $C.Screen.cell_height)
    crane = new MovingCrane(holder, -1200, 0, $C.Screen.cell_width, 500)
    crane.setXPosition(3000)
    #new MovingCrane(holder, -1200, 0, 1000, $C.Screen.cell_height)  //x: -1200..1000, y: -200..1000
  ########################################################################################################

  moveLeft: ->
    $('.background', @container).animate
      left: "+=100px"
      500

  wait2: (time, callback) =>
    setTimeout =>
        callback.apply(@)
      ,10000

  moveRight: ->
    $('.background', @container).animate
      left: "-=100px"
      500

  hookGotos: ->
    $('.gotoSite').click (e)=>
      @cell.goto(@LocationSite)
    $('.gotoShop').click (e)=>
      @cell.goto(@LocationShop)
    $('.gotoImpossible').click (e)=>
      @cell.goto(@LocationImpossible)
    $('.gotoPortfolio').click (e)=>
      @cell.goto(@LocationPortfolio)

  moveBackground: (x,y) ->
    width = $(window).width()
    if (x<width/3) and @position
      @position = false
      @moveRight()
    if (x>2*width/3) and not @position
      @position = true
      @moveLeft()



  hookGlobalMove: ->
    $('html').mousemove (e) =>
      @moveBackground(e.clientX, e.clientY)

  constructor: ->
    @initialize()
    @generateClouds()
    @hookGotos()
    @hookGlobalMove()



#############################
### Moving cloud ############
#############################
class MovingItem
  minNumber: 1
  maxNumber: 17
  minSpeed: 500
  maxSpeed: 1500
  rightToLeft: false

  constructor: (holder, @x1, @y1, @x2, @y2) ->
    cloudNumber = Math.floor(@minNumber + Math.random()*(@maxNumber - @minNumber))
    id = 'cloud' + Math.floor(Math.random()*1000) + "_" + Math.floor(Math.random()*1000) + "_" + Math.floor(Math.random()*1000)
    cloudDiv = "<img class='cloud' id='" + id + "' src='/media/images/black-and-white/clouds/" + cloudNumber + ".png' />"

    @start_x = if @rightToLeft then x2 else x1
    @end_x = if @rightToLeft then x1 else x2
    @random_x = Math.floor(@x1 + Math.random()*(@x2 - @x1))
    @start_y = Math.floor(@y1 + Math.random()*(@y2 - @y1))
    @speed = Math.floor(@minSpeed + Math.random()*(@maxSpeed - @minSpeed))
    
    holder.append(cloudDiv)
    @cloud = $('#' + id)
    @cloud.css('left', @random_x)
    @cloud.css('top', @start_y)
    @cloud[0].ai = @

    @run()

  setXPosition: (x) ->
    @stop()
    @cloud.css('left', x)
    @run()

  hide: ->
    @cloud.hide()

  show: ->
    @cloud.show()

  stop: =>
    @cloud.stop()

  start: =>
    @run()

  run: ->
    @length = Math.abs(@cloud.position().left - @end_x)
    @time = Math.floor(10000*@length/@speed)
    @cloud.animate
      left: @end_x + "px"
      @time
      'linear'
      =>
        @cloud.css('left', @start_x)    
        @length = Math.abs(@end_x - @start_x)
        @time = Math.floor(10000*@length/@speed)
        setTimeout =>
            @run()        
          ,1000

#############################
### Moving crane ############
#############################
class MovingCrane extends MovingItem
  minNumber: 0
  maxNumber: 0
  rightToLeft: true


$C.BlackAndWhite = new BlackAndWhite
