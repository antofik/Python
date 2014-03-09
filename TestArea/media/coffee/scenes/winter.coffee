$C = @

class Winter extends $C.Scene
  cell: new $C.Cell(1,0)
  container: $('.scene-winter')
  beginSnowFall: ->
    $('.scene-winter').snowfall
      flakeCount : 1000
      maxSpeed : 10
  constructor: ->
    @initialize()
    @beginSnowFall()

$C.Winter = new Winter
