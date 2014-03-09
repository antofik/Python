random = (@max)->
  Math.floor((Math.random()*max) + 1)

class Screen
  @speed = 1000
  @cell_width = 4000
  @cell_height = 3000

class Cell
  constructor: (@x, @y) ->
  goto: (location)->
    dx = @x * Screen.cell_width
    dy = @y * Screen.cell_height
    if location
      dx += location.x
      dy += location.y
    $('.layer-speed-1').animate({left: -dx + 'px', top: -dy + 'px'}, Screen.speed)

class Scene
  initialize: ->
    @container.css('left', Screen.cell_width*@cell.x);
    @container.css('top', Screen.cell_height*@cell.y);
    @container.show()
  enter: ->
    @cell.goto()

class Location
  constructor: (@x, @y) ->
  goto: ->


@.random = random
@.Screen = Screen
@.Cell = Cell
@.Location = Location
@.Scene = Scene

